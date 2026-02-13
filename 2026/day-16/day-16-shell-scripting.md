# TASK-1(Script code)
-#!/bin/bash
-echo "Hello , Devops!"

# OUTPUT 
Hello , Devops!

# TASK-2(Script)
- #!/bin/bash
-read -p  "Type your name:" name
-read -p "Type your role:" role
-echo "Hello my name is $name and my role is is $role"

# OUTPUT
-Type your name:uttam
-Type your role:teacher
-Hello my name is uttam and my role is is teacher

# TASK-3(Script)
-#!/bin/bash
-read -p  "Type your name:" name
-read -p "Type your fav. tool:" tool
-echo "Hello my name is $name and my favourite tool is $tool"

# OUTPUT
-Type your name:uttam
-Type your fav. tool:docker
-Hello my name is uttam and my favourite tool is docker

# TASK-4(Script)
-#!/bin/bash
-read -p "Enter your number:" a
-if [ $a -gt 0 ];then
-        echo "Given number is positive"
-elif [ $a -eq 0 ];then
-        echo "Given number is is exactly zero"
-else
-        echo "Given number is negative"
fi

# OUTPUT

-Enter your number:0
-Given number is is exactly zero

# TASK-5(Script)
-#!/bin/bash

-read -p "Enter service name:" service_name
-read -p "Do you want to check service status(y/n)"
-if [ y ];then
-        echo "service is active"
-        systemctl status $service_name
-else
-        echo "SKipped"
-fi

# OUTPUT

-Enter service name:nginx
-Do you want to check service status(y/n)y
-service is active
-● nginx.service - A high performance web server and a reverse proxy server
-     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: enable>
-     Active: active (running) since Fri 2026-02-13 07:09:53 UTC; 4h 38min ago
-       Docs: man:nginx(8)
-   Main PID: 1708 (nginx)
-      Tasks: 5 (limit: 2131)
-     Memory: 3.7M (peak: 8.3M)
-        CPU: 96ms
-     CGroup: /system.slice/nginx.service
-             ├─1708 "nginx: master process /usr/sbin/nginx -g daemon on; master_pro>
-             ├─1711 "nginx: worker process"
-             ├─1712 "nginx: worker process"
-             ├─1713 "nginx: worker process"
-
-              └─1714 "nginx: worker process"

