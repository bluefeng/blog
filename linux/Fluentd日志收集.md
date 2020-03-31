## [Fluentd](https://docs.fluentd.org/)

### 1. 安装

#### 1. Linux([Centos](https://docs.fluentd.org/installation/install-by-rpm))

1. add  repo and install:  
	`$ curl -L https://toolbelt.treasuredata.com/sh/install-redhat-td-agent3.sh | sh`  
2. 脚本命令  

	````
	$ sudo /etc/init.d/td-agent start
	$ sudo /etc/init.d/td-agent stop
	$ sudo /etc/init.d/td-agent restart
	$ sudo /etc/init.d/td-agent status
	````

3. 配置文件路径

	````
	/etc/td-agent/td-agent.conf
	/var/log/td-agent/td-agent.log
	````
4. 测试(查看.log输出)  
	`$ curl -X POST -d 'json={"json":"message"}' http://localhost:8888/debug.test`

#### 2. [Mac](https://docs.fluentd.org/installation/install-by-dmg)

1. 下载[安装包](https://td-agent-package-browser.herokuapp.com/3/macosx)  
2. 脚本命令

	````
	$ sudo launchctl load /Library/LaunchDaemons/td-agent.plist
	$ sudo launchctl unload /Library/LaunchDaemons/td-agent.plist
	````
3. 配置文件路径 

	````
	/etc/td-agent/td-agent.conf
	/var/log/td-agent/td-agent.log
	````
4. 测试(查看.log输出)  
	`curl -X POST -d 'json={"json":"message"}' http://localhost:8888/debug.test`

6. 卸载

	````
	rm -rf /Library/LaunchDaemons/td-agent.plist
	rm -rf /etc/td-agent
	rm -rf /opt/td-agent
	rm -rf /var/log/td-agent
	````

###  2. 配置文件解析   

#### 指令说明  
`source`  确定数据来源  
`match` 确定数据输出目标  
`filter` 确定事件处理管道  
`system` 系统范围的配置  
`label` 给输出和管线路由分组  
`@include` 包括其他文件  

1.  `source`  指令表示数据从何处来  
	标准输入插件有`http` 和 `forward` 分别从 http 和 tcp 接收数据。同时可以定义多个`source`
	每一个 `source` 必须包括 `@type` 参数， `@type` 参数说明使用的输入插件。  
	`source` 生成事件提供给 Fluentd 的路由引擎，一个事件包括三个部分: `tag`, `time`, `record`。`tag` 是一个以`.`分隔的字符串，为路由引擎指明方向，`time` 由输入插件生成必须是Unix时间格式，`record ` 是 `json` 对象。
	
2. `match` 指令告诉 fluentd 该怎么做  
	`match`指令查找具有匹配标签的事件并对其进行处理，`match`指令最常见的用法是将事件输出到其他系统, 标准输出插件包括`file`和`forward`。  
	每一个`match`必须包括一个匹配模式和`@type`参数，只有带有与标签匹配的的事件才会被发送到输出目标。

3. `filter` 时间处理管道  
	`filter`语法类似`match`，可以将事件作用于管道。类似：  
	`Input  ->  filter 1 -> ... -> filter N -> Output`  
	
4. `system` 设置系统范围的[配置](https://docs.fluentd.org/deployment/system-config)  
	
5. `label` 指令将 `filter` 和 output 分组  
	`label` 指令将过滤器和输出分组以进行内部路由。“标签”降低了标签处理的复杂性。`label`是内置的插件参数，因此需要前缀`@`。 eg：  
	
	````
	<source>
	  @type forward
	</source>
	​
	<source>
	  @type tail
	  @label @SYSTEM
	</source>
	​
	<filter access.**>
	  @type record_transformer
	  <record>
	    # ...
	  </record>
	</filter>
	<match **>
	  @type elasticsearch
	  # ...
	</match>
	​
	<label @SYSTEM>
	  <filter var.log.middleware.**>
	    @type grep
	    # ...
	  </filter>
	  <match **>
	    @type s3
	    # ...
	  </match>
	</label>
	````
	
	`@ERROR` 标签是内置标签，记录插件api发出的错误记录，如果在配置中设置`<label @ERROR>`，则在发出相关错误时，事件将被路由的这个标签。

6. `@include` 指令用于复用你的配置文件  
	该`@include`指令支持普通文件路径，glob匹配模式，以及HTTP URL约定
	
	````
	# absolute path
	@include /path/to/config.conf
	​
	# if using a relative path, the directive will use
	# the dirname of this config file to expand the path
	@include extra.conf
	​
	# glob match pattern
	@include config.d/*.conf
	​
	# http
	@include http://example.com/fluent.conf
	````
	
#### 匹配规则  

匹配规则用于 `match` 和 `filter` 标签  

##### 通配符和扩展  

* `*` 匹配单个标签部分   
	`a.*` 匹配 `a.b` 但是不匹配 `a` 和 `a.b.c`。  
* `**` 匹配0个或者多个标签部分  
	`a.**` 匹配 `a.b` 并且匹配 `a` 和 `a.b.c`。  
* `{X,Y,Z}` 匹配 X, Y 或者Z，X,Y,Z 是匹配模式。  
	`{a,b}` 匹配 `a` 和 `b`, 也可以这么用 `a.{b,c}.*`, `a.{b,c.**}`。  
* `#{...}`将括号内的字符串作为Ruby表达式求值。  
	
	````
	<match "app.#{ENV['FLUENTD_TAG']}">
	  @type stdout
	</match>
	````
* 当一个标签内列出了多个模式（由一个或多个空格分隔）时，它会与列出的任何模式匹配
	* `<match a b>` 匹配 `a` 和 `b`
	* `<match a.** b.*>` 匹配 `a`, `a.b`, `a.b.c`, `b.d`

##### 匹配顺序  

Fluentd尝试按标签在配置文件中出现的顺序进行匹配

````
# ** matches all tags. Bad :(
<match **>
  @type blackhole_plugin
</match>
​
<match myapp.access>
  @type file
  path /var/log/fluent/access
</match>
````

`myapp.access` 不会被匹配到。应该在紧密匹配模式之后定义较宽的匹配模式。 需要匹配多个输出使用[out_copy](https://docs.fluentd.org/output/copy) 插件。  

#### 值支持的数据类型  

每个Fluentd插件都有一组参数，例如，in_tail具有诸如`rotate_wait`和`pos_file`的参数, 每个参数都有与之关联的特定类型。它们的定义如下：  

* `string` 类型：字段被解析为字符串。这是最“通用”类型，每个插件决定如何处理字符串。`'` 或者 `"`包围。
*  `integer` 类型：解析为整型。
*  `float` 类型：解析为浮点型。
*  `size` 类型：将字段解析为字节数，有几种符号上的变化：
	* `<INTEGER>k` or `<INTEGER>K`, 解析为 整数 千。 下面以此类推    
	* `<INTEGER>m` or `<INTEGER>M`  
	* `<INTEGER>g` or `<INTEGER>G`  
	* `<INTEGER>t` or `<INTEGER>T`  
	* 否则，该字段将解析为整数，并且该整数为字节数  
* `time`类型：字段被解析为持续时间  
	* `<INTEGER>s` 秒  
	* `<INTEGER>m` 分  
	* `<INTEGER>h` 时  
	* `<INTEGER>d` 天  
	* 否则，该字段将解析为float，并且float是秒数。此选项对于指定亚秒级的持续时间  
* `array` 类型：该字段被解析为JSON数组，它还支持速记语法  
	* 正常：`["key1", "key2"]`  
	* 速记：`key1,key2`  
* `hash` 类型：该字段被解析为JSON对象。它还支持速记语法。  
	* 正常：`{"key1":"value1", "key2":"value2"}`  
	* 速记：`key1:value1,key2:value2`  

#### 常用插件参数

这些参数是系统保留的，并且具有`@`前缀:  

* `@type` 指定插件类型
* `@id` 指定插件ID。in_monitor_agent将此值用于plugin_id字段
* `@label` 指定标签符号
* `@log_level` 按插件指定日志级别