#!/bin/bash

if command -v dpkg >/dev/null 2>&1; then
  dpkg --force-all -i /root/pkgs/*.deb
elif command -v rpm >/dev/null 2>&1; then
  rpm -iUv /root/pkgs/*.rpm --nodeps --force
else
  echo "Unknown package manager"
fi

driver_installed=$(find /usr/local/Ascend/driver -name "version.info"|wc -l)
firmware_installed=$(find /usr/local/Ascend/firmware -name "version.info"|wc -l)
if [ $driver_installed -eq 0 ];then
  bash /root/*-driver*.run --nox11 --full --install-for-all --quiet
fi
if [ $firmware_installed -eq 0 ]; then
  bash /root/*firmware*.run --nox11 --full --quiet
fi
if [ $driver_installed -eq 1 ]&&[ $firmware_installed -eq 1 ]; then
  firmware_filename=$(ls /root/Ascend-hdk-*-firmware*)
  basename="${firmware_filename%.*}"
  firmware_part=$(echo $basename | cut -d "-" -f 5)
  if [[ "${firmware_part:0:8}"=="firmware" ]]; then
    version_part=$(echo $firmware_part | cut -d "_" -f 2 )
  else
    echo "wrong firmware file format"
    exit 1
  fi
  present_version=$(awk -F= '($1=="Version"){print $2}' /usr/local/Ascend/firmware/version.info)
  if [[ "$present_version" != "$version_part" ]]; then
    bash /root/*firmware*.run --nox11 --upgrade --quiet
  fi
  driver_filename=$(ls /root/Ascend-hdk-*-driver*)
  driver_part=$(echo $driver_filename | cut -d "-" -f 5)
  if [[ "${driver_part:0:6}"=="driver" ]]; then
    version_part=$(echo $driver_part | cut -d "_" -f 2)
  else
    echo "wrong npu file format"
    exit 1
  fi
  present_version=$(awk -F= '($1=="Version"){print $2}' /usr/local/Ascend/driver/version.info)
  if [[ "$present_version" != "$version_part" ]]; then
    bash /root/*-driver*.run --nox11 --upgrade --quiet
  fi
fi
