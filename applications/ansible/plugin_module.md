# difference

module 可以通过ansible API, command 和 playbook 调用
>https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#modules-and-plugins-what-s-the-difference
If you’re writing a new module, you can choose any programming language you like.

## python
当 module 是 Python 实现的时, 模块执行前, 会把模块文件和它依赖的`ansible.module_utils`下的文件, 以及传递模块参数的一些样板文件,打包到一个 zipfile里,然后使用Base64编码, 用一个Python 脚本包裹这段编码后的文件.

Python 脚本在远端管理机上decode zipfile, 解压到一个临时目录,设置PYTHONPATH找到模块,然后调用python执行模块.

## Non-native want JSON module
模块是一个能自执行的脚本文件, 文件里必须包含字符串 `WANT_JSON`, ansible 会把模块参数以JSON形式写入一个临时文件,执行这个脚本文件,
脚本文件的命令行只有一个参数, 就是临时文件的文件名, 模块开发者需要自己打开文件,解析里面的JSON内容.


## 二进制 module

传参方式和 want JSON module 一样, 
一个 go 实现,https://github.com/ansible/ansible/blob/devel/test/integration/targets/binary_modules/library/helloworld.go

## 命令行参数
python 模块是通过读取 stdin JSON 字符串,然后由模块里的 AnsibleModule 来解析, 存到 params 属性上.

# pipeling
只支持Python module, 从远端 python stdin 传入代码,而不是zipfile 解压,  

# refs
https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html
