import json
import os
import tkinter as tk

import win32con

import QSpeedW as QSpeedW
import TkUtils as MyTK
import win32ui  # 引入模块


# 弹窗
import Window


class PopupDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('设置用户信息')
        self.parent = parent  # 显式地保留父窗口
        # 第一行（两列）
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text='QQ：', width=8).pack(side=tk.LEFT)
        self.QQ = tk.StringVar()
        tk.Entry(row1, textvariable=self.QQ, width=20).pack(side=tk.LEFT)
        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(row2, text='密码：', width=8).pack(side=tk.LEFT)
        self.password = tk.StringVar()
        tk.Entry(row2, textvariable=self.password, width=20).pack(side=tk.LEFT)
        # 第三行
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="取消", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(row3, text="确定", command=self.ok).pack(side=tk.RIGHT)

    def ok(self):
        # 显式地更改父窗口参数
        # self.parent.name = self.name.get()
        # self.parent.age = self.age.get()
        # # 显式地更新父窗口界面
        # self.parent.l1.config(text=self.parent.name)
        # self.parent.l2.config(text=self.parent.age)
        # self.destroy()  # 销毁窗口

        self.parent.add(self.QQ, self.password)
        self.destroy()

    def cancel(self):
        self.destroy()


def add(QQ, password):
    # lines = S_value.get()
    global qq_data_lines
    print(QQ.get() + "----" + password.get())
    qq_data_lines[QQ.get()] = password.get()
    write_qq_lines()


# 'All File(*.*)|*.*|' \
#         'Html File(*.html)|*.html|' \
#         'Image File(*.bmp .jpg .png)|*.png;*.jpg;*.bmp|' \
def select():
    global filename
    file_type = \
        'QSpeed File(*.exe .lnk)|*.exe;*.lnk|' \
        '|'
    api_flag = win32con.OFN_OVERWRITEPROMPT | win32con.OFN_FILEMUSTEXIST
    dlg = win32ui.CreateFileDialog(1, None, None, api_flag, file_type)  # 参数 1 表示打开文件对话框
    dlg.SetOFNInitialDir('%userprofile%')  # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename['path'] = dlg.GetPathName()  # 返回选择的文件路径和名称
    # 如果选择的是快捷方式 转换为真实地址
    if filename['path'].endswith(".lnk"):
        filename['path'] = Window.getTargetPath4Lnk(filename['path'])
    # print(filename)
    write_launch()


QQ_hwnd_map = {}


def change_hwnd(QQ):
    QSpeedW.change_speed(QQ_hwnd_map[QQ], root)


def login(user_name: str, password: str):
    global filename
    if len(filename['path']) == 0:
        print("请选择飞车启动路径")
        select()
    QSpeedW.login_window(filename['path'], user_name, password)


def write_launch():
    file = open(local_user_path + '\\launch.json', 'w')
    print('写入=>' + str(filename))
    # file.writelines(qq_data_lines)
    json.dump(filename, file)
    file.close()


def read_launch():
    global filename
    # 读取本地QQ&密码 没有则为空
    if not os.path.exists(local_user_path + '\\launch.json'):
        if not os.path.exists(local_user_path):
            print('初始化创建文件夹')
            os.mkdir(local_user_path)
        file = open(local_user_path + '\\launch.json', 'w')
        json.dump(filename, file)
        file.close()
    with open(local_user_path + '\\launch.json', "r") as f:
        filename = json.load(f)
        print('读取到文件路径: ' + str(filename))
        f.close()


def write_qq_lines():
    file = open(local_user_path + '\\QQ.json', 'w')
    print('写入=>' + str(qq_data_lines))
    # file.writelines(qq_data_lines)
    json.dump(qq_data_lines, file)
    file.close()
    read_qq_lines()


def read_qq_lines():
    global qq_data_lines
    # 读取本地QQ&密码 没有则为空
    if not os.path.exists(local_user_path + '\\QQ.json'):
        if not os.path.exists(local_user_path):
            print('初始化创建文件夹')
            os.mkdir(local_user_path)
        file = open(local_user_path + '\\QQ.json', 'w')
        json.dump(qq_data_lines, file)
        file.close()
    with open(local_user_path + '\\QQ.json', "r") as f:
        qq_data_lines = json.load(f)
        print('读取到: ' + str(qq_data_lines))
        f.close()
        show_qq_lines()


buttons = []


def remove(qq):
    global qq_data_lines
    qq_data_lines.pop(qq)
    write_qq_lines()


def show_qq_lines():
    # 重新铺按钮
    row = 1
    global QQ_hwnd_map
    QQ_hwnd_map = {}
    global buttons
    for b in buttons:
        b.destroy()
    buttons = []
    for qq in qq_data_lines.keys():
        button = tk.Button(root, command=lambda qq=qq: login(qq, qq_data_lines[qq]), text=qq,
                           width=100, height=1, padx=0, pady=0)
        button.place(x=50, y=row + (row - 1) * 30)
        button2 = tk.Button(root, command=lambda qq=qq: remove(qq), text='移除',
                            width=5, height=1, padx=0, pady=0)
        button2.place(x=1, y=row + (row - 1) * 30)
        buttons.append(button)
        buttons.append(button2)
        QQ_hwnd_map[qq_data_lines[qq]] = 0

        row += 1


# 设置参数
def setup_config(self):
    pw = PopupDialog(self)
    # 这一句很重要！！！
    self.wait_window(pw)
    return


env_dist = os.environ  # environ是在os.py中定义的一个dict environ = {}

# print(env_dist.get('APPDATA'))
# print(env_dist['JAVA_HOME'])
#
# # 打印所有环境变量，遍历字典
# for key in env_dist:
#     print(key + ' : ' + env_dist[key])

qq_data_lines = {}
print(os.path.abspath('%userprofile%'))
local_user_path = env_dist.get('APPDATA') + '\\..\\Local\\QSpeedAutoLogin'
filename = {'path': ''}
g_buttons = []
root = MyTK.create_window("上号器--by-easy", "750x400")
# 初始化飞车窗口按钮
MyTK.text(root, "tips: 1,选择启动路径 2, 添加QQ 3,直接点击QQ号上号", 300, 330)
tk.Button(root, command=lambda: select(), text=' 选择启动文件 ', padx=0, pady=0).place(x=1, y=360)
tk.Button(root, command=lambda: setup_config(root), width=8, text=' 添加账号 ', padx=0, pady=0).place(x=1, y=330)
root.add = add

# S_value = tk.StringVar()
# pyinstaller -F -w  -p ../../src --uac-admin -r ../../__init__.py,1 ../../AutoLogin.py
# S_value.trace('w', add)
# # S_value.set(0)
# E2_S = tk.Entry(root, bd=2, width=2, textvariable=S_value)
# E2_S.place(x=1, y=330)

# tk.Button(root, command=lambda: stop(), width=6, text=' 停止 ', padx=0, pady=0).place(x=64, y=330)
# g_q_s_window_map = show_speed_in_tk(root)
read_qq_lines()
read_launch()


def flush():
    global g_buttons_2
    g_buttons_2 = QSpeedW.flush(root, g_buttons_2)


g_buttons_2 = QSpeedW.show_speed_window(root)
buttonA = tk.Button(root, command=lambda: flush(), text=' 刷新 ', width=10, height=1, relief=tk.RAISED)
buttonA.place(x=5, y=240)

root.mainloop()
