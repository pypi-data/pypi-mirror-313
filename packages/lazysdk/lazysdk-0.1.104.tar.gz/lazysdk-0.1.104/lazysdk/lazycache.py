import os
import sys

ROOT_FOLDER_NAME = ".lazysdk"
cache_root = "cache"
DEFAULT_PROJECT_ROOT_CACHE_PATH = os.path.join(sys.path[0], ROOT_FOLDER_NAME)  # 当前项目路径
DEFAULT_USER_HOME_CACHE_PATH = os.path.join(os.path.expanduser("~"), ROOT_FOLDER_NAME)  # 用户文件夹下的缓存
default_cache_directory = os.path.join(DEFAULT_USER_HOME_CACHE_PATH, cache_root)  # 默认用户缓存文件夹


def user_cache_path(folder_name: str = ".cache"):
    """
    返回用户缓存文件夹路径
    """
    return os.path.join(os.path.expanduser("~"), folder_name)
