#!/bin/bash

# package.json
echo "Checking package.json..."
repo_ver=$(curl -s https://raw.githubusercontent.com/misskey-dev/misskey/develop/package.json | grep version | awk -F \" '{print $4}')
echo "-> $repo_ver"

echo

# api/meta
echo "Checking api/meta..."
ins_ver=$(curl -s -X POST https://stella.ocellaris.dev/api/meta | awk -F \" '{print $12}')
echo "-> $ins_ver"

echo

if [ "$ins_ver" = "$repo_ver" ]; then
    echo "-> Misskey is up-to-date!"
    bash /home/caipira113/cron.sh &
    gh workflow run merge-upstream.yml -R ocellaris-dev/stella
    sudo service cron start
    exit 0
else
    echo "-> New version detected."
    exit 0
fi