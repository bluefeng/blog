## 关于Git

Git的介绍，以及Git常用命令 以及自己搭建Git服务器的方法

### 分布式版本控制

Git属于**分布式**版本控制系统，svn属于*集中式*。
  
集中式版本控制只有一分代码，每个人电脑上有一份完整备份。  
集中式存在安全问题，中心服务器挂掉就*GG*了。

分布式版本控制，每个人电脑上都有一个版本控制系统。然后和中心服务器进行交互。

### 新建Git仓库

#### 在工作目录中初始化新仓库

在项目所在目录执行`git init`，初始化后，在当前目录下会出现一个名为 .Git 的目录，所有 Git 需要的数据和资源都存放在这个目录中。

#### 从现有仓库克隆

Git 支持许多数据传输协议，可以使用 `git://`Git协议或者 `http(s)://`http协议或者 `user@server:/path.git`ssh协议进行传输。eg：

```
git clone git://path.git
git clone http://path.git
git clone user@server:/path.git
```
可以使用`-b name`来指定要克隆的分支名。克隆master分支：

```
git clone -b master user@server:/path.git
```

### 工作流

#### 工作区 --> stage(暂存区) --> branch(版本树) *--> origin(远端版本树)*

```
git add file 把工作区中的文件修改添加到暂存区
git commit 把暂存区的修改打包为一个节点，提交到当前分支
git reset HEAD  --file 使用当前分支的内容覆盖暂存区，撤销 git add，不指定file 回退add的所有文件
git checkout --file 使用暂存区的修改覆盖工作区的修改，撤销未对尚未add修改。
```
#### 跳跃暂存区进行操作

```
git commit -a  相当于 git add + git commit
git checkout HEAD --file 取出最后一次修改，直接放在工作区
```

对文件的操作，如果路径输入`.`表示对所有文件执行操作

### 节点

每一个节点的是单次提交相对于上个节点改变的所有文件的集合，拥有的是这些文件副本的指针。使用`git commit`新建节点。


### 分支

分支类似于链表结构，每一个节点通过指针链接成一条线，HEAD指针指向当前分支的指针。   
每次提交新的节点会让当前分支指针向前移动，而其他分支指针并不会移动。可以使用`git checkout branchName`切换HEAD指向的分支(当前分支)。使用`git branch`查看所有本地分支。

#### 新建

新建分支就是新建一个指针指向当前分支线的最后一个节点。 可以使用`git branch newBranch`或者`git checkout -b newBranch`新建分支，后者会在信件后让HEAD指针指向新分支，让新分支成为当前分支。新建分支后使用`git push <远程主机名> <本地分支名>:<远程分支名>`推送到远程。

#### 合并

两个分支合并使用`git merge branchName`会产生合并操作

##### Fast forward

"快进式合并"*(fast-farward merge)*，当当前分支到需要合并的分支没有岔路，只是先后关系，会将当前分支的指针直接移动到需要合并分支的头部，分支信息上不存在合并的信息。如果需要合并的信息可以使用`--no-ff`参数禁用Fast forward模式，并使用`-m`参数产生一个新的commit节点：  

`git merge --no-ff -m "merge message" branchName`  

##### 冲突

当两个分支在分开之后各自分别修改过同一个文件，在合并的时候就会产生冲突，对于冲突的产生原理是，回溯两个分支找到最近的一个公共父节点，然后比较当前分支头部的文件与这个父节点的差异文件，然后进行筛选，不能自动合并的文件就会产生冲突，冲突文件形如：

```
<<<<<<< HEAD
abcdef.
=======
hsdgasd.
>>>>>>> other
```
Git会使用`<<<<<<<`,`=======`,`>>>>>>>`分隔并标记处不同分支的内容，只需手动进行修改后，重新`git add file`就可以解决。

#### 储藏(Stashing)

在一个分支进行修改但是未提交时需要切换到其他分支进行操作的时候，可以将当前分支修改的内容使用`git stash`储藏起来，工作完成之后，切换回原分支，使用`git stash apply`即可以将储藏的修改恢复到工作区。

### .gitignore文件

Git仓库忽略的文件列表，支持正则表达试。

### 远程仓库

与远程仓库同步，和本地分支合并类似。使用`git branch -r`查看远程的分支名。

- 使用`git pull`命令拉取远程分支内容，`git pull`包含了两步操作`git fetch`和`git merge`，`git fetch`抓取远端的更新内容，`git merge`合并远端的内容和本地的内容，此时如果自己进行过提交会产生冲突，和本地分支合并的操作是一样的。如果运行`git pull`提示找不到对应的远程分支，可以使用如下命令关联本地和远程分支：  

```
#关联本地和远程分支
git branch --set-upstream-to=<远程主机名>/<远程分支名> <本地分支名>
#pull
git pull <远程主机名> <远程分支名>:<本地分支名>
#eg:
git pull origin master:master
```

- 使用`git push`命令将当前分支推送到远端，因为冲突解决只在用户本地解决，所以本地分支落后于远端分支时需要先使用`git pull`拉取远端内容并解决冲突。

```
#push
git push <远程主机名> <本地分支名>:<远程分支名>
#没有本地分支名 相当于删除远程分支
git push <远程主机名> :<远程分支名>
#⬆️等价于⤵️
git push origin --delete <远程分支名>

```

更多命令行见：

![](http://www.heryc.fun/media/blog/20190316/abc.jpg)

###自建远程仓库

一切操作在自己的远程**Linux**服务器上

1. 安装Git  
```
yum install git
```

2. 创建`git`用户， 运行`git`服务  
```
sudo adduser git
```

3. 创建证书登录， 收集需要登录的用户的公钥*(`id_rsa.pub`文件)* 导入到 `/home/git/.shh/authorized_keys`文件中。

4. 初始化Git仓库，选定一个目录作为Git仓库，假定是`/mygit/hello.git`,在`/mygit`目录输入*(--bare 用来创建裸仓库，没有工作区，只是用于共享历史版本，不能修改工作区。服务器上的Git仓库通常以`.git`结尾)*：
```
sudo git init --bare hello.git
```

5. 把仓库的owner改为`git`  
```
sudo chown -R git:git hello.git
```

6. 安全考虑，最好不允许`git`用户登陆`shell`，可以通过编辑`/etc/passwd`文件完成。找到类似下面的一行：  
```
git:x:1001:1001:,,,:/home/git:/bin/bash
```   
改为：  
```
git:x:1001:1001:,,,:/home/git:/usr/bin/git-shell
```   
这样，`git`用户可以通过ssh使用Git,但是无法登陆shell。为`git`指定的`git-shell`每次登陆就会自动退出。

7. 使用`git clone`克隆自己的远程仓库  
```
git clone git@host:/mygit/hello.git
```   
如果自己的`ssh`端口号不是默认的`22`,可以使用： 
```
git clone ssh://git@host:port/mygit/hello.git
```


更多内容：  
[git-scm/book](https://git-scm.com/book/zh "Title")   
[廖雪峰博客](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000 "Title") 