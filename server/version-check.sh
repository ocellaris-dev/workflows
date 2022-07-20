#!/bin/bash

echo

#current time
tdc1=$(timedatectl | grep "Local time" | awk '{print $1, $2, $3, $4, $5}')
tdc2=$(timedatectl | grep "Universal time" | awk '{print $1, $2, $3, $4, $5}')
tdc3=$(timedatectl | grep "RTC time" | awk '{print $1, $2, $3, $4, $5}')
tdc4=$(timedatectl | grep "Time zone" | awk '{print $1, $2, $3, $4, $5}')
echo "$tdc1"
echo "$tdc2"
echo "$tdc3"
echo "$tdc4"

echo

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
    exit 0
else
    echo "-> New version detected."
    bash /home/caipira113/cron.sh &
    gh workflow run merge-upstream.yml -f docker=true -R ocellaris-dev/stella
    exit 0
fi