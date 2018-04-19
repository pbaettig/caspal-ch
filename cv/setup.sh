#!/bin/bash
USERNAME=anon

apt-get update && apt-get upgrade
apt-get install python python-pip

adduser --disabled-password --home /home/${USERNAME} --shell /home/${USERNAME}/print_cv.py --quiet --gecos ""  ${USERNAME}
sed -i -re "s/^${USERNAME}:[^:]+:/${USERNAME}::/" /etc/passwd /etc/shadow
aws s3 sync s3://caspal-bootstrap/cv/ /tmp/cv
cp config/sshd_config /etc/ssh/sshd_config
cp config/pam.d-sshd /etc/pam.d/sshd
rm /etc/motd
rm /etc/update-motd.d/10-uname

cp scripts/*.py /home/${USERNAME}
chmod a+x /home/${USERNAME}/print_cv.py

pip install prettytable

shutdown -r now