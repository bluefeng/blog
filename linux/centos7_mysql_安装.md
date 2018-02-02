## centos7mysql的安装和卸载

### 卸载mariadb

因为centos7预装了mariadb（mysql的一个社区开源分支版本），所以安装mysql之前需要卸载掉，不然会冲突。

```
#检查是否安装mariadb
yum list installed | grep mariadb 

#如果有输出则全部卸载
yum -y remove mariadb*    

#再次运行确认删除干净
yum list installed | grep mariadb
```

### 安装mysql指定版本并开启远程连接

1. 如果没有安装wget需要先安装wget
	
	```
	yum install wget 
	```
	
[mysqlnet]: https://dev.mysql.com/downloads/repo/yum/
2. 从[官网][mysqlnet]下载对应系统版本的yum源最新rpm安装包，[官网][mysqlnet]有说明最新安装包里包含哪些mysql版本:
	![](http://www.iwill.fun/media/blog/20180202/mysqldown.png)  
	我下载的[Red Hat Enterprise Linux 7 / Oracle Linux 7 (Architecture Independent), RPM Package](https://dev.mysql.com/downloads/file/?id=470281),直接鼠标右键下面的[No thanks, just start my download.](https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm)选择复制链接地址就可以得到我们要下在的rpm包地址  
	![](http://www.iwill.fun/media/blog/20180202/mysqldowm2.png)  

	```
	#获得地址后使用wget获取rpm包
	wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
	
	#安装下载的发行包
	rpm -Uvh platform-and-version-specific-package-name.rpm
	```
	
3. 选择一个合适的mysql版本（安装最新版本可以忽略默认会安装最新版本）
	
	```
	#查看包内有的版本
	yum repolist all | grep mysql
	
	#禁用已启用的最新版本， 启用需要的版本 eg：
	yum-config-manager --disable mysql57-community
	yum-config-manager --enable mysql55-community
	
	#检查禁用和启用的是否正确
	yum repolist all | grep mysql
	```
	
4. 安装并启动mysql
	
	```
	#安装
	yum install mysql-community-server
	
	#启动
	service mysqld start
	
	#开机启动
	systemctl enable mysqld
	systemctl daemon-reload
	
	#因为安装了rpm包会自动更新mysql 如果不需要再卸载掉
	#查看包名
	rpm -qa | grep -i mysql
	#卸载掉.noarch
	yum -y remove mysql57-community-release-el7-11.noarch
	```
	
5. 修改密码开启远程连接
	
	```
	#运行命令进入数据库
	mysql -uroot -p
	
	#某些版本会在安装的时候生成随机密码，如果进入mysql需要密码的话查看随机密码
	grep "password" /var/log/mysqld.log
	
	#忘记密码可以先
	mysqld_safe --skip-grant-tables&
	
	#切换到mysql库
	use mysql;
	
	#修改密码
	update user set password = password('newpass') where user = 'root';
	
	#增加远程账户
	grant all privileges on 库名(*全部).表名(*全部) to '用户名'@'%' identified by '密码' with grant option;
	
	#刷新权限
	flush privileges;
	```

###卸载mysql

1. 查看是否安装mysql(-i: 不区分大小写)
	
	```
	rpm -qa | grep -i mysql
	```
	
2. 卸载mysql
	
	```
	yum -y remove (所有上一步查出来的应用)
	```
	
3. 删除分散的mysql文件(警告：小心错删其他应用的文件)

	```
	find / -name mysql
	rm -rf /usr/lib/mysql
	rm -rf /usr/share/mysql
	```

4. 删除自启服务
	
	```
	chkconfig --list | grep -i mysql
	chkconfig --del mysqld
	```