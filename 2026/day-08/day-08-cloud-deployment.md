# LIST OF COMMANDS THAT I USED

   1  ls
    2  systemctl is-enabled nginx
    3  sudo apt-get install nginx
    4  systemctl is-enabled nginx
    5  systemctl status nginx
    6  cat /etc/hostname
    7  scp -i downloads/nginx.pem ubuntu@54.87.49.42:~/nginx-logs.txt .
    8  sudo scp -i downloads/nginx.pem ubuntu@54.87.49.42:~/nginx-logs.txt .
    9  scp -i nginx.pem ubuntu@54.87.49.42:~/nginx-logs.txt . 
   11  systemctl is-enabled nginx 
   15  history
    427  scp -i downloads/nginx.pem ubuntu@52.91.197.11:~/nginx-logs.txt .
  428  chmod 600 downloads/nginx.pem
  429  scp -i downloads/nginx.pem ubuntu@52.91.197.11:~/nginx-logs.txt .
  430  ls -l downloads/nginx.pem
  431  sudo chmod 600 downloads/nginx.pem
  432  ls -l downloads/nginx.pem
  433  sudo chmod 600 downloads/nginx.pem
  434  ls -l downloads/nginx.pem
  435  mv downloads/nginx.pem nginxx.pem
  436  ls
  437  ls nginx.pem
  438  cat nginxx.pem
  439  ls -l
  440  sudo chmod 600 nginxx.pem
  441  ls -l
  442  cd ~
  443  ls
  444  mkdir -p ~/.ssh
  445  ls
  446  ls -l
  447  ls -a
  448  cp /mnt/c/Users/dell/downloads/nginx.pem ~/.ssh/nginx.pem
  449  cp /mnt/c/Users/dell/Downloads/nginx.pem ~/.ssh/nginx.pem
  450  cd /mnt/c/Users/dell
  451  ls
  452  cp /mnt/c/Users/dell/nginxx.pem ~/.ssh/nginx.pem
  453  cd ~
  454  ls
  455  ls -l ~/.ssh/nginxx.pem
  456  sudo ls -l ~/.ssh/nginxx.pem
  457  cd .ssh
  458  ls
  459  cd ..
  460  ls
  461  ls -l ~/.ssh/nginx.pem
  462  chmod 600 ~/.ssh/nginx.pem
  463  ls -l ~/.ssh/nginx.pem
  464  scp -i ~/.ssh/nginx.pem ubuntu@52.91.197.11:/var/log/nginx/access.log .
  465  ls
  466  cat access.log



# PROBLEM THAT I FACED WAS THAT I WAS RUNNING THAT (scp) COMMAND FROM MY SSH INSTANCE RATHER THAN MY LOCAL MACHINE SO IT TOOK ME A LOT OF TIME BUT NOW IT'S CLEAR

# WHAT I LEARNED
I learned how to copy log files from another server.

