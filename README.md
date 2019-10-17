# J1939

## Extract Linux driver

```bash
git clone https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
cd linux
git fetch
git checkout -b tag-v5.0 v5.0
git archive -o ../subarchive.zip HEAD drivers/net/can include/linux/can net/can include/uapi/linux/can.h include/net/netns/can.h include/uapi/linux/can
```


```bash
mkdir j1939-driver;
cd j1939-driver; 
unzip ../subarchive.zip

git init
git remote add origin git@git.ovh.iot:iotbzh/j1939-driver.git
git add .
git commit -m "Initial commit"
git tag v5.0
git push --tags -u origin master
```

## Apply patch

```bash
git am ../can-j1939.patch
```

## Install dep

Fedora:

```bash
dnf install kernel-core kernel-devel dkms make
```
Fedora:

```bash
sudo apt install dkms linux-headers-$(uname -a | cut -d' ' -f 3 | cut -d'-' -f1)
```

## Build dkms

```bash
export VERSION="5.0"
export MODULE_NAME="can"
export MODULE_SOURCE="/usr/src/${MODULE_NAME}-${VERSION}/"


cd ${HERE_YOUR_SOURCE}
sudo mkdir -p ${MODULE_SOURCE}
sudo cp -fr * ${MODULE_SOURCE}

sudo dkms add     -m ${MODULE_NAME} -v ${VERSION} -c ./dkms.conf
sudo dkms build   -m ${MODULE_NAME} -v ${VERSION} -c ./dkms.conf
sudo dkms install -m ${MODULE_NAME} -v ${VERSION} -c ./dkms.conf
```

To remove module:

```bash
sudo dkms remove  -m ${MODULE_NAME} -v ${VERSION} --all
```

## Build rpm src package

```bash
sudo dnf in rpm-build
sudo dkms mkrpm --source-only -m ${MODULE_NAME} -v ${VERSION}
sudo dkms mktarball --source-only -m ${MODULE_NAME} -v ${VERSION}
```

## Build deb src package

```bash
sudo apt install debhelper
sudo dkms mkrpm --source-only -m ${MODULE_NAME} -v ${VERSION}
sudo dkms mktarball --source-only -m ${MODULE_NAME} -v ${VERSION}
```

## Install package from OBS


### Ubuntu

```bash
export DISTRO="xUbuntu_19.10"
wget -O - http://obs.lorient.iot/J1939:/5.0/${DISTRO}/Release.key | sudo apt-key add -
sudo bash -c "cat >> /etc/apt/sources.list.d/J1939.list <<EOF
#Can J1939
deb http://obs.lorient.iot/J1939:/5.0/${DISTRO}/ ./
EOF"
sudo apt update  -oAcquire::AllowInsecureRepositories=true
sudo apt-get install can-dkms
```

### Fedora

```bash
sudo bash -c "cat >> /etc/yum.repos.d/J1939.repo <<EOF
[J1939]
name=Automotive Grade Linux Application Development tools - master branch (Fedora_30)
type=rpm-md
baseurl=http://obs.lorient.iot/J1939:/5.0/Fedora_30/
gpgcheck=1
gpgkey=http://obs.lorient.iot/J1939:/5.0/Fedora_30/repodata/repomd.xml.key
enabled=1
EOF"

sudo dnf install can-dkms
```

## Test kernel mod

```bash
sudo /usr/sbin/modprobe can-j1939
sudo infomod can-j1939
```
