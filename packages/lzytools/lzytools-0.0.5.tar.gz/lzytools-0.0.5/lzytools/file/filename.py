from typing import Union

from lzytools.file import _src


def is_legal_filename(filename: str) -> bool:
    """检查文件名是否符合Windows的文件命名规范
    :param filename: str，仅文件名（不含文件扩展名和文件父路径）
    """
    return _src.is_legal_filename(filename)


def replace_illegal_filename(filename: str, replace_str: str = '') -> Union[str, bool]:
    """替换文件名中的非法字符串
    :param filename: str，仅文件名（不含文件扩展名和文件父路径）
    :param replace_str: str，用于替换的新字符
    """
    return _src.replace_illegal_filename(filename, replace_str)


def is_dup_filename(filename: str, check_dirpath: str) -> bool:
    """检查文件名在指定路径中是否已存在（检查重复文件名）
    :param filename: str，文件名（包含文件扩展名）
    :param check_dirpath: str，需要检查的文件夹路径
    :return: bool，是否在指定文件夹中存在重复文件名
    """
    return _src.is_dup_filename(filename, check_dirpath)


def remove_suffix(filetitle: str, suffix: str = None) -> str:
    """提取无后缀的文件名（剔除（1）等后缀和自定义后缀）
    :param filetitle: str，文件名（不包含文件扩展名）
    :param suffix: str，自定义的后缀（若存在）
    :return: str，提取出的无后缀的文件名（不包含文件扩展名）"""
    return _src.remove_suffix(filetitle, suffix)


def create_nodup_filename_standard_digital_suffix(filetitle: str, check_dirpath: str,
                                                  filename_extension: str = None) -> str:
    """生成指定路径对应的文件在目标文件夹中非重复的文件名（统一数字后缀的文件名，(1)（1）等后缀）
    :param filetitle: str，文件名（不包含文件扩展名）
    :param filename_extension: str，文件扩展名（如果检查的文件名是文件的文件名，则必须使用该参数）
    :param check_dirpath: str，目标文件夹路径
    :return: str，非重复的文件名（包含文件扩展名）"""
    return _src.create_nodup_filename_standard_digital_suffix(filetitle, check_dirpath, filename_extension)


def create_nodup_filename_custom_suffix(filetitle: str, check_dirpath: str, add_suffix: str,
                                        filename_extension: str = None) -> str:
    """生成指定路径对应的文件在目标文件夹中非重复的文件名（可指定目标文件名）
    :param filetitle: str，文件名（不包含文件扩展名）
    :param filename_extension: str，文件扩展名（如果检查的文件名是文件的文件名，则必须使用该参数）
    :param check_dirpath: str，目标文件夹路径
    :param add_suffix: 存在重复文件名时在文件名后添加的后缀
    :return: str，非重复的文件名（包含文件扩展名）"""
    return _src.create_nodup_filename_custom_suffix(filetitle, check_dirpath, add_suffix, filename_extension)
