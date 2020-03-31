## es 服务器搭建 

搭建elasticsearch + kibana 日志数据库搭建
--- 
### 1. 安装 
从[官网](https://www.elastic.co/cn/start)下载 es kibana安装包并解压。  
从[github](https://github.com/lmenezes/cerebro/releases)下载cerebro解压

### 2.修改配置文件

elasticsearch ./config/jvm.options  ./conig/elasticsearch.yml  
kibana ./config/kibana.yml  
cerebro ./conf/application.conf (借用 elasticsearch 的jdk,  `export JAVA_HOME =jdk路径`,  `PATH=$PATH:$JAVA_HOME/bin`)  

### 3.启动

elasticsearch ./bin/elasticsearch -d （默认 9200）  
kibana ./bin/kibana &  (默认 5601)   或在screen 中运行
cerebro ./bin/cerebro &(默认 9000) 或在screen 中运行

### 4.数据安全

#### 1.身份认证与用户鉴权  

1. `config`中添加 `xpack.security.enabled: true` 启动集群  
2. 运行 `bin/elasticsearch-setup-passwords interactive` 设置初始密码  
3. 开启完成后配置kibana `elasticsearch.username` 和 `elasticsearch.password`    
4. 在kibana中设置用户权限 增加用户  

#### 2. 集群内部安全通信

1. 运行`bin/elasticsearch-certutil ca` 创建 ca 证书  
2. 运行`bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12` 基于ca文件为节点签发证书  
3. 自建目录保存签发的证书
	
	````
	mkdir config/certs
	cp elastic-certificates.p12 config/certs/elastic-certificates.p12
	````
	
4. `config` 中开启证书验证
	
	````
	xpack.security.transport.ssl.enabled: true
	xpack.security.transport.ssl.verification_mode: certificate
	xpack.security.transport.ssl.keystore.path: certs/elastic-certificates.p12
	xpack.security.transport.ssl.truststore.path: certs/elastic-certificates.p12
	````

#### 3. 集群与外部的安全通信

1. 修改配置文件使用上面签发的证书对 http 进行验证 打开https
	
	````
	xpack.security.http.ssl.enabled: true
	xpack.security.http.ssl.keystore.path: certs/elastic-certificates.p12
	xpack.security.http.ssl.truststore.path: certs/elastic-certificates.p12
	````
2. kibana 使用 https 连接es  

	1. 使用 `openssl` 转换 es 签发的证书  并拷贝到保存的目录  
		
		````
		openssl pkcs12 -in elastic-certificates.p12 -cacerts -nokeys -out elastic-ca.pem
		cp elastic-ca.pem config/certs/elastic-ca.pem
		````  
	2. 修改 kibina 配置文件  
	
		````
		elasticsearch.hosts: ["https://xxx:xxxx"]
		elasticsearch.ssl.certificateAuthorities : 刚才生成的pem 的全路径
		elasticsearch.ssl.verificationMode: certificate
		```` 