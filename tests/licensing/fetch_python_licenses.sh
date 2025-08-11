set -euo pipefail
mkdir -p third_party/licenses
pip install -q pip-licenses
pip-licenses --from=mixed \
  --with-urls --with-authors --with-license-file --with-notice-file \
  --format=json --no-license-path \
  --output-file third_party/licenses/pip-licenses.json
pip-licenses --from=mixed --format=markdown \
  --output-file LICENSES.generated.md
echo "Wrote third_party/licenses/pip-licenses.json and LICENSES.generated.md"
