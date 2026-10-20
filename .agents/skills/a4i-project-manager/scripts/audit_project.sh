#!/usr/bin/env bash
set -euo pipefail

REPO="jimmycgz/challenge2-117"
PROJECT_ID="qwiklabs-gcp-04-6c7101c1dba1"
SERVICE_URL="https://food-broker-817377390808.us-east1.run.app"

echo "======================================================================"
echo "  CHICAGO FOOD RESCUE BROKER — PROJECT & DELIVERABLES AUDIT"
echo "======================================================================"

echo ""
echo "[1/5] GIT & PULL REQUEST STATUS"
git fetch --all --quiet || true
echo "  Current branch : $(git rev-parse --abbrev-ref HEAD)"
echo "  main HEAD      : $(git log -1 --oneline origin/main 2>/dev/null || echo 'unknown')"
echo "  agent PR HEAD  : $(git log -1 --oneline origin/feature/food-broker-agent 2>/dev/null || echo 'merged/none')"
echo "  submission tag : $(git tag -l submission)"
gh pr list --repo "$REPO" --state all

echo ""
echo "[2/5] GITHUB ISSUES BY PICKUP STATUS"
echo "--- 🔴 NEEDS PICKUP (Action Required Now) ---"
gh issue list --repo "$REPO" --label "needs-pickup" --json number,title,assignees,labels \
  --jq '.[] | "  #\(.number) [\([.assignees[].login] | join(","))] \(.title)"'

echo ""
echo "--- 🟡 OPTIONAL PICKUP (Browser Check or Stretch Goal) ---"
gh issue list --repo "$REPO" --label "optional-pickup" --json number,title,assignees,labels \
  --jq '.[] | "  #\(.number) [\([.assignees[].login] | join(","))] \(.title)"'

echo ""
echo "--- 🟢 NO PICKUP NEEDED (Done / Reference) ---"
gh issue list --repo "$REPO" --label "no-pickup-needed" --json number,title,assignees,labels \
  --jq '.[] | "  #\(.number) [\([.assignees[].login] | join(","))] \(.title)"'

echo ""
echo "[3/5] LIVE CLOUD RUN SERVICE ($SERVICE_URL)"
HTTP_APPS=$(curl -s --max-time 5 "$SERVICE_URL/list-apps" || echo "UNREACHABLE")
echo "  GET /list-apps : $HTTP_APPS"
gcloud run revisions list --service=food-broker --region=us-east1 --project="$PROJECT_ID" --limit=3 2>/dev/null || true

echo ""
echo "[4/5] BIGQUERY DATASET ($PROJECT_ID:a4i_food)"
bq ls --project_id="$PROJECT_ID" a4i_food 2>/dev/null || echo "  (Run gcloud config set project $PROJECT_ID to inspect BQ)"

echo ""
echo "[5/5] DELIVERABLES CHECKLIST"
for path in \
  "docs/DECK-OUTLINE.md" \
  "docs/DEMO-SCRIPT.md" \
  "docs/SUBMISSION.md" \
  "agent/food_broker/EQUITY-AUDIT.md" \
  "docs/evidence/spinach-answer.md" \
  "docs/evidence/sealed-formula-answer.md" \
  "docs/evidence/mcp-walk-in-answer.md" \
  "docs/evidence/follow-ups-transcript.md"; do
  if git cat-file -e "origin/feature/food-broker-agent:$path" 2>/dev/null || [ -f "$path" ]; then
    echo "  [x] $path (Present)"
  else
    echo "  [ ] $path (MISSING)"
  fi
done
echo "======================================================================"
