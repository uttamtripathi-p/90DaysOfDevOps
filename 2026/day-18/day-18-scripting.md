## function.sh for greeting user and printing sum of two numbers
#!/bin/bash

greet_user () {
        read -p "Enter a number:" a
        read -p "Enter another number:" b
        sum=$((a + b))
        echo "Hello $1! "
        echo "Sum of the numbers is : $sum"
}
greet_user "$1"

## disk_check.sh

#!/bin/bash


check_disk() {
        echo "====== Root disk usage ====="
        df -h /
        echo
}

check_memory() {
        echo "===== Memory usage ====="
        free -h
        echo
}


check_disk
check_memory


## strict_demo.sh

#!/bin/bash


set -euo pipefail
read -p "Input which function to call (1/2/3): " input

undefined_variable ()
{
        echo "hello learners"
        echo "hope you are doing $well"
}
command_failure ()
{
        echo "The given command is"
        ls /etrin
}
pipe_failure ()
{
        cat "PIPE" | awk #23
        echo "The piefail has occured beacuse a part of script has failed"
}

if [ $input == 1 ]
then
        undefined_variable
        echo "Done"
elif [ $input == 2 ]
then
        command_failure
        echo "Donw"
elif [ $input == 3 ]
then
        pipe_failure
        echo "Done"
fi

# local_demo.sh

#!/bin/bash


local_variable_store () {
        local x=10
        echo "Local variable value inside function is : $x"
}
global_variable_store () {
        y=20
        echo "Value of global variable inside function is : $y"
}
local_variable_store
echo "Value of local variable outside function is : $x"
echo "===========LOCAL VARIABLE CAN'T BE ACCESSED OUTSIDE FUNCTION======================"
global_variable_store
echo "Value of global variable outside function is : $y"

# system_info.sh

#!/bin/bash


set -euo pipefail

hostname_info () {
        cat /etc/os-release
        hostname
}
uptime () {
        /usr/bin/uptime -p
}
disk_usage () {
        df -h | sort -h | head -n 6
}
memory_usage () {
        free -h
}
cpu_cons_proc () {
        ps aux --sort=-%cpu | head -n 6
}
main_function () {
        echo " ========== Hostname and OS info are ============================"
        hostname_info
echo "=============== Uptime of the system is ======================="
uptime
echo "==================TOP 5 DISK USAGES ==================="
disk_usage
echo "================== MEMORY USAGE ==================="
memory_usage
echo "=========================== TOP 5 CPU CONSUMING PROCESSES ======================="
cpu_cons_proc
}
main_function



