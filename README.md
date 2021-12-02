# cheat-engine-QQSpeed-By-python  
cheat engine QQSpeed By python  

#### Main  test_python.py  
### to exe Script  
```
# 1. 加密
python setup.py build_ext --inplace
# 2. 加密打包
pyinstaller -F -w -p ./build --add-data=./dll/ChangeQS.dll;. --add-data=./dll/cars1.json;. ^
--uac-admin -r ./test_python.exe.manifest,1 ./start.py
# 3. 加壳打包
pyinstaller -F -w -p ./build --add-data=D:/project/my-python32/dist/start.exe;. ^
--uac-admin -r ./test_python.exe.manifest,1 ./startO.py
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
##### QQ飞车改车2.8.x 更新日志:
: 优化10020精准命中 以减少崩溃情况的发生
##### QQ飞车改车2.9.x 更新日志:
: 优化普通赛车代码精准命中 大大减少崩溃情况的发生
##### QQ飞车改车2.12.1 更新日志:
: 增加群验证 QQ扫码验证是否在群里
: pyd编译加密 防止反编译
: 加壳让每次运行的md5不一致, 防止大片封号


