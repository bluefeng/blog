#构建 README.md
import os

lines = ['# 个人所有博客内容同步更新\n\n\n',]

blogs = {}

def doAllFile(path, parent):
	fl = os.listdir(path)
	for tempP in fl :
		cpath = os.path.join(path, tempP)
		if os.path.isdir(cpath) and not tempP.find('.') == 0:
			parent[tempP] = {}
			doAllFile(cpath, parent[tempP])
		elif os.path.isfile(cpath) and tempP.find('README') == -1 and os.path.splitext(tempP)[1] == ".md" :
			parent["files"] = parent.get("files", [])
			parent["files"].append(os.path.splitext(tempP)[0])
	
doAllFile("./", blogs)

def parseBlog(values, depth, root):
	if "files" in values :
		for one in values["files"] :
			lines.append('* [{}]({}{}.md)  \n'.format(one, root, one))
		del values["files"]
	for path, item in values.items():
		if item:
			lines.append('\n' + '#' * depth + ' ' + path + '  \n\n')
			parseBlog(item, depth + 1, root + path + "/")

parseBlog(blogs, 3, "https://github.com/bluefeng/blog/blob/master/")


lines.append('\n转载请注明出处: [http://www.heryc.fun](http://www.heryc.fun) \n')

with open('./README.md', 'w') as file:
	file.writelines( lines )


