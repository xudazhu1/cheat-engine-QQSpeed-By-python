import os
import json

env_dist = os.environ  # environ是在os.py中定义的一个dict environ = {}
local_user_path = env_dist.get('APPDATA') + '\\..\\Local\\ChangeQQSpeed'
if not os.path.exists(local_user_path):
    print('初始化创建文件夹')
    os.mkdir(local_user_path)


def getProGramPath():
    return local_user_path


def write_file_on_this(jsonTemp, fileName):
    # 写入数据 没有则为空 为空时新建文件
    if not os.path.exists(local_user_path + '\\' + fileName):
        file = open(local_user_path + '\\' + fileName, 'w')
        file.close()

    file = open(local_user_path + '\\' + fileName, 'w')
    print('写入=>' + str(jsonTemp))
    # file.writelines(qq_data_lines)
    # file.write(strTemp)
    json.dump(jsonTemp, file)
    file.close()
    # read_ids()


def read_file_on_this(fileName):
    data = {}
    # 读取本地QQ&密码 没有则为空
    if not os.path.exists(local_user_path + '\\' + fileName):
        file = open(local_user_path + '\\' + fileName, 'w')
        json.dump(data, file)
        file.close()
    with open(local_user_path + '\\' + fileName, "r") as f:
        data = json.load(f)
        print('读取到: ' + str(data))
        f.close()
    return data


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
        file = open(local_user_path + '\\Id.json', 'w')
        json.dump(ids, file)
        file.close()
    with open(local_user_path + '\\Id.json', "r") as f:
        ids = json.load(f)
        print('读取到: ' + str(ids))
        f.close()
    return ids
