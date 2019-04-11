## Makefile编写

一个工程中的源文件不计其数，其按类型、功能、模块分别放在若干个目录中，makefile定义了一系列的规则来指定，哪些文件需要先编译，哪些文件需要后编译，哪些文件需要重新编译，甚至于进行更复杂的功能操作，因为 makefile就像一个Shell脚本一样，其中也可以执行操作系统的命令。

makefile带来的好处就是——“自动化编译”，一旦写好，只需要一个make命令，整个工程完全自动编译，极大的提高了软件开发的效率。make是一个命令工具，是一个解释makefile中指令的命令工具，一般来说，大多数的IDE都有这个命令，比如：Delphi的make，Visual C++的nmake，Linux下GNU的make。可见，makefile都成为了一种在工程方面的编译方法。


---
### 关于程序的编译和链接

一般来水，无论是C还是C++，首先要把文件编译成中间代码文件，在Windows下是`.obj`文件，UNIX下是`.o`文件，也就是`Object File`，这个动作叫做编译*(compile)*。然后再把大量的`Object File`合并成执行文件，这个动作叫做链接*(link)*。

编译时，编译器需要的是语法的正确，函数与变量的声明的正确。对于后者，通常是你需要告诉编译器头文件的所在位置*(头文件中应该只是声明，而定义应该放在C/C++文件中)*，只要所有的语法正确，编译器就可以编译出中间目标文件。一般来说，每个源文件都应该对应于一个中间目标文件*(`.o`文件或是`.obj`文件)*。

链接时，主要是链接函数和全局变量，所以，我们可以使用这些中间目标文件*(`.o`文件或是`.obj`文件)*来链接我们的应用程序。链接器并不管函数所在的源文件，只管函数的中间目标文件*(`Object File`)*，在大多数时候，由于源文件太多，编译生成的中间目标文件太多，而在链接时需要明显地指出中间目标文件名，这对于编译很不方便，所以，我们要给中间目标文件打个包，在Windows下这种包叫“库文件”*(Library File)*，也就是`.lib`文件，在UNIX下，是Archive File，也就是`.a`文件。

源文件首先会生成中间目标文件，再由中间目标文件生成执行文件。在编译时，编译器只检测程序语法，和函数、变量是否被声明。如果函数未被声明，编译器会给出一个警告，但可以生成`Object File`。而在链接程序时，链接器会在所有的`Object File`中找寻函数的实现，如果找不到，那到就会报链接错误码`Linker Error`，在VC下，这种错误一般是：`Link 2001`错误，意思说是说，链接器未能找到函数的实现。你需要指定函数的`Object File`。


### 1 Makefile介绍

make命令执行时，需要一个 Makefile 文件，以告诉make命令需要怎么样的去编译和链接程序。规则：

1. 如果这个工程没有编译过，那么我们的所有C文件都要编译并被链接。
2. 如果这个工程的某几个C文件被修改，那么我们只编译被修改的C文件，并链接目标程序。
3. 如果这个工程的头文件被改变了，那么我们需要编译引用了这几个头文件的C文件，并链接目标程序。

#### 1.1 Makefile 主要的5个部分（显示规则，隐晦规则，变量定义，文件指示，注释）

Makefile基本格式如下：

````
target ... : prerequisites ...
    command
    ...
    ...
````
* target --目标文件，可以使 `Object File`, 也可以是可执行文件。
* prerequisites --生成target所需要的文件或者目标。
* command --make需要执行的命令（任意的shell命令），Makefile中的命令必须以`[tab]`开头。

1. 显示规则：说明如何生成一个或多个目标文件(包括 生成的文件, 文件的依赖文件, 生成的命令)
2. 隐晦规则：make的自动推导功能所执行的规则
3. 变量定义：Makefile中定义的变量
4. 文件指示：Makefile中引用其他Makefile; 指定Makefile中有效部分; 定义一个多行命令
5. 注释：Makefile只有行注释 "#", 如果要使用或者输出"#"字符, 需要进行转义, "\#"

#### 1.2 GNU make 的工作方式

1. 读入主Makefile (主Makefile中可以引用其他Makefile)
2. 读入被include的其他Makefile
3. 初始化文件中的变量
4. 推导隐晦规则, 并分析所有规则
5. 为所有的目标文件创建依赖关系链
6. 根据依赖关系, 决定哪些目标要重新生成
7. 执行生成命令

### 2 Makefile 初级语法

#### 2.1 Makefile 规则

##### 2.1.1 规则语法

规则主要2部分：依赖关系和生成目标的方法。
语法以下两种：

````
target ... : prerequisites ...
    command
    ...
````
或者

````
target ... : prerequisites ; command
    command
    ...
````
command太长, 可以用 `\` 作为换行符

##### 2.1.2 规则中的通配符

* `*` ：表示任意一个或多个字符
* `?` ：表示任意一个字符
* `[...]` ：[abcd] 表示a,b,c,d中任意一个字符, [^abcd]表示除a,b,c,d以外的字符, [0-9]表示 0~9中任意一个数字
* `~` ：表示用户的home目录

##### 2.1.3 路径搜索

当一个Makefile中涉及到大量源文件时(这些源文件和Makefile极有可能不在同一个目录中)。这时, 最好将源文件的路径明确在Makefile中, 便于编译时查找。 Makefile中有个特殊的变量 `VPATH` 就是完成这个功能的。指定了 `VPATH` 之后, 如果当前目录中没有找到相应文件或依赖的文件, Makefile 回到 `VPATH` 指定的路径中再去查找。
`VPATH`使用方法：

* `vpath <directories>` ：当前目录中找不到文件时, 就从`<directories>`中搜索，目录由“冒号”分隔
* `vpath <pattern> <directories>` ：符合<pattern>格式的文件, 就从<directories>中搜索
* `vpath <pattern>` ：清除符合<pattern>格式的文件搜索路径
* `vpath` ：清除所有已经设置好的文件路径

````
# 示例1 - 当前目录中找不到文件时, 按顺序从 src目录 ../parent-dir目录中查找文件
vpath src:../parent-dir
# 示例2 - .h结尾的文件都从 ./header 目录中查找
vpath %.h ./header
# 示例3 - 清除示例2中设置的规则
vpath %.h
# 示例4 - 清除所有VPATH的设置
vpath
````

#### 2.2 Makefile 中的变量

##### 2.2.1 变量定义 ( = or := )

其中 `=` 和 `:=` 的区别在于, `:=` 只能使用前面定义好的变量, `=` 可以使用后面定义的变量

````
OBJS = programA.o programB.o
OBJS-ADD = $(OBJS) programC.o
# 或者
OBJS := programA.o programB.o
OBJS-ADD := $(OBJS) programC.o
````

##### 2.2.2 变量替换

````
# Makefile内容
SRCS := programA.c programB.c programC.c
OBJS := $(SRCS:%.c=%.o)
all:
    @echo "SRCS: " $(SRCS)
    @echo "OBJS: " $(OBJS)
# bash中运行make
$ make
SRCS:  programA.c programB.c programC.c
OBJS:  programA.o programB.o programC.o
````

##### 2.2.3 变量追加值 +=

````
# Makefile内容
SRCS := programA.c programB.c programC.c
SRCS += programD.c
all:
    @echo "SRCS: " $(SRCS)
# bash中运行make
$ make
SRCS:  programA.c programB.c programC.c programD.c
````

##### 2.2.4 变量覆盖 override

作用是使 Makefile中定义的变量能够覆盖 make 命令参数中指定的变量
语法：

* `override <variable> = <value>`
* `override <variable> := <value>`
* `override <variable> += <value>`


##### 2.2.5 目标变量

作用是使变量的作用域仅限于这个目标(target), 而不像之前例子中定义的变量, 对整个Makefile都有效.
````
# Makefile 内容
SRCS := programA.c programB.c programC.c
target1: TARGET1-SRCS := programD.c
target1:
    @echo "SRCS: " $(SRCS)
    @echo "SRCS: " $(TARGET1-SRCS)
target2:
    @echo "SRCS: " $(SRCS)
    @echo "SRCS: " $(TARGET1-SRCS)
# bash中执行make
$ make target1
SRCS:  programA.c programB.c programC.c
SRCS:  programD.c
$ make target2     <-- target2中显示不了 $(TARGET1-SRCS)
SRCS:  programA.c programB.c programC.c
SRCS:
````

#### 2.3 Makefile 命令前缀

Makefile 中书写shell命令时可以加2种前缀 `@` 和 `-`, 或者不用前缀。

* 不用前缀 ： 输出执行的命令以及命令执行的结果, 出错的话停止执行
* 前缀 @ ： 只输出命令执行的结果, 出错的话停止执行
* 前缀 - ： 命令执行有错的话, 忽略错误, 继续执行

#### 2.4 伪目标

伪目标并不是一个"目标(target)", 不像真正的目标那样会生成一个目标文件。典型的伪目标是 Makefile 中用来清理编译过程中中间文件的 `clean` 伪目标, 使用`.PHONY`声明一个伪目标，一般格式如下:

````
.PHONY: clean
clean:
    -rm -f *.o
````

#### 2.5 引用其他的Makefile

语法: `include <filename>`  (`filename` 可以包含通配符和路径)  
eg: `include ./other/Makefile`

#### 2.6 查看C文件的依赖关系

写 Makefile 的时候, 需要确定每个目标的依赖关系。  
GNU提供一个机制可以查看C代码文件依赖那些文件, 这样我们在写 Makefile 目标的时候就不用打开C源码来看其依赖那些文件了。比如, 下面命令显示内核源码中 `virt/kvm/kvm_main.c` 中的依赖关系:

````
$ cd virt/kvm/
$ gcc -MM kvm_main.c 
kvm_main.o: kvm_main.c iodev.h coalesced_mmio.h async_pf.h   <-- 这句就可以加到 Makefile 中作为编译 kvm_main.o 的依赖关系
````

#### 2.7 make 退出码

Makefile的退出码有以下3种：  

* `0` :表示成功执行
* `1` :表示make命令出现了错误
* `2` :使用了 "-q" 选项, 并且make使得一些目标不需要更新

#### 2.8 指定 Makefile, 指定特定目标

默认执行 `make` 命令时, GNU make在当前目录下依次搜索下面3个文件`GNUmakefile`, `makefile`, `Makefile`,  
找到对应文件之后, 就开始执行此文件中的第一个目标`target`. 如果找不到这3个文件就报错。  
非默认情况下, 可以在 `make` 命令中指定特定的 Makefile 和特定的目标。

````
# Makefile文件名改为 MyMake, 内容
target1:
    @echo "target [1]  begin"
    @echo "target [1]  end"
target2:
    @echo "target [2]  begin"
    @echo "target [2]  end"
########### bash 中执行 make #############
$ ls
Makefile
$ mv Makefile MyMake
$ ls
MyMake
$ make                     <-- 找不到默认的 Makefile
make: *** No targets specified and no makefile found.  Stop.
$ make -f MyMake           <-- 指定特定的Makefile
target [1]  begin
target [1]  end
$ make -f MyMake target2   <-- 指定特定的目标(target)
target [2]  begin
target [2]  end
````

#### 2.9 make 参数介绍

make 的参数有很多, 可以通过 `make -h` 去查看, 下面只介绍几个我认为比较有用的。

|参数|含义|
|:------|:------|
| --debug[=<options>]| 输出make的调试信息, options 可以是 a, b, v |
| -j --jobs| 同时运行的命令的个数, 也就是多线程执行 Makefile| 
| -r --no-builtin-rules | 禁止使用任何隐含规则|
| -R --no-builtin-variabes | 禁止使用任何作用于变量上的隐含规则|
| -B --always-make | 假设所有目标都有更新, 即强制重编译|

#### 2.10 Makefile 隐含规则
编译C时，`<n>.o` 的目标会自动推导为 `<n>.c`

````
# Makefile 中
main : main.o
    gcc -o main main.o
#会自动变为:
main : main.o
    gcc -o main main.o
main.o: main.c    <-- main.o 这个目标是隐含生成的
    gcc -c main.c
````

#### 2.11 隐含规则中的 命令变量 和 命令参数变量

##### 2.11.1 命令变量 书写Makefile写shell时可以直接用这些变量

|变量名|含义|
|:---|:---|
|RM|rm -f|
|AR|ar|
|CC|cc|
|CXX|g++|

##### 2.11.2 命令参数变量

|变量名|含义|
|:---|:---|
|CFLAGS|C语言编译器的参数|
|CXXFLAGS|C++语言编译器的参数|

#### 2.12 自动变量

Makefile 中很多时候通过自动变量来简化书写, 各个自动变量的含义如下:

|变量名|含义|
|:---|:---|
|`$@`|目标集合|
|`$%`|当目标是函数库文件时, 表示其中的目标文件名|
|`$<`|第一个依赖目标. 如果依赖目标是多个, 逐个表示依赖目标|
|`$?`|比目标新的依赖目标的集合|
|`$^`|所有依赖目标的集合, 会去除重复的依赖目标|
|`$+`|所有依赖目标的集合, 不会去除重复的依赖目标|
|`$*`|这个是GNU make特有的, 其它的make不一定支持|

### 3 Makefile 高级语法

#### 3.1 嵌套Makefile

在Makefile 文件中 cd 到其他Makefile文件目录 执行make， 可以使用 export 定义或者修改当前进程的环境变量， 达到传递参数的效果，例如`export VALUE1 := export.c`

#### 3.2 定义命令包

命令包有点像是个函数, 将连续的相同的命令合成一条, 减少 Makefile 中的代码量, 便于以后维护。    
语法:

````
define <command-name>
command
...
endef
````

例如：

````
# Makefile 内容
define run-hello-makefile
@echo -n "Hello"
@echo " Makefile!"
@echo "这里可以执行多条 Shell 命令!"
endef
all:
	$(run-hello-makefile)
# bash 中运行make
$ make
Hello Makefile!
这里可以执行多条 Shell 命令!
````

#### 3.3 条件判断

条件判断的关键字主要有 ifeq ifneq ifdef ifndef  
语法：

````
<conditional-directive>
<text-if-true>
endif
# 或者
<conditional-directive>
<text-if-true>
else
<text-if-false>
endif
````

eg:

````
# ifeq的例子, ifneq和ifeq的使用方法类似, 就是取反
# Makefile 内容
all:
ifeq ("aa", "bb")
    @echo "equal"
else
    @echo "not equal"
endif
# bash 中执行 make
$ make
not equal
#
#
#ifdef的例子, ifndef和ifdef的使用方法类似, 就是取反
# Makefile 内容
SRCS := program.c
all:
ifdef SRCS
    @echo $(SRCS)
else
    @echo "no SRCS"
endif
# bash 中执行 make
$ make
program.c
````

#### 3.4 Makefile 中的函数

Makefile 中自带了一些函数, 利用这些函数可以简化 Makefile 的编写。  
函数调用语法如下:

````
$(<function> <arguments>)
# 或者
${<function> <arguments>}
````

##### 3.4.1 字符串函数
|函数|简介|功能|返回值|
|:----|:----|:----|:----|
|`$(subst <from>,<to>,<text>)`|字符串替换函数|把字符串`<text>` 中的 `<from>` 替换为 `<to>`|替换过的字符串|
|`$(patsubst <pattern>,<replacement>,<text>)`|模式字符串替换函数|查找`<text>`中的单词(单词以`空格`, `tab`, `换行`来分割) 是否符合 `<pattern>`, 符合的话, 用 `<replacement>` 替代|替换过的字符串|
|`$(strip <string>)`|去空格函数|去掉 `<string>` 字符串中开头和结尾的空字符|替换过的字符串|
|`$(findstring <find>,<in>)`|查找字符串函数|在字符串 `<in>`中查找 `<find>` 字符串|如果找到, 返回 `<find>` 字符串,  否则返回空字符串|
|`$(filter <pattern...>,<text>)`|过滤函数|以 `<pattern>` 模式过滤字符串 `<text>`, **保留** 符合模式 <pattern> 的单词, 可以有多个模式|符合模式 `<pattern>` 的字符串|
|`$(filter-out <pattern...>,<text>)`|反过滤函数|以 `<pattern>` 模式过滤字符串 `<text>`, **去除** 符合模式 `<pattern>` 的单词, 可以有多个模式|不符合模式 `<pattern>` 的字符串|
|`$(sort <list>)`|排序函数|给字符串 `<list>` 中的单词排序 (升序)|排序后的字符串|
|`$(word <n>,<text>)`|取单词函数|取字符串 `<text>` 中的 第`<n>`个单词 (n从1开始)|`<text>` 中的第`<n>`个单词, 如果`<n>` 比 `<text>` 中单词个数要大, 则返回空字符串|
|`$(wordlist <s>,<e>,<text>)`|取单词串函数|从字符串`<text>`中取从`<s>`开始到`<e>`的单词串,`<s>`和`<e>`是一个数字|从`<s>`到`<e>`的字符串|
|`$(words <text>)`|单词个数统计函数| 统计字符串 `<text>` 中单词的个数|单词个数|
|`$(firstword <text>)`|首单词函数|取字符串 `<text>` 中的第一个单词|字符串 `<text>` 中的第一个单词|

##### 3.4.2 文件名函数

|函数|简介|功能|返回值|
|:----|:----|:----|:----|
|`$(dir <names...>)`|取目录函数|从文件名序列 `<names>` 中取出目录部分|文件名序列 `<names>` 中的目录部分|
|`$(notdir <names...>)`|取文件函数|从文件名序列 `<names>` 中取出非目录部分|文件名序列 `<names>` 中的非目录部分|
|`$(suffix <names...>)`|取后缀函数|从文件名序列 `<names>` 中取出各个文件名的后缀|文件名序列 `<names>` 中各个文件名的后缀, 没有后缀则返回空字符串|
|`$(basename <names...>)`|取前缀函数| 从文件名序列 `<names>` 中取出各个文件名的前缀|文件名序列 `<names>` 中各个文件名的前缀, 没有前缀则返回空字符串|
|`$(addsuffix <suffix>,<names...>)`|加后缀函数|把后缀 `<suffix>` 加到 `<names>` 中的每个单词后面|加过后缀的文件名序列|
|`$(addprefix <prefix>,<names...>)`|加前缀函数|把前缀 `<prefix>` 加到 `<names>` 中的每个单词前面|加过前缀的文件名序列|
|`$(join <list1>,<list2>)`|连接函数|`<list2> `中对应的单词加到 `<list1>` 后面|连接后的字符串|

##### 3.4.3 foreach

`$(foreach <var>,<list>,<text>)`

eg：

````
# Makefile 内容
targets := a b c d
objects := $(foreach i,$(targets),$(i).o)
all:
    @echo $(targets)
    @echo $(objects)
# bash 中执行 make
$ make
a b c d
a.o b.o c.o d.o
````

##### 3.4.4 if

这里的`if`是个函数, 和前面的条件判断不一样, 前面的条件判断属于Makefile的关键字

````
$(if <condition>,<then-part>)
$(if <condition>,<then-part>,<else-part>)

````
eg:

````
# Makefile 内容
val := a
objects := $(if $(val),$(val).o,nothing)
no-objects := $(if $(no-val),$(val).o,nothing)
all:
    @echo $(objects)
    @echo $(no-objects)
# bash 中执行 make
$ make
a.o
nothing
````

##### 3.4.5 call 创建新的参数化函数

`$(call <expression>,<parm1>,<parm2>,<parm3>...)`

eg:

````
# Makefile 内容
log = "====debug====" $(1) "====end===="
all:
    @echo $(call log,"正在 Make")
# bash 中执行 make
$ make
====debug==== 正在 Make ====end====
````

##### 3.4.6 origin 判断变量的来源

`$(origin <variable>)`  
返回值有如下类型：

|类型|含义|
|:----|:----|
| `undefined` |`<variable>` 没有定义过|
| `default` |`<variable>` 是个默认的定义, 比如 CC 变量|
|`environment`|`<variable>` 是个环境变量, 并且 make时没有使用 -e 参数|
| `file` |`<variable>` 定义在Makefile中|
|`command line`|`<variable>` 定义在命令行中|
|`override`|`<variable>` 被 `override` 重新定义过|
|`automatic`|`<variable>` 是自动化变量|

eg:

````
# Makefile 内容
val-in-file := test-file
override val-override := test-override
all:
    @echo $(origin not-define)    # not-define 没有定义
    @echo $(origin CC)            # CC 是Makefile默认定义的变量
    @echo $(origin PATH)         # PATH 是 bash 环境变量
    @echo $(origin val-in-file)    # 此Makefile中定义的变量
    @echo $(origin val-in-cmd)    # 这个变量会加在 make 的参数中
    @echo $(origin val-override) # 此Makefile中定义的override变量
    @echo $(origin @)             # 自动变量, 具体前面的介绍
# bash 中执行 make
$ make val-in-cmd=val-cmd
undefined
default
environment
file
command line
override
automatic
````

##### 3.4.7 shell

`$(shell <shell command>)`

它的作用就是执行一个shell命令, 并将shell命令的结果作为函数的返回。 作用和`` `<shell command>` ``一样，注意 `` ` ``。

##### 3.4.8 make 控制函数

|函数|简介|功能|
|:----|:----|:----|
|`$(error <text ...>)`|产生一个致命错误|输出错误信息, 停止Makefile的运行|
|`$(warning <text ...>)`|输出警告|输出警告信息, Makefile继续运行|

#### 3.5 Makefile中一些约定俗成的伪目标

如果有过在Linux上, 从源码安装软件的经历的话, 就会对 make clean, make install 比较熟悉。像 clean, install 这些伪目标, 广为人知, 不用解释就大家知道是什么意思了。下面列举一些常用的伪目标, 如果在自己项目的Makefile合理使用这些伪目标的话, 可以让我们自己的Makefile看起来更专业：

|伪目标|含义|
|:----|:----|
|`all`|所有目标的目标，其功能一般是编译所有的目标|
|`clean`|删除所有被make创建的文件|
|`install `|安装已编译好的程序，其实就是把目标可执行文件拷贝到指定的目录中去|
|`print`|列出改变过的源文件|
|`tar`|把源程序打包备份. 也就是一个tar文件|
|`dist`|创建一个压缩文件, 一般是把tar文件压成Z文件. 或是gz文件|
|`TAGS`|更新所有的目标, 以备完整地重编译使用|
|`check 或 test`|一般用来测试makefile的流程|


引用:

* [Makefile 使用总结](https://www.cnblogs.com/wang_yb/p/3990952.html)
* [Makefile教程（绝对经典，所有问题看这一篇足够了）](https://blog.csdn.net/weixin_38391755/article/details/80380786)




