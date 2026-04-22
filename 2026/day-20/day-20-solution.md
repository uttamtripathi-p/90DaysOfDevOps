#########

####### MY BASH SCRIPT FOR LOG ANALYSER AND SAMPLE REPORT

#!/bin/bash
set -euo pipefail
TIMESTAMP=$(date '+%Y-%m-%y-%H-%M-%S')
error_check() {
if [ $# -eq 0 ]; then
        echo "NO ARGUMENTS PROVIDED" >&2
        echo "USAGE: $0 <path to a log file>" >&2
        exit 1
fi


LOG_FILE="$1"
TOTAL_LINES=$(wc -l < "$LOG_FILE")


if [ ! -f "$LOG_FILE" ]; then
      echo "Error: FILE does not exist: $LOG_FILE" >&2
      exit 1
fi
        echo "Logs found"
}
error_check "$@"

error_count() {
        awk '/DEBUG/ { print NR $0 }' $LOG_FILE
}


critical_events() {
        CRITICAL=$(awk '/CRITICAL/ { print NR,$0 }' $LOG_FILE)
        if [ $? -eq 0 ]; then
                echo "--------------CRITICAL EVENTS------------------"
                echo "$CRITICAL"
        fi
}



top_error() {
        GREP=$(grep "ERROR" $LOG_FILE | awk '{$1=$2=$3=""; print}' | sort | uniq -c | sort -rn | head -2)
echo "---------------TOP 2 ERROR MESSAGES-------------------"
echo "$GREP"
}

Summary_report() {
        echo "TIMESTAMP: $TIMESTAMP"
        echo "$LOG_FILE"
        echo "Total lines processed: $TOTAL_LINES"
        error_count
        top_error
        echo "----------TOP 2 ERROR MESSAGES COUNT------------"
        top_error | wc -l
        critical_events


} >> "log_report_${LOG_FILE}_${TIMESTAMP}.txt"
Summary_report
