## Laravel 已有项目配置

### php安装
1. 从[官网](https://www.php.net/downloads.php)下载php安装包
2. 安装 `php` 依赖 

	````
	sudo yum install -y gcc sqlite-devel libxml2 libxml2-devel openssl openssl-devel bzip2 bzip2-devel libcurl libcurl-devel libjpeg libjpeg-devel libpng libpng-devel freetype freetype-devel gmp gmp-devel libmcrypt libmcrypt-devel readline readline-devel libxslt libxslt-devel oniguruma oniguruma-devel zip unzip php-zip
	````
3. 修改`./configure`增加扩展: 

	````
	./configure \
	--prefix=/usr/local/php7 \
	--with-config-file-path=/usr/local/php7/etc \
	--enable-fpm \
	--with-xmlrpc \
	--with-openssl \
	--with-sqlite3 \
	--with-zlib \
	--with-openssl-dir \
	--with-zlib-dir \
	--enable-json \
	--enable-mbstring \
	--enable-pdo \
	--with-mysqli=mysqlnd \
	--with-pdo-mysql=mysqlnd \
	--with-zlib-dir \
	--with-pdo-sqlite \
	--with-readline \
	--enable-simplexml \
	--enable-mysqlnd-compression-support \
	--with-curl
	````  
4. `make && make install`  

5. 环境变量  
	使用vi命令打开`/etc/profile`文件，在文件最末尾加上如下代码
	
	````
	export PHP_HOME=/usr/local/php7
	export PATH=$PATH:$PHP_HOME/bin:$PHP_HOME/sbin
	````
	
6.  修改配置文件 启动php-fpm

	````
	sudo cp php.ini-production /usr/local/php7/etc/php.ini (源代码下执行)
	cd /usr/local/php7/etc
	sudo cp php-fpm.conf.default php-fpm.conf
	cd /usr/local/php7/etc/php-fpm.d
	sudo cp www.conf.default www.conf


	修改php-fpm.conf  
	pid = ... --打开注释
	
	修改 www.conf
	listen = 127.0.0.1:8181  --修改需要的端口号
	
	php-fpm -t     --检测php-fpm配置文件
	php-fpm 	--启动
	
	kill -INT `cat  pid路径`      --php-fpm关闭
	kill -USR2 `cat  pid路径`    --php-fpm平滑重启
	````

7. 安装 [Composer](https://docs.phpcomposer.com/00-intro.html)

	````
	curl -sS https://getcomposer.org/installer | php
	sudo mv composer.phar /usr/local/bin/composer
	````
8. Composer安装项目依赖

	````
	--切换为国内镜像
	composer config -g repo.packagist composer https://packagist.phpcomposer.com
	--更新自己
	composer selfupdate
	--在项目目录下 (composer.json)
	composer install
	````
	
### nginx 配置

1. 安装[openresty](http://openresty.org/cn/linux-packages.html)
	
	````
	--添加仓库
	sudo yum install -y yum-utils
	sudo yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo
	
	--安装软件包
	sudo yum install -y openresty
	
	--安装命令行工具
	sudo yum install -y openresty-resty
	````
2. 修改配置文件 增加
	
	````
	server {
		listen 9191;
		root   .../public;
		index  index.php index.htm index.html;
		location / {
			try_files $uri $uri/ /index.php?$query_string;
		}
	
		location ~ \.php$ {
			fastcgi_pass   127.0.0.1:8181;
			fastcgi_index  index.php;
			fastcgi_param  SCRIPT_FILENAME  .../public/$fastcgi_script_name;
			include        fastcgi_params;
			proxy_read_timeout 6000;
			fastcgi_read_timeout 1000;
		}
	}
	````
	
	