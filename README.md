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
patch -p1 < ../can-j1939.patch
```
