# TO CREATE LOG ROTATION

#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <log_directory>"
    exit 1
fi

LOG_DIR="$1"

[ -d "$LOG_DIR" ] || { echo "Error: Directory does not exist."; exit 1; }

# Count & compress .log files older than 7 days
compressed=$(find "$LOG_DIR" -type f -name "*.log" -mtime +7 -exec gzip {} \; -printf '.' | wc -c)

# Count & delete .gz files older than 30 days
deleted=$(find "$LOG_DIR" -type f -name "*.gz" -mtime +30 -delete -printf '.' | wc -c)

echo "Compressed $compressed file(s)."
echo "Deleted $deleted old compressed file(s)."




# TO CREATE SERVER BACKUP SCRIPT

#!/bin/bash
set -euo pipefail

<< readme
This is a script for backup
Usage:
./backup.sh <Path to your source> <Path to backup folder>
readme


display_usage() {
        echo "Usage:
./backup.sh <Path to your source> <Path to backup folder>
"
}

if [ $# -eq 0 ]; then
        display_usage
fi

source_dir=$1
timestamp=$(date '+%Y-%m-%d-%H-%M-%S')
backup_dir=$2

create_backup() {
        zip -r "${backup_dir}/backup_${timestamp}.zip" "${source_dir}" >/dev/null
        if [ $? -eq 0 ]; then
        echo "Backup generated successfully for ${timestamp}"
        echo "BACKUP_FILE_NAME======${backup_dir}/backup_${timestamp}.zip"
        fi
}
create_backup

create_delete() {
        # Count & delete .gz files older than 30 days
deleted=$(find "$backup_dir" -type f -name "*.zip" -mtime +14 -delete -printf '.' | wc -c)
}
create_delete  


# CRON_JOB

0 2 * * * /home/dell-2004/bash_scripts/log_rotate2.sh >> /home/dell-2004/cron.log 2>&1
0 3 * * 7 /home/dell-2004/bash_scripts/backup.sh >> /home/dell-2004/cron.log 2>&1


# MAINTENANCE.SH


#!/bin/bash


maintenance() {
        date=$(date '+%Y-%m-%y-%H-%M-%S')
        echo "$dt"

        source ./backup.sh /home/dell-2004/bash_scripts /home/dell-2004/backups

        if [ $? -eq 0 ]; then
                echo "backup taken"
        else
                echo "backup failed"
        fi


        source ./log_rotate2.sh /home/dell-2004/log_practise

        if [ $? -eq 0 ]; then
                echo "log move successfully"
        else
                echo "logfiles didn't move"
        fi
} >> /var/log/maintenance.log

maintenance

## cat /var/log/maintenance.log

Backup generated successfully for 2026-02-23-17-01-42
BACKUP_FILE_NAME======/home/dell-2004/backups/backup_2026-02-23-17-01-42.zip
backup taken
Compressed 0 file(s).
Deleted 0 old compressed file(s).
log move successfully

