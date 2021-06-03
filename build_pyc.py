# 将python3项目编译为pyc文件
# python环境中

# 单文件
import py_compile

# py_compile.compile(r'D:\Project.py') # 绝对路径

# 多文件
import compileall

# 绝对路径
compileall.compile_dir(r'D:\project\my-python32\src')

# 运行主程序发现pyc文件 导包错误
# 解决方法
# 1. 将所有__pycache__目录的pyc文件全部粘贴到当前目录
# 2. 将所有pyc文件后缀改为与目录中的pyc文件相同名字 如: test.cpython-37.pyc  -->> test.pyc
# 3. 将所有py文件删除

#运行主程序

# pyc文件反编译
# pip install uncompyle6
# uncompyle6.exe test.pyc