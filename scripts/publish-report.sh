#!/usr/bin/env bash
# Publish one pytest-html report to the gh-pages branch and keep the last N days.
# Run by the `pages` job in .github/workflows/ci.yml, from a checkout of this repo (actions/checkout keeps
# the GITHUB_TOKEN in git's config, so no token ever appears in a URL or the log).
#
#   scripts/publish-report.sh <report.html> [keep_days]
#
# Layout on gh-pages:  reports/<YYYY-MM-DD>/run-<n>/index.html  + an index.html listing them.
# Each publish replaces gh-pages with ONE orphan commit: old reports are kept as files, not as git history,
# so the branch never grows. The job's `concurrency` group queues publishes, so two runs can't overwrite each other.
set -euo pipefail

REPORT=$1
KEEP_DAYS=${2:-7}
RUN="run-${GITHUB_RUN_NUMBER:?}"
TODAY=$(TZ=Asia/Taipei date +%F)
CUTOFF=$(TZ=Asia/Taipei date -d "-$KEEP_DAYS days" +%F)

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

# Start an empty orphan branch, then bring back the files of the current gh-pages (if it exists yet).
git checkout -q --orphan gh-pages-new
git rm -rq --cached . && git clean -fdxq
if git fetch -q --depth 1 origin gh-pages 2>/dev/null; then  # first publish: no gh-pages yet
  git checkout -q FETCH_HEAD -- .
fi

# Add this run's report.
mkdir -p "reports/$TODAY/$RUN"
cp "$REPORT" "reports/$TODAY/$RUN/index.html"

# Keep the last KEEP_DAYS days (folder names are dates, so string comparison works).
for dir in reports/*/; do
  day=$(basename "$dir")
  if [[ "$day" < "$CUTOFF" ]]; then
    rm -rf "$dir"
    echo "removed $day"
  fi
done

# Index page: newest first. Names are only dates and run numbers we generate, so nothing to escape.
{
  echo '<!doctype html><meta charset="utf-8"><title>device-lab test reports</title>'
  echo '<style>body{font-family:system-ui,sans-serif;max-width:640px;margin:40px auto;padding:0 16px}li{margin:4px 0}</style>'
  echo "<h1>device-lab test reports</h1><p>Last $KEEP_DAYS days, main branch only. Times are Asia/Taipei.</p>"
  for day in $(ls -r reports); do
    echo "<h2>$day</h2><ul>"
    for run in $(ls reports/"$day" | sort -t- -k2 -nr); do
      echo "<li><a href=\"reports/$day/$run/\">$run</a></li>"
    done
    echo "</ul>"
  done
} > index.html
touch .nojekyll # serve files as-is, no Jekyll processing

git add -A
git commit -qm "report: $TODAY $RUN"
git push -q --force origin HEAD:gh-pages
echo "url=https://${GITHUB_REPOSITORY_OWNER}.github.io/${GITHUB_REPOSITORY#*/}/reports/$TODAY/$RUN/" >> "$GITHUB_OUTPUT"
