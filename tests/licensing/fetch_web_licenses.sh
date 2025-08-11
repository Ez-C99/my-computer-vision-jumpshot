set -euo pipefail
mkdir -p third_party/licenses
# If you have a web viewer subfolder with package.json:
( cd webviewer && npx --yes license-checker --summary > ../third_party/licenses/npm-licenses.txt )
# Optional: generate a TPN aligned to your production bundle:
# npx --yes @rnx-kit/third-party-notices --output ../third_party/licenses/THIRD-PARTY-NOTICES.web.txt
