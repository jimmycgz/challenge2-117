#!/usr/bin/env bash
#
# Complete virtual environment setup for the Food Broker Agent (strictly within agent/).
# Works on Linux, macOS, and Windows (Git Bash, MSYS2, and WSL on Windows drives).
# Creates agent/.venv, installs agent/requirements.txt, runs the offline self-check,
# and prints instructions for starting the agent.
#
# Usage:
#   cd agent && bash setup.sh
#   (or from repo root: bash agent/setup.sh)

set -euo pipefail

AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${AGENT_DIR}"

VENV_NAME="${VENV_DIR:-.venv}"
REQ_FILE="requirements.txt"

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
bold() { printf '\033[1m%s\033[0m\n' "$*"; }
info() { printf '  %s\n' "$*"; }
fail() { printf '\n\033[1;31mERROR:\033[0m %s\n\n' "$*" >&2; exit 1; }

bold "=== Food Broker Agent - Environment Setup (agent/) ==="
echo

# --------------------------------------------------------------------------
# 1. Locate Python interpreter (prefer Python 3.12+, Windows-aware)
# --------------------------------------------------------------------------
bold "1/4  Locating Python interpreter"
PYTHON_BIN="${PYTHON:-}"

# Detect if running on Windows (Git Bash / MSYS / Cygwin, or WSL on a mounted Windows drive /mnt/*)
IS_WINDOWS_ENV=0
case "${OSTYPE:-}" in
  msys*|cygwin*|win32*) IS_WINDOWS_ENV=1 ;;
esac
if [[ "${IS_WINDOWS_ENV}" -eq 0 ]] && grep -qi "microsoft" /proc/version 2>/dev/null && [[ "${AGENT_DIR}" == /mnt/* ]]; then
  IS_WINDOWS_ENV=1
fi

if [[ -z "${PYTHON_BIN}" ]]; then
  if [[ "${IS_WINDOWS_ENV}" -eq 1 ]]; then
    CANDIDATES=(python.exe python python3.12 python3)
  else
    CANDIDATES=(python3.12 python3 python python.exe)
  fi

  for candidate in "${CANDIDATES[@]}"; do
    if command -v "${candidate}" >/dev/null 2>&1; then
      if "${candidate}" -c "import sys, venv, ensurepip; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >/dev/null 2>&1; then
        PYTHON_BIN="${candidate}"
        break
      fi
    fi
  done
fi

[[ -n "${PYTHON_BIN}" ]] || fail "Python 3.10+ with venv/ensurepip not found. Install Python 3.12 and re-run."

PY_VERSION="$("${PYTHON_BIN}" --version 2>&1 | tr -d '\r')"
info "Using Python: ${PYTHON_BIN} (${PY_VERSION})"
echo

# --------------------------------------------------------------------------
# 2. Create virtual environment inside agent/.venv
# --------------------------------------------------------------------------
bold "2/4  Creating virtual environment at ${AGENT_DIR}/${VENV_NAME}"
if [[ -f "${VENV_NAME}/Scripts/python.exe" || -x "${VENV_NAME}/bin/python" ]]; then
  info "Existing virtual environment found at ${VENV_NAME} - reusing it"
else
  rm -rf "${VENV_NAME}"
  "${PYTHON_BIN}" -m venv "${VENV_NAME}"
  info "Created virtual environment at ${VENV_NAME}"
fi

# Resolve venv binaries across Windows (Scripts/) and Unix (bin/)
if [[ -f "${VENV_NAME}/Scripts/python.exe" ]]; then
  VENV_PY="${VENV_NAME}/Scripts/python.exe"
  IS_WIN_VENV=1
elif [[ -x "${VENV_NAME}/bin/python" ]]; then
  VENV_PY="${VENV_NAME}/bin/python"
  IS_WIN_VENV=0
else
  fail "Could not locate python executable inside ${VENV_NAME}"
fi
echo

# --------------------------------------------------------------------------
# 3. Install dependencies from agent/requirements.txt
# --------------------------------------------------------------------------
bold "3/4  Installing dependencies from requirements.txt"
[[ -f "${REQ_FILE}" ]] || fail "Requirements file not found at ${AGENT_DIR}/${REQ_FILE}"

"${VENV_PY}" -m pip install --upgrade pip --quiet
"${VENV_PY}" -m pip install -r "${REQ_FILE}"
info "Dependencies installed successfully"
echo

# --------------------------------------------------------------------------
# 4. Run offline self-check from agent/
# --------------------------------------------------------------------------
bold "4/4  Running offline agent self-check (food_broker.selfcheck)"
"${VENV_PY}" -m food_broker.selfcheck
info "Offline self-check passed!"
echo

# --------------------------------------------------------------------------
# Print instructions to start the agent
# --------------------------------------------------------------------------
GCLOUD_CMD=""
for gc in gcloud gcloud.cmd; do
  if command -v "${gc}" >/dev/null 2>&1; then
    GCLOUD_CMD="${gc}"
    break
  fi
done

DETECTED_PROJECT=""
DETECTED_ACCOUNT=""
if [[ -n "${GCLOUD_CMD}" ]]; then
  DETECTED_PROJECT="$("${GCLOUD_CMD}" config get-value project 2>/dev/null | tr -d '\r' || true)"
  DETECTED_ACCOUNT="$("${GCLOUD_CMD}" config get-value account 2>/dev/null | tr -d '\r' || true)"
fi

if [[ -z "${DETECTED_PROJECT}" || "${DETECTED_PROJECT}" == "(unset)" ]]; then
  DETECTED_PROJECT="<your-gcp-project-id>"
fi

if [[ -n "${DETECTED_ACCOUNT}" && "${DETECTED_ACCOUNT}" == *"@"* ]]; then
  DETECTED_SUFFIX="@${DETECTED_ACCOUNT#*@}"
else
  DETECTED_SUFFIX="@<your-account-domain>"
fi

bold "=================================================================="
bold "Setup complete! Follow the steps below to start the Food Broker Agent"
bold "=================================================================="

if [[ "${IS_WIN_VENV}" -eq 1 ]]; then
cat <<EOF

[Option 1: Windows PowerShell]
1. Move into the agent directory and activate the virtual environment:
   cd agent
   .\.venv\Scripts\Activate.ps1

2. Set the required environment variables (Identity Guard & Vertex AI):
   \$env:GOOGLE_CLOUD_PROJECT="${DETECTED_PROJECT}"
   \$env:A4I_EXPECTED_PROJECT="${DETECTED_PROJECT}"
   \$env:A4I_EXPECTED_PRINCIPAL_SUFFIX="${DETECTED_SUFFIX}"
   \$env:GOOGLE_GENAI_USE_VERTEXAI="1"
   \$env:GOOGLE_CLOUD_LOCATION="us-central1"
   \$env:A4I_MCP="1"   # Optional: enables Google's managed BigQuery MCP toolset

3. Start the agent locally (from inside 'agent/'):
   adk api_server --with_ui --port 8765 .
   # Then open: http://127.0.0.1:8765/dev-ui/

------------------------------------------------------------------
[Option 2: Git Bash / Bash on Windows]
1. Move into the agent directory and activate the virtual environment:
   cd agent
   source .venv/Scripts/activate

2. Set the required environment variables (Identity Guard & Vertex AI):
   export GOOGLE_CLOUD_PROJECT="${DETECTED_PROJECT}"
   export A4I_EXPECTED_PROJECT="${DETECTED_PROJECT}"
   export A4I_EXPECTED_PRINCIPAL_SUFFIX="${DETECTED_SUFFIX}"
   export GOOGLE_GENAI_USE_VERTEXAI=1
   export GOOGLE_CLOUD_LOCATION="us-central1"
   export A4I_MCP=1   # Optional: enables Google's managed BigQuery MCP toolset

3. Start the agent locally (from inside 'agent/'):
   adk api_server --with_ui --port 8765 .
   # Then open: http://127.0.0.1:8765/dev-ui/

EOF
else
cat <<EOF

1. Move into the agent directory and activate the virtual environment:
   cd "${AGENT_DIR}"
   source .venv/bin/activate

2. Set the required environment variables (Identity Guard & Vertex AI):
   export GOOGLE_CLOUD_PROJECT="${DETECTED_PROJECT}"
   export A4I_EXPECTED_PROJECT="${DETECTED_PROJECT}"
   export A4I_EXPECTED_PRINCIPAL_SUFFIX="${DETECTED_SUFFIX}"
   export GOOGLE_GENAI_USE_VERTEXAI=1
   export GOOGLE_CLOUD_LOCATION="us-central1"
   export A4I_MCP=1   # Optional: enables Google's managed BigQuery MCP toolset

3. Start the agent locally (from inside 'agent/'):
   # Option A: Start ADK API Server + Web Dev UI (recommended for browser testing)
   adk api_server --with_ui --port 8765 .
   # Then open: http://127.0.0.1:8765/dev-ui/

   # Option B: Start ADK API Server only
   adk api_server --port 8765 .

   # Option C: Run interactive CLI session
   adk run food_broker

EOF
fi

cat <<EOF
4. Other useful commands (from inside 'agent/'):
   python -m food_broker.selfcheck     # Offline unit & guard verification (no credentials needed)
   python -m food_broker.demo_tracks   # Run one posting per track against BigQuery tables
   bash deploy.sh                      # Deploy the agent to Google Cloud Run

EOF
