# du -sh /var/log 2>/dev/null | sort -n | tail -n 5
132M    /var/log

#  journalctl -u nginx | tail -n 1
Feb 03 09:28:05 ip-172-31-21-199 systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.

# cat /etc/hostname
ip-172-31-21-199

# systemctl is-enabled nginx
enabled

# systemctl list-unit-files | tail -3
xfs_scrub_all.timer                            disabled        enabled

410 unit files listed.

#  ps aux --sort=-%cpu | head -3
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.3  1.3  22092 13420 ?        Ss   :27   0:04 /sbin/init
ubuntu      1335  0.2  0.7  14996  7140 ?        S    09:31   0:01 sshd: ubuntu@pts/0

