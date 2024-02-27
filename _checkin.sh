#!/bin/bash
if [[ $# < 1 ]]; then
  echo "Add quoted comment for commit."
  exit -1
fi
gitleaks > .gitleaks 2>&1
rm onboard_client/logs/* > /dev/null 2>\&1
rm -rf onboard_client/lib/__pycache__ > /dev/null 2>\&1
rm onboard_server/logs/* > /dev/null 2>\&1
rm -rf onboard_server/lib/__pycache__ > /dev/null 2>\&1
branch_name=$(git rev-parse --abbrev-ref HEAD)
echo
echo "Committing changes to current branch ($branch_name) with comment:"
echo "  $1"
echo
echo "Press <enter> to continue, <ctrl>-C to exit..."
read foo

git add .
git commit -m "$1"
git push origin $branch_name
