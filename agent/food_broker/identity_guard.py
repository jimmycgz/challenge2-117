"""Refuse to run as anyone but the hackathon lab identity.

This box's default Application Default Credentials can belong to a different organization. If this
process fell back to them, every BigQuery query and Gemini call would run in the wrong cloud. So the
guard reads who the credentials really are and which project they resolve to, and stops otherwise.

Configuration (no defaults, so a missing value refuses rather than guesses):
  A4I_EXPECTED_PROJECT           the lab project id
  A4I_EXPECTED_PRINCIPAL_SUFFIX  e.g. "@qwiklabs.net" for the lab's student account

Where the code runs as a service account of the lab project itself (Cloud Run, Agent Runtime) the
principal is that project's service account, not a student account. A service account is accepted
only by its EMAIL: <A4I_EXPECTED_PROJECT>.iam.gserviceaccount.com, the project's default compute
account (needs A4I_EXPECTED_PROJECT_NUMBER, no default), or an address in A4I_SA_ALLOWLIST. The
project the credentials resolve to proves nothing on its own, since GOOGLE_CLOUD_PROJECT overrides
it. Impersonated credentials are refused outright.
"""

import json
import os
import urllib.parse
import urllib.request


class WrongIdentity(RuntimeError):
    pass


def check_identity(principal: str, project: str, is_service_account: bool,
                   expected_project: str, suffix: str, project_number: str = "",
                   sa_allowlist: tuple = (), impersonated: bool = False) -> str:
    """Pure decision. Returns a one-line description of the accepted identity, or raises.

    The resolved `project` is NOT proof of who is calling: google.auth.default() takes it from
    GOOGLE_CLOUD_PROJECT or the quota project when those are set, whatever the credential is. So a
    service account is judged on its email, never on the project it resolved to.
    """
    if not expected_project or not suffix:
        raise WrongIdentity(
            "A4I_EXPECTED_PROJECT and A4I_EXPECTED_PRINCIPAL_SUFFIX must both be set. "
            "Refusing to run without knowing which identity is allowed.")
    if impersonated:
        raise WrongIdentity(
            f"Impersonated credentials ({principal!r}) are refused outright: the account that "
            "does the impersonating is not checked here.")
    if project != expected_project:
        raise WrongIdentity(
            f"Credentials resolve to project {project!r}, expected {expected_project!r}. "
            "Refusing to run. Check GOOGLE_APPLICATION_CREDENTIALS and the gcloud config dir.")
    if is_service_account:
        belongs = (
            principal.endswith(f"@{expected_project}.iam.gserviceaccount.com")
            or (bool(project_number)
                and principal == f"{project_number}-compute@developer.gserviceaccount.com")
            or principal in sa_allowlist
        )
        if not belongs:
            raise WrongIdentity(
                f"Service account {principal!r} does not belong to project {expected_project!r} "
                "(not its own iam.gserviceaccount.com address, its default compute account, or "
                "on A4I_SA_ALLOWLIST). Refusing to run.")
        return f"service account {principal} in project {project}"
    if not principal.endswith(suffix):
        raise WrongIdentity(
            f"Credentials belong to {principal!r}, which does not end in {suffix!r}. "
            "Refusing to run: this may be a different organization's identity.")
    return f"user {principal} in project {project}"


def _principal_of(creds) -> tuple[str, bool, bool]:
    """(email, is_service_account, impersonated) for a google-auth credential object."""
    import google.auth.impersonated_credentials

    if isinstance(creds, google.auth.impersonated_credentials.Credentials):
        return getattr(creds, "service_account_email", "") or "unknown", True, True
    sa = getattr(creds, "service_account_email", None)
    if sa == "default":
        # Compute-engine style credentials report "default" until the metadata server is asked.
        import google.auth.transport.requests
        creds.refresh(google.auth.transport.requests.Request())
        sa = creds.service_account_email
    if sa:
        return sa, True, False
    # User credentials from `gcloud auth application-default login`: ask Google who the token is.
    import google.auth.transport.requests
    creds.refresh(google.auth.transport.requests.Request())
    url = "https://oauth2.googleapis.com/tokeninfo?" + urllib.parse.urlencode(
        {"access_token": creds.token})
    with urllib.request.urlopen(url, timeout=10) as resp:  # noqa: S310  (fixed https endpoint)
        info = json.load(resp)
    email = info.get("email")
    if not email:
        raise WrongIdentity("Could not read the credential's email (token lacks the email scope).")
    return email, False, False


_accepted: str | None = None


def assert_lab_identity() -> str:
    """Read the active credentials and refuse unless they are the lab's. Cached after success."""
    global _accepted
    if _accepted:
        return _accepted
    import google.auth
    import google.auth.exceptions

    try:
        creds, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"])
    except google.auth.exceptions.DefaultCredentialsError as exc:
        raise WrongIdentity(f"No usable credentials ({exc}). Refusing to run.") from exc
    principal, is_sa, impersonated = _principal_of(creds)
    _accepted = check_identity(
        principal, project or "",
        is_sa,
        os.environ.get("A4I_EXPECTED_PROJECT", ""),
        os.environ.get("A4I_EXPECTED_PRINCIPAL_SUFFIX", ""),
        project_number=os.environ.get("A4I_EXPECTED_PROJECT_NUMBER", ""),
        sa_allowlist=tuple(e.strip() for e in os.environ.get("A4I_SA_ALLOWLIST", "").split(",")
                           if e.strip()),
        impersonated=impersonated,
    )
    return _accepted


if __name__ == "__main__":
    # `python -m food_broker.identity_guard` for deploy scripts: exit 0 only on the lab identity.
    try:
        print("identity ok:", assert_lab_identity())
    except WrongIdentity as exc:
        print("REFUSED:", exc)
        raise SystemExit(2)
