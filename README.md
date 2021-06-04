# cheat-engine-QQSpeed-By-python  
cheat engine QQSpeed By python  

main  test_python.py  
to exe Script  
# pyinstaller -F -p ../../src --add-data=../../dll/FileDriver.sys;. --uac-admin -r ../../test_python.exe.manifest,1 ../../test_python.py  

~~use python 2.7 win32 pyinstaller 3.6~~ python3.9 win64

QQ飞车改车2.6.1 更新日志:  
 : 修复2.6版本中由于32位升级到64位内存值变量类型不匹配造成的修改失败的问题  
  
QQ飞车改车2.6 更新日志:   
 : python2.7 win32 改为 python3.9 win64  
 : 使用多线程优化搜索内存值的速度 提高大概1/3的速度  
