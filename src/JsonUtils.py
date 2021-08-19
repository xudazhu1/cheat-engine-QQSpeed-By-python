import os
import json

env_dist = os.environ  # environ是在os.py中定义的一个dict environ = {}
local_user_path = env_dist.get('APPDATA') + '\\..\\Local\\ChangeQQSpeed'


def write_file(strTemp, fileName):
    file = open(fileName, 'w')
    print('写入=>' + str(strTemp))
    # file.writelines(qq_data_lines)
    file.write(strTemp)
    file.close()
    # read_ids()


def write_ids(ids):
    file = open(local_user_path + '\\Id.json', 'w')
    print('写入=>' + str(ids))
    # file.writelines(qq_data_lines)
    json.dump(ids, file)
    file.close()
    # read_ids()


def read_ids():
    ids = {}
    # 读取本地QQ&密码 没有则为空
    if not os.path.exists(local_user_path + '\\Id.json'):
        if not os.path.exists(local_user_path):
            print('初始化创建文件夹')
            os.mkdir(local_user_path)
        file = open(local_user_path + '\\Id.json', 'w')
        json.dump(ids, file)
        file.close()
    with open(local_user_path + '\\Id.json', "r") as f:
        ids = json.load(f)
        print('读取到: ' + str(ids))
        f.close()
    return ids
