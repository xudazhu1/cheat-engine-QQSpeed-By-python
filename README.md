# cheat-engine-QQSpeed-By-python  
cheat engine QQSpeed By python  

#### Main  test_python.py  
### to exe Script  
```
pyinstaller -F -p ../../src --add-data=../../dll/FileDriver.sys;. --uac-admin -r ../../test_python.exe.manifest,1 ../../test_python.py  
```
~~use python 2.7 win32 pyinstaller 3.6~~ python3.7 win64

##### QQ飞车改车2.6.1 更新日志:  
 : 修复2.6版本中由于32位升级到64位内存值变量类型不匹配造成的修改失败的问题  
  
##### QQ飞车改车2.6 更新日志:   
 : python2.7 win32 改为 python3.9 win64  
 : 使用多线程优化搜索内存值的速度 提高大概1/3的速度  

##### QQ飞车改车2.7 更新日志:  
 : 更新改车ID填写UI 现在可以直接选车  
 : 使用友站的车子接口 动态获取车子( ﹁ ﹁ ) ~→  
 : 记住改车ID 下次打开软件还在  
##### QQ飞车改车2.7.1 更新日志:  
: 由py3.9.5改成py3.7.8 解决3.9.5打包依赖c++出现分电脑打不开的问题
##### QQ飞车改车2.7.2 更新日志:
: 优化10020代码数量大于600时候的命中代码逻辑
##### QQ飞车改车2.7.3 更新日志:
: 优化10020代码数量大于1000时候的命中代码逻辑, 增加模式1(老逻辑), 模式2(直接改一半10020), 模式3(全部10020)


