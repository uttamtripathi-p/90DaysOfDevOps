# for_loop.sh

#!/bin/bash

# Define an array of 5 fruits
fruits=("Apple" "Banana" "Orange" "Grape" "Mango")

# Loop through each fruit in the array
for fruit in "${fruits[@]}"; do
  echo "Fruit: $fruit"
done

# count.sh

#!/bin/bash

for i in {1..10};
do
echo "$i"
done

# countdown.sh

read -p "Enter a number:" number

while [  $number -ge 0 ]; do
        echo "Number is $number"
        ((number--))
done

# greet.sh 

#!/bin/bash


echo "Hello,$1"

# args_demo.sh

#!/bin/bash

echo "$#"
echo "$@"
echo "$0"

# install_packages.sh

#!/bin/bash

PACKAGES=("nginx" "curl" "wget")
echo "Updating package lists.."
sudo apt-get update -qq

for PKG in "${PACKAGES[@]}"; do

        if dpkg -s "$PKG" >/dev/null 2>&1; then
                echo "[SKIP] $PKG is already installed"
        else
                echo "[MISSING] $PKG is not installed.Installing now.."

                if sudo apt-get install -y "$PKG" >/dev/null 2>&1; then
                        echo "[SUCCESS] $PKG has been installed"
                else
                        echo "[ERROE] failed to install $PKG ."
                fi
        fi
done

# safe_script.sh

#!/bin/bash


set -e

mkdir -p /tmp/devops-test || echo "Directory already exists"
cd /tmp/devops-test
echo "I'm in $(pwd)"
touch empty.text
exit


