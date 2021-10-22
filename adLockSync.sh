#!/usr/bin/env bash
cd /opt/zimbra-adlock-sync
source bin/activate
python3 AdLockSync.py
sleep 2
zmprov -f ADLockedAccounts.txt