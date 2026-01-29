# Outcome of ps
ps
    PID TTY          TIME CMD
   1181 pts/1    00:00:00 sudo
   1182 pts/1    00:00:00 su
   1183 pts/1    00:00:00 bash
   1688 pts/1    00:00:00 ps

# Output of top
1 root      20   0   22496  13704   9480 S   0.0   1.4   0:01.55
      2 root      20   0       0      0      0 S   0.0   0.0   0:00.00
      3 root      20   0       0      0      0 S   0.0   0.0   0:00.00
      4 root       0 -20       0      0      0 I   0.0   0.0   0:00.00
      5 root       0 -20       0      0      0 I   0.0   0.0   0:00.00
      6 root       0 -20       0      0      0 I   0.0   0.0   0:00.00

# Outcome of systemctl status
systemctl status  1180
● session-2.scope - Session 2 of User ubuntu
     Loaded: loaded (/run/systemd/transient/session-2.scope; transient)
  Transient: yes
     Active: active (running) since Thu 2026-01-29 06:37:11 UTC; 36min ago
      Tasks: 9
     Memory: 93.7M (peak: 136.4M)
        CPU: 5.584s
     CGroup: /user.slice/user-1000.slice/session-2.scope
             ├─ 875 "sshd: ubuntu [priv]"
             ├─ 990 "sshd: ubuntu@pts/0"
             ├─1027 -bash
             ├─1180 sudo su
             ├─1181 sudo su
             ├─1182 su
             ├─1183 bash
             ├─1798 systemctl status 1180
             └─1799 less
             
# Outcome of tail
tail -5 file
ssh ..
touch
vi
vim
nano

# Outcome of crontab -l
crontab -l
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command

0 3 * * *



17 13 * * 4 echo "Weekend soon!" | mail -s "Reminder" gzeus5476@gmail.com

# Outcome of journalctl
journalctl -u google.com
-- No entries --
