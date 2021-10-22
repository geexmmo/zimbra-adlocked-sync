# About:
Script generates a list of emails from all disabled users in Active Directory.

Locked user are being searched by `userAccountControl=514` field, meaning that search will hit only those who was manually blocked by AD administrators and those whose accounts are expired, users who was temporary blocked by exceeding their login attempt limits are ignored.

Script generates file `ADLockedAccounts.txt`, it contains `zmprov` commands that can be used to change status of Zimbra mail accounts to 'closed' or something, leaving emails stored in those accounts intact.

# Running:

* Clone this repo

* Create venv to install dependencies, can be ignored if dependencies is going to be install system-wide   
`python3 -m venv ./zimbra-adlock-sync`
* Activate environment:   
`source bin/activate`
* Install requirements:   
`pip install -r requirements.txt`
* Edit settings in `settings.py` according to your system and Active Directory setup
* Run script   
`python3 AdLockSync.py`   
* * File `ADLockedAccounts.txt` should be generated and populated with `ma $mail zimbraAccountStatus closed` commands.
* * This file should be reviewed on first runs to make sure nothing critical will be blocked (some users for some weirdest reasons may have multiple AD accounts with similar emails and some of their accounts may be disabled - resulting in this emails being included in the generated list)

* Run zmprov to apply changes to account in list   
`zmprof -f ADLockedAccounts.txt`


# Cronjob
To automate this process a cron job could be started.

* Make simple bash script to activate environment and run all commands:   
```
#!/usr/bin/env bash
cd /opt/zimbra-adlock-sync
source bin/activate
python3 sync.py
sleep 2
zmprov -f ADLockedAccounts.txt
```

* Make sure the script can be executed and add it to crontab:   
`chmod +x /opt/zimbra-adlock-sync/adLockSync.sh`