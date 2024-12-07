import os
from typing import Union

from pptools.file import _src


def reverse_path(path: str) -> str:
    """反转路径字符串，从后往前排列目录层级
    :param path: str，路径
    :return: str，重组后的路径字符串
    """
    return _src.reverse_path(path)


def delete_empty_folder(dirpath: str, send_to_trash: bool = True):
    """删除指定文件夹中的空文件夹（及其自身）
    :param dirpath: str，文件夹路径
    :param send_to_trash: bool，是否删除至回收站
    """
    return _src.delete_empty_folder(dirpath, send_to_trash)


def delete(path: str, send_to_trash: bool = False) -> bool:
    """删除指定的文件/文件夹
    :param path: str，需要删除的路径
    :param send_to_trash: bool，是否删除至回收站
    :return: bool，是否成功删除"""
    return _src.delete(path, send_to_trash)


def is_hidden_file(path: str):
    """路径对应的文件是否隐藏
    :param path: str，需要删除的路径"""
    if not os.path.exists(path):
        raise Exception(f'路径不存在：{path}')

    return _src.is_hidden_file(path)


def get_size(path: str):
    """获取指定文件/文件夹的总大小（字节byte）
    :param path: str，文件/文件夹路径
    :return: int，总大小（字节byte）"""
    if not os.path.exists(path):
        raise Exception(f'路径不存在：{path}')

    if os.path.isdir(path):
        return _src.get_dir_size(path)
    elif os.path.isfile(path):
        return os.path.getsize(path)


def get_files_in_dir(dirpath: str) -> list:
    """获取文件夹中所有文件的路径
    :param dirpath: str，文件夹路径"""
    return _src.get_files_in_dir(dirpath)


def get_folders_in_dir(dirpath: str) -> list:
    """获取文件夹中所有文件夹的路径
    :param dirpath: str，文件夹路径"""
    return _src.get_folders_in_dir(dirpath)


def get_parent_dirpaths(path: str) -> list:
    """获取一个路径的所有上级目录路径
    :param path: str，文件/文件夹路径
    :return: list，所有上级目录列表，层级高的在前面"""
    return _src.get_parent_dirpaths(path)


def guess_filetype(path) -> Union[str, None]:
    """判断文件类型
    :param path: str，文件路径"""
    return _src.guess_filetype(path)


def get_first_multi_file_dirpath(dirpath: str) -> str:
    """找出文件夹中首个含多个下级文件/文件夹的文件夹路径（功能：解除套娃文件夹）
    :param dirpath: str，需要检查的文件夹路径
    :return: str，首个含多个下级文件/文件夹的文件夹路径
    """
    return _src.get_first_multi_file_dirpath(dirpath)


def split_path(path: str):
    """拆分路径为父目录路径，文件名（不含文件扩展名），文件扩展名
    :param path: str，需要拆分的路径
    :return: 父目录路径，文件名（不含文件扩展名），文件扩展名"""
    return _src.split_path(path)


def get_shortcut_target_path(shortcut_path: str) -> str:
    """获取快捷方式指向的路径
    :param shortcut_path: str，快捷方式路径
    :return: 快捷方式指向的路径"""
    return _src.get_shortcut_target_path(shortcut_path)


def set_hidden_attrib(path: str, is_hidden: bool = False) -> bool:
    """设置文件/文件及的隐藏属性
    :param path: str，文件/文件夹路径
    :param is_hidden: bool，是否隐藏文件/文件夹
    :return: bool，True为显示，False为隐藏"""
    return _src.set_hidden_attrib(path, is_hidden)


def release_nesting_folder(check_path: str, target_dirpath: str) -> str:
    """解除套娃文件夹，将最深一级的非单层文件/文件夹移动至指定文件夹
    :param check_path: str，需要检查的路径
    :param target_dirpath: str，移动的目标文件夹
    :return: str，最终移动后的路径
    """
    return _src.release_nesting_folder(check_path, target_dirpath)
