## centos7 python 安装

centOS7 默认已经安装了 Python2， 我们只需要安装python3就可以了

---
### 安装python3依赖

```
yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel
```
### 下载python

使用`wget`从[官网](https://www.python.org/downloads/release)下载最新python安装文件（Source release）

```
cd '你要下载的目录'
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
```

### 解压压缩包

```
tar -zxvf Python-3.6.4.tgz
cd '解压后的文件夹'
```
### 编译

```
mkdir /usr/local/python3
./configure --prefix=/usr/local/python3
make
make install
```
### 把python2 的链接备份 链接python3,pip

```
cd /usr/bin
mv python python.bak
ln -s /usr/local/python3/bin/python3  /usr/bin/python
ln -s "/usr/local/python3/bin/pip3" /usr/bin/pip
```
### 因为yum脚本依赖python2，修改配置文件

```
vi /usr/bin/yum
#!/usr/bin/python 改为 #!/usr/bin/python.bak

vi /usr/bin/gnome-tweak-tool
#!/usr/bin/python 改为 #!/usr/bin/python.bak

vi /usr/libexec/urlgrabber-ext-down
#!/usr/bin/python 改为 #!/usr/bin/python.bak

```



