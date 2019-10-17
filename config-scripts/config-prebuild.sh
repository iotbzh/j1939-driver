#!/bin/sh

# Enable automatic default config when mostconf is loaded
# Author: fulup/at/iot.bzh
# Date  : Avril 2017
# Object: Install udev and modprobe rules after driver install

BASEDIR=`dirname $0`

echo "*** Prebuild Create Directories"
mkdir -p /var/tmp/dkms
