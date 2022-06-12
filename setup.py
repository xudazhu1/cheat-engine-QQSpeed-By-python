import os
import shutil
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        ["src/Main.py",
         "src/BaseModuleAddrUtils.py",
         "src/CarMap.py",
         "src/ChangeUtils.py",
         "src/DriverUtil.py",
         "src/JsonUtils.py",
         "src/KeyCodeUtils.py",
         "src/MemoryUtils.py",
         "src/MemoryUtilsBack.py",
         "src/MyTread.py",
         "src/Run.py",
         "src/QSpeedW.py",
         "src/QunVer.py",
         "src/Qverify.py",
         "src/TkUtils.py",
         "src/UIUtils.py",
         "src/VersionControl.py",
         "src/Window.py",
         "src/Register.py",
         "src/FullDisplayMod.py",
         ]
        , build_dir="D:/project/my-python32/venv/Scripts/build/cython"
    ),  # add.py 为需要打包的文件名，不能包含中文
)

# 拷贝文件 BaseModuleAddrUtils.pyd
filepathapp = "D:\\project\\my-python32\\"
out = "D:\\project\\my-python32\\build\\"
files_1 = os.listdir(filepathapp)
for i in files_1:
    if i.endswith(".pyd"):
        so_file = filepathapp + i
        target = out + i
        target = target.replace(".cp37-win_amd64", "")
        # 文件移动或拷贝
        shutil.copy(so_file, target)

        os.remove(so_file)

        # # 3、删除原文件和生成的附属文件夹
        # files2 = os.listdir("./")
        # for file in files2:
        #     if file == dirPath or file.endswith(".c"):
        #         # 判断文件是否存在
        #         if (os.path.exists(file)):
        #             os.remove(file)
        #             print('移除后test 目录下有文件：%s' % file)
        #         else:
        #             print("要删除的文件不存在！")

    # 删除附属文件夹
    # try:
    #     shutil.rmtree(filePath3)
    # except Exception as ex:
    #     print("错误信息："+str(ex))#提示：错误信息，目录不是空的
    #
    # print("删除完成")
