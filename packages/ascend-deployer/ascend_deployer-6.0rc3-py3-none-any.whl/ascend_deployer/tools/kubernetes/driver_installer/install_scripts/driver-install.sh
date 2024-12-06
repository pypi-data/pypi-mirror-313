#!/bin/bash

ping -c 1 172.17.0.1 > /dev/null

if [ $? -eq 0 ];then
  hostIp=172.17.0.1
else
  hostIp=$(ip route|awk '/default/ {print $3}')
fi


mkdir -p /root/.ssh /mnt/.ssh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
cat ~/.ssh/id_rsa.pub >> /mnt/.ssh/authorized_keys

cd /root
cp *-driver*.run /mnt
cp *firmware*.run /mnt
cp install.sh /mnt
cp exec.sh /mnt

mkdir -p /mnt/pkgs
cp *.deb /mnt/pkgs
cp *.rpm /mnt/pkgs

ssh -o "StrictHostKeyChecking=no" root@$hostIp groupadd HwHiAiUser
ssh root@$hostIp useradd -g HwHiAiUser -d /home/HwHiAiUser -m HwHiAiUser -s /bin/bash
ssh root@$hostIp bash /root/exec.sh

tail -f /var/log/ascend_seclog/ascend_install.log
