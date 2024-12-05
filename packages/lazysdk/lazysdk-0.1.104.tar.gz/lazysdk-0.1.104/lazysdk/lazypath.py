#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
import subprocess
import platform
import shutil
import sys
import os
import filetype
current_user_path = os.path.abspath('.')
if platform.system() == 'Windows':
    path_separator = '\\'
else:
    path_separator = '/'


def make_path(
        path: str = None,
        overwrite: bool = False
) -> bool:
    """
    创建目录
    """
    if path is None:
        return False
    else:
        if overwrite:
            delete(path_or_file=path)
        os.makedirs(name=path, exist_ok=True)
        return True


def make_data_path(
        file_name: str
):
    file_name = os.path.basename(file_name).replace(".py", "")
    path = os.path.join('data', file_name)
    if os.path.exists(path) is True:
        pass
    else:
        make_path("data")
        os.mkdir(path)
    return path


def project_path(
        project_name
):
    # 获取项目的根目录，需要输入项目名称
    cur_path = os.path.abspath(os.path.dirname(__file__))
    _project_path = cur_path[:cur_path.find("%s%s" % (project_name, path_separator)) + len("%s%s" % (project_name, path_separator))]
    return _project_path


def file_path(__file__):
    """
    os.path.dirname(os.path.abspath(__file__))  单纯的文件地址
    os.path.dirname(os.path.realpath(__file__))  可能会存在的文件指向的真实地址
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_all_top_dir():
    """
    枚举当前文件所处的文件夹的所有明细路径
    """
    file_dir = sys.argv[0]
    dir_list = file_dir.split(path_separator)
    dir_list_length = len(dir_list)
    new_dir_list = list()
    for i in range(dir_list_length):
        dir_list.pop(dir_list_length - i - 1)
        if len(dir_list) > 0:
            temp_dir = path_separator.join(dir_list)
            if len(temp_dir) > 0:
                new_dir_list.append(temp_dir)
            else:
                continue
        else:
            continue
    return new_dir_list


def visit_dir(
        path
):
    total_size = 0
    file_num = 0
    dir_num = 0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        # print(sub_path)
        if os.path.isfile(sub_path):
            file_num = file_num+1
            # print(fileNum)# 统计文件数量
            total_size = total_size+os.path.getsize(sub_path)  # 文件总大小
        elif os.path.isdir(sub_path):
            dir_num = dir_num+1  # 统计文件夹数量
            visit_dir(sub_path)  # 递归遍历子文件夹
    return file_num


def file_list(
        file_dir=os.path.dirname(os.path.realpath(__file__)),
        with_path=False
):
    """
    对某个路径枚举路径下的文件列表
    """
    dir_file_list = os.listdir(file_dir)
    if with_path:
        dir_file_list_f = list()
        for each in dir_file_list:
            dir_file_list_f.append(os.path.join(file_dir, each))
        return dir_file_list_f
    else:
        return dir_file_list


def open_path(path):
    """
    打开某个路径/文件
    """
    if platform.system() == 'Windows':
        os.startfile(path)  # Windows上打开文件
    else:
        subprocess.check_call(['open', path])  # 非Windows上打开文件


def path_clean(content):
    """
    清除路径前后可能出现的引号
    """
    if content[0] == '"' and content[-1] == '"':
        content = content[1:-1]
    elif content[0] == '“' and content[-1] == '”':
        content = content[1:-1]
    elif content[0] == "'" and content[-1] == "'":
        content = content[1:-1]
    else:
        pass
    return content


def file_info(
        file
):
    """
    获取文件信息
    """
    res = dict()
    res['file'] = file
    res['path_exists'] = os.path.exists(file)  # 文件/路径是否存在
    if os.path.exists(file):
        # 文件存在，继续获取详细信息
        create_time = os.path.getctime(file)
        if os.path.isdir(file):
            res['path_type'] = 'dir'
            res['path_name'] = os.path.basename(file)
        elif os.path.isfile(file):
            res['path_type'] = 'file'
            res['file_name'] = os.path.basename(file)
            guess_kind = filetype.guess(file)  # 猜测文件类型
            if guess_kind:
                res['file_extension'] = guess_kind.extension  # 后缀名，例如：mp4
                res['file_type'] = guess_kind.mime  # 文件类型，例如：video/mp4
        else:
            res['path_type'] = ''

        res['path_isabs'] = os.path.isabs(file)  # 是否为绝对路径
        res['size'] = os.path.getsize(file)  # 获取大小
        res['dir_name'] = os.path.dirname(file)  # 上层目录名
    else:
        # 文件不存在
        pass
    return res


def delete(path_or_file):
    """
    删除目录/文件
    """
    if os.path.exists(path_or_file):
        if os.path.isdir(path_or_file):
            shutil.rmtree(path_or_file)
        else:
            os.remove(path_or_file)
    else:
        return


def get_folder_name(dir_or_path: str):
    """
    获取文件夹名称
    """
    if os.path.isdir(dir_or_path):
        # 这里多做一步处理，避免有可能路径后面再有个路径分割符号不能识别的情况
        return os.path.basename(os.path.abspath(dir_or_path))
    elif os.path.isfile(dir_or_path):
        tmp_dir = os.path.dirname(dir_or_path)
        return os.path.basename(tmp_dir)
    else:
        return


def path_rename(
        folder_path,
        new_folder_name
):
    """
    文件夹重命名
    """
    if os.path.isdir(folder_path):
        second_last_path, last_path = os.path.split(os.path.abspath(folder_path))
        new_path = os.path.join(second_last_path, new_folder_name)
        os.rename(folder_path, new_path)
        return new_path
    else:
        return


def exe_path():
    """
    获取当前脚本的绝对路径
    """
    return os.path.dirname(os.path.realpath(sys.argv[0]))
