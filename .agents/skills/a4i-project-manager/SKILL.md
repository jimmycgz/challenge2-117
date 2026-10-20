---
name: a4i-project-manager
description: >-
  Use this skill when the user asks to audit project progress, manage GitHub issues/labels/assignees,
  check team lane status, verify Cloud Run or BigQuery deployment readiness, track the 4 AngelHack
  submission deliverables, or prepare the pitch deck and demo video for the Chicago Food Rescue
  Broker (Challenge 2 / Track 1).
---

# Chicago Food Rescue Broker — Project & Deliverables Manager

This skill provides a complete workflow for auditing, coordinating, and shipping the **Chicago Food Rescue Broker** (`jimmycgz/challenge2-117`) across the team, GitHub Issues, and Google Cloud (`qwiklabs-gcp-04-6c7101c1dba1`).

## Quick Audit Runbook

1. **Run the automated project audit script:**
   Execute [audit_project.sh](./scripts/audit_project.sh) from the repository root to inspect Git branches, open PRs, GitHub issue status/pickup labels, and live Cloud Run health in one pass:

   ```bash
   bash .agents/skills/a4i-project-manager/scripts/audit_project.sh
   ```

2. **Consult the Deliverables & Rubric Reference:**
   Read [deliverables_rubric.md](./references/deliverables_rubric.md) when checking the 4 Mandatory Judge Checks, the 7 Coordinator Questions, the 4 AngelHack portal links, or the team roster mapping.

---

## Managing GitHub Issues, Labels & Team Pickup State

Before mutating issues or labels on `jimmycgz/challenge2-117`, check which account `gh` will act as (`gh api user --jq .login`). Do not switch, log in or log out the machine-wide `gh` account to make a command work; if it is the wrong account, stop and ask.

### 1. Label Taxonomy

Every issue in `jimmycgz/challenge2-117` must carry **4 label dimensions** so teammates immediately know what to pick up:

* **Pickup Action (Whether someone needs to pick it up):**
  * `needs-pickup` (Red `#D93F0B`) — **Action Required:** Open tasks must be completed before submission.
  * `optional-pickup` (Yellow `#FBCA04`) — **Core Complete:** Only a quick browser dry-run or optional stretch feature remains.
  * `no-pickup-needed` (Green `#0E8A16`) — **Done / Reference:** Already built, verified, and captured in `docs/evidence/`.
* **Completion Status:**
  * `status: done` — 100% implemented and verified.
  * `status: in-progress` — 50–95% complete; see unchecked `[ ]` items in the issue body.
  * `status: reference` — Architecture / team alignment documentation.
* **Lane Tag:**
  * `lane: repo-env`, `lane: data-audit`, `lane: agent-tools`, `lane: prompt-eval`, `lane: frontend-deploy`, `lane: story-pitch`
* **Owner Tag & GitHub Assignee (Self-Pickup Policy):**
  * **Do NOT pre-assign open/unclaimed issues by default.** Unclaimed issues carry `assignee: unassigned` and have no GitHub assignee so teammates can pick them up themselves.
  * Once a teammate claims an issue (or has already committed the code for it), remove `assignee: unassigned`, add their `owner: <handle>` label (`owner: jimmycgz`, `owner: k0d3r3d`, `owner: f1mahesh`, `owner: kkeremkurt`, `owner: mb-misha`), and set `--add-assignee <handle>`.

### 2. Claiming an Issue / Updating Status After Progress (Evidence-Backed Rule)

**CRITICAL RULE:** Never mark an issue or sub-task `status: done` without linking concrete proof in a **"Proof of What Was Built, Deployed & Tested"** table inside the issue body:

1. **Pull Request & Commit Link:** Link the merged PR and commit SHA on `main`.
2. **Code Built:** Link the exact files on `main` (`https://github.com/jimmycgz/challenge2-117/blob/main/...`).
3. **Deployment Proof:** State the GCP project (`qwiklabs-gcp-04-6c7101c1dba1`), Cloud Run revision (e.g. `food-broker-00007-4sm`), and live URL (`https://food-broker-817377390808.us-east1.run.app/dev-ui/`).
4. **Tests & Verification Evidence:** Link the automated test (`agent/food_broker/selfcheck.py`) and captured live output in `docs/evidence/`.
5. **What Is NOT Tested / Built Yet:** Explicitly separate HTTP/CLI verification from unverified browser UI walkthroughs, unbuilt slides, or unrecorded video.

When a teammate picks up an issue:

```bash
gh issue edit <num> --repo jimmycgz/challenge2-117 \
  --remove-label "assignee: unassigned" \
  --add-label "owner: <github-handle>" \
  --add-assignee "<github-handle>"
```

When code lands on `origin/main` or when a Cloud Run revision is deployed:

1. Fetch latest commits: `git fetch --all`
2. Check off completed `[x]` acceptance criteria in the issue body via `gh issue edit <num> --repo jimmycgz/challenge2-117 --body ...`
3. Transition labels if pickup state changed:

   ```bash
   gh issue edit <num> --repo jimmycgz/challenge2-117 \
     --remove-label "needs-pickup,status: in-progress" \
     --add-label "no-pickup-needed,status: done"
   ```

---

## Live Environment & Pre-Submission Verification

1. **Verify Active GCP Project & Credentials:**
   * Project ID: `qwiklabs-gcp-04-6c7101c1dba1` (Project Number: `817377390808`)
   * BigQuery Dataset: `a4i_food` (`recipients`=192 rows: 183 real organizations plus nine invented teaching cases with `profile_source` = `'planted'`; `recipient_embeddings`=192, `shelf_life`=661, `surplus_postings`=10, `tract_demographics`=1004)
   * Cloud Run Service (`us-east1`): `https://food-broker-817377390808.us-east1.run.app/dev-ui/`
2. **Run Offline Self-Check (When on agent branch or after PR #1 merge):**

   ```bash
   PYTHONPATH=agent python3 -m food_broker.selfcheck
   ```

3. **Final Submission Sequence (Before 16:00 Freeze):**
   * Merge PR #1 (`feature/food-broker-agent`) into `main`.
   * Tag the release commit on `main`:

     ```bash
     git checkout main && git pull origin main
     git tag submission && git push origin submission
     ```

   * Verify all 4 items in [deliverables_rubric.md](./references/deliverables_rubric.md) are uploaded to `https://portal.angelhack.com/a4i-console`.
