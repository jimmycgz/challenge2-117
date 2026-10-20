#!/usr/bin/env bash
#
# Deploy the food broker to Cloud Run from source. Cloud Build builds the image in the project, so
# nothing is built locally. Run from anywhere:   bash agent/deploy.sh
#
# Refuses to deploy unless gcloud is signed in as the lab account, on the lab project, and the same
# identity guard the agent runs with accepts the credentials. A deploy as the wrong identity stops here.
#
# Required settings (from the environment or from lab.env next to this script; a missing one stops the script):
#   A4I_EXPECTED_PROJECT           the lab project id
#   A4I_EXPECTED_PRINCIPAL_SUFFIX  how the lab account's address ends
# Optional: REGION (default us-east1), VERTEX_LOCATION (default global, or GOOGLE_CLOUD_LOCATION when set), SERVICE (default food-broker),
#   PYTHON (interpreter with the agent's requirements, default python3), A4I_MODEL, A4I_THINKING_LEVEL (LOW, MEDIUM or HIGH), NO_UI=1 for the API only
#   (the chat page is on by default), OPEN=0 to require
#   authentication (open by default, by the team's decision: ADK's API server has no authentication of its
#   own, so spend is bounded by --max-instances, --concurrency and --timeout below), A4I_ALLOW_ORIGINS for CORS,
#   NO_MCP=1 to leave out the BigQuery MCP toolset.

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"

# Settings shared with the team: lab.env fills in anything you have not set yourself. It holds no secrets.
if [[ -f "${HERE}/lab.env" ]]; then
  while IFS='=' read -r key value; do
    [[ -z "${!key:-}" ]] && export "${key}=${value}"
  done < <(grep -E '^[A-Z0-9_]+=' "${HERE}/lab.env")
fi

: "${A4I_EXPECTED_PROJECT:?set A4I_EXPECTED_PROJECT to the lab project id}"
: "${A4I_EXPECTED_PRINCIPAL_SUFFIX:?set A4I_EXPECTED_PRINCIPAL_SUFFIX to the lab account suffix}"
REGION="${REGION:-us-east1}"
VERTEX_LOCATION="${VERTEX_LOCATION:-${GOOGLE_CLOUD_LOCATION:-global}}"
# Say what will run, and stop on a combination that fails at the first question: gemini-3.x models exist only in the
# global location, and setup.sh tells people to export GOOGLE_CLOUD_LOCATION=us-central1.
echo "model: ${A4I_MODEL:-<default>}  location: ${VERTEX_LOCATION}  thinking: ${A4I_THINKING_LEVEL:-<default>}"
[[ "${A4I_MODEL:-}" == gemini-3* && "${VERTEX_LOCATION}" != "global" ]] \
  && { echo "REFUSED: ${A4I_MODEL} needs location global, got ${VERTEX_LOCATION} (unset GOOGLE_CLOUD_LOCATION and VERTEX_LOCATION)" >&2; exit 2; }
SERVICE="${SERVICE:-food-broker}"
PYTHON="${PYTHON:-python3}"

command -v gcloud >/dev/null 2>&1 || { echo "gcloud not found" >&2; exit 1; }

ACCOUNT="$(gcloud config get-value account 2>/dev/null || true)"
PROJECT="$(gcloud config get-value project 2>/dev/null || true)"
echo "gcloud account: ${ACCOUNT}"
echo "gcloud project: ${PROJECT}"
[[ "${PROJECT}" == "${A4I_EXPECTED_PROJECT}" ]] \
  || { echo "REFUSED: gcloud project is '${PROJECT}', expected '${A4I_EXPECTED_PROJECT}'" >&2; exit 2; }
[[ "${ACCOUNT}" == *"${A4I_EXPECTED_PRINCIPAL_SUFFIX}" ]] \
  || { echo "REFUSED: gcloud account '${ACCOUNT}' does not end in '${A4I_EXPECTED_PRINCIPAL_SUFFIX}'" >&2; exit 2; }

# The agent's own guard, on the credentials any code run from here would use.
( cd "${HERE}" && GOOGLE_CLOUD_PROJECT="${A4I_EXPECTED_PROJECT}" "${PYTHON}" -W ignore -m food_broker.identity_guard ) \
  || { echo "REFUSED: identity guard did not accept the credentials" >&2; exit 2; }

PROJECT_NUMBER="$(gcloud projects describe "${A4I_EXPECTED_PROJECT}" --format='value(projectNumber)')"

AUTH_FLAG="--no-allow-unauthenticated"
# The team chose to leave the service open so judges can use it; OPEN=0 keeps it behind authentication.
[[ "${OPEN:-1}" == "1" ]] && AUTH_FLAG="--allow-unauthenticated"

ENV_VARS="GOOGLE_CLOUD_PROJECT=${A4I_EXPECTED_PROJECT}"
ENV_VARS+=",A4I_EXPECTED_PROJECT=${A4I_EXPECTED_PROJECT}"
ENV_VARS+=",A4I_EXPECTED_PRINCIPAL_SUFFIX=${A4I_EXPECTED_PRINCIPAL_SUFFIX}"
ENV_VARS+=",A4I_EXPECTED_PROJECT_NUMBER=${PROJECT_NUMBER}"
ENV_VARS+=",GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_LOCATION=${VERTEX_LOCATION}"
[[ -n "${A4I_MODEL:-}" ]] && ENV_VARS+=",A4I_MODEL=${A4I_MODEL}"
[[ -n "${A4I_THINKING_LEVEL:-}" ]] && ENV_VARS+=",A4I_THINKING_LEVEL=${A4I_THINKING_LEVEL}"
# ADK's chat page is served by default; NO_UI=1 serves the API only.
[[ "${NO_UI:-0}" != "1" ]] && ENV_VARS+=",A4I_UI_FLAG=--with_ui"
# One instance only: ADK keeps chat sessions in that instance's memory, so a second instance would lose a follow-up.
# Google's managed BigQuery MCP server, for free-form questions about the data; NO_MCP=1 leaves it out.
[[ "${NO_MCP:-0}" != "1" ]] && ENV_VARS+=",A4I_MCP=1"
[[ -n "${A4I_ALLOW_ORIGINS:-}" ]] && ENV_VARS+=",A4I_ALLOW_ORIGINS=${A4I_ALLOW_ORIGINS}"

echo "deploying ${SERVICE} to ${REGION} (${AUTH_FLAG})"
gcloud run deploy "${SERVICE}" \
  --project "${A4I_EXPECTED_PROJECT}" \
  --region "${REGION}" \
  --source "${HERE}" \
  "${AUTH_FLAG}" \
  --min-instances 1 --max-instances 1 --concurrency 8 --timeout 300 \
  --memory 1Gi \
  --set-env-vars "${ENV_VARS}"
