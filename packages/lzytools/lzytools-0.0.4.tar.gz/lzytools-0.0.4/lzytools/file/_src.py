import ctypes
import os
import re
import shutil
import subprocess
import time
from typing import Union

import filetype
import send2trash
import win32com.client  # pywin32

from lzytools.general._src import create_random_string

# WINDOWS系统文件命名规则：文件和文件夹不能命名为“.”或“..”，也不能包含以下任何字符: \ / : * ? " < > |
_ILLEGAL_CHARACTERS = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']


def split_path(path: str):
    """拆分路径为父目录路径，文件名（不含文件扩展名），文件扩展名
    :param path: str，需要拆分的路径
    :return: 父目录路径，文件名（不含文件扩展名），文件扩展名"""
    if os.path.isfile(path):
        _temp_path, file_extension = os.path.splitext(path)
        parent_dirpath, filetitle = os.path.split(_temp_path)
    elif os.path.isdir(path):
        file_extension = ''
        parent_dirpath, filetitle = os.path.split(path)
    else:
        raise Exception('非法路径')

    return parent_dirpath, filetitle, file_extension


def is_legal_filename(filename: str) -> bool:
    """检查文件名是否符合Windows的文件命名规范
    :param filename: str，仅文件名（不含文件扩展名和文件父路径）
    """
    # 检查.（强制文件名不能以.开头）
    if filename[0] == '.':
        return False

    # 检查非法字符
    for key in _ILLEGAL_CHARACTERS:
        if key in filename:
            return False

    return True


def replace_illegal_filename(filename: str, replace_str: str = '') -> Union[str, bool]:
    """替换文件名中的非法字符串
    :param filename: str，仅文件名（不含文件扩展名和文件父路径）
    :param replace_str: str，用于替换的新字符
    """
    # 检查用于替换的字符是否属于非法字符
    if replace_str in _ILLEGAL_CHARACTERS:
        raise Exception(f'替换字符非法：{replace_str}')

    # 替换非法字符
    for word in _ILLEGAL_CHARACTERS:
        filename = filename.replace(word, replace_str)

    # 替换.（强制文件名不能以.开头）
    while filename[0] == '.':
        filename = filename[1:]

    filename = filename.strip()
    if not filename:
        raise Exception(f'结果文件名非法：{filename}')

    return filename


def reverse_path(path: str) -> str:
    """反转路径字符串，从后往前排列目录层级
    :param path: str，路径
    :return: str，重组后的路径字符串
    """
    path = os.path.normpath(path)
    _split_path = path.split('\\')
    path_reversed = ' \\ '.join(_split_path[::-1])
    path_reversed = os.path.normpath(path_reversed)
    return path_reversed


def delete_empty_folder(dirpath: str, send_to_trash: bool = True):
    """删除指定文件夹中的空文件夹（及其自身）
    :param dirpath: str，文件夹路径
    :param send_to_trash: bool，是否删除至回收站
    """
    _dirpaths = []

    # 提取所有文件夹路径
    for _dirpath, dirnames, filenames in os.walk(dirpath):
        _dirpaths.append(_dirpath)

    _dirpaths.insert(0, dirpath)  # 将其自身放于首位

    # 从后往前逐级删除
    for child_dirpath in _dirpaths[::-1]:
        if not os.listdir(child_dirpath):
            if send_to_trash:
                send2trash.send2trash(child_dirpath)
            else:
                os.rmdir(child_dirpath)


def delete(path: str, send_to_trash: bool = False) -> bool:
    """删除指定的文件/文件夹
    :param path: str，需要删除的路径
    :param send_to_trash: bool，是否删除至回收站
    :return: bool，是否成功删除"""
    if os.path.exists(path):
        try:
            if send_to_trash:
                send2trash.send2trash(path)
            else:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
            return True  # 成功执行删除操作的返回True
        except Exception as e:  # 报错PermissionError:文件被占用
            print(f'报错提示：{e}')
            return False
    return False


def is_hidden_file(path: str):
    """路径对应的文件是否隐藏
    :param path: str，需要删除的路径"""
    get_file_attributes_w = ctypes.windll.kernel32.GetFileAttributesW
    file_attribute_hidden = 0x2
    invalid_file_attributes = -1

    def is_hidden(_file):
        # 获取文件属性
        attrs = get_file_attributes_w(_file)
        if attrs == invalid_file_attributes:
            # 文件不存在或无法访问
            return False

        return attrs & file_attribute_hidden == file_attribute_hidden

    return is_hidden(path)


def get_dir_size(dirpath: str) -> int:
    """获取指定文件夹的总大小（字节byte）
    :param dirpath: str，文件夹路径
    :return: int，总大小（字节byte）"""
    _folder_size = 0
    for _dirpath, dirnames, filenames in os.walk(dirpath):
        for item in filenames:
            filepath = os.path.join(_dirpath, item)
            _folder_size += os.path.getsize(filepath)

    return _folder_size


def get_files_in_dir(dirpath: str) -> list:
    """获取文件夹中所有文件的路径
    :param dirpath: str，文件夹路径"""
    files = []
    for _dirpath, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            filepath_join = os.path.normpath(os.path.join(_dirpath, filename))
            files.append(filepath_join)

    return files


def get_folders_in_dir(dirpath: str) -> list:
    """获取文件夹中所有文件夹的路径
    :param dirpath: str，文件夹路径"""
    folders = []
    for _dirpath, dirnames, filenames in os.walk(dirpath):
        for dirname in dirnames:
            filepath_join = os.path.normpath(os.path.join(_dirpath, dirname))
            folders.append(filepath_join)

    return folders


def get_parent_dirpaths(path: str) -> list:
    """获取一个路径的所有上级目录路径
    :param path: str，文件/文件夹路径
    :return: list，所有上级目录列表，层级高的在前面"""
    parent_dirs = []

    while True:
        parent_dirpath, filename = os.path.split(path)
        if filename:
            parent_dirs.append(parent_dirpath)
        else:
            break

        path = parent_dirpath

    # 反转列表顺序，使得越上级目录排在越前面
    parent_dirs = parent_dirs[::-1]

    return parent_dirs


def guess_filetype(path) -> Union[str, None]:
    """判断文件类型
    :param path: str，文件路径"""
    if not os.path.isfile(path):
        return None

    kind = filetype.guess(path)
    if kind is None:
        return None

    type_ = kind.extension
    if type_:
        return type_
    else:
        return None


def get_first_multi_file_dirpath(dirpath: str) -> str:
    """找出文件夹中首个含多个下级文件/文件夹的文件夹路径（功能：解除套娃文件夹）
    :param dirpath: str，需要检查的文件夹路径
    :return: str，首个含多个下级文件/文件夹的文件夹路径
    """
    if not os.path.exists(dirpath):
        raise Exception("传入路径不存在")
    if not os.path.isdir(dirpath):
        raise Exception("传入路径不是文件夹")

    child_paths = os.listdir(dirpath)
    # 没有对空文件夹进行进一步检查
    if len(child_paths) == 1:  # 文件夹下级只有一个文件/文件夹
        child_path = os.path.normpath(os.path.join(dirpath, child_paths[0]))
        if os.path.isfile(child_path):  # 如果是文件，则直接返回结果
            return child_path
        else:  # 如果是文件夹，则递归
            return get_first_multi_file_dirpath(child_path)
    else:
        return dirpath


def is_dup_filename(filename: str, check_dirpath: str) -> bool:
    """检查文件名在指定路径中是否已存在（检查重复文件名）
    :param filename: str，文件名（包含文件扩展名）
    :param check_dirpath: str，需要检查的文件夹路径
    :return: bool，是否在指定文件夹中存在重复文件名
    """
    filenames_in_dirpath = [i.lower() for i in os.listdir(check_dirpath)]
    return filename.lower() in filenames_in_dirpath


def remove_suffix(filetitle: str, suffix: str = None) -> str:
    """提取无后缀的文件名（剔除（1）等后缀和自定义后缀）
    :param filetitle: str，文件名（不包含文件扩展名）
    :param suffix: str，自定义的后缀（若存在）
    :return: str，提取出的无后缀的文件名（不包含文件扩展名）"""
    # 剔除(1)等后缀
    filetitle = re.sub(r'\s*\(\d+\)\s*$', '', filetitle)
    # 剔除（1）等后缀
    filetitle = re.sub(r'\s*（\d+）\s*$', '', filetitle)
    # 剔除自定义后缀+数字的组合
    if suffix:
        filetitle = re.sub(rf'\s*{suffix}\s*\d+\s*$', '', filetitle)

    return filetitle.strip()


def create_nodup_filename_standard_digital_suffix(filetitle: str, check_dirpath: str,
                                                  filename_extension: str = None) -> str:
    """生成指定路径对应的文件在目标文件夹中非重复的文件名（统一数字后缀的文件名，(1)（1）等后缀）
    :param filetitle: str，文件名（不包含文件扩展名）
    :param filename_extension: str，文件扩展名（如果检查的文件名是文件的文件名，则必须使用该参数）
    :param check_dirpath: str，目标文件夹路径
    :return: str，非重复的文件名（包含文件扩展名）"""
    # 组合文件名
    if filename_extension.strip():
        filename = f'{filetitle}.{filename_extension.strip()}'  # 假设为文件的文件名
    else:
        filename = filetitle  # 假设为文件夹的文件名

    # 剔除后缀
    filetitle_filter = remove_suffix(filetitle)

    if filetitle_filter == filetitle:
        return filename
    else:
        # 检查重复文件名
        if is_dup_filename(filename, check_dirpath):
            # 生成无重复的文件名，按照Windows重复文件名规则，一直循环后缀编号累加，直到不存在重复文件名
            count = 1
            while True:
                # 组合文件名
                if filename_extension.strip():
                    filename = f'{filetitle} ({count}).{filename_extension.strip()}'  # 假设为文件的文件名
                else:
                    filename = f'{filetitle} ({count})'  # 假设为文件夹的文件名

                # 检查
                if is_dup_filename(filename, check_dirpath):
                    count += 1
                else:
                    break

        return filename


def create_nodup_filename_custom_suffix(filetitle: str, check_dirpath: str, add_suffix: str,
                                        filename_extension: str = None) -> str:
    """生成指定路径对应的文件在目标文件夹中非重复的文件名（可指定目标文件名）
    :param filetitle: str，文件名（不包含文件扩展名）
    :param filename_extension: str，文件扩展名（如果检查的文件名是文件的文件名，则必须使用该参数）
    :param check_dirpath: str，目标文件夹路径
    :param add_suffix: 存在重复文件名时在文件名后添加的后缀
    :return: str，非重复的文件名（包含文件扩展名）"""
    # 剔除原始后缀
    filetitle = remove_suffix(filetitle, add_suffix)

    # 组合文件名
    if filename_extension.strip():
        filename = f'{filetitle}.{filename_extension.strip()}'  # 假设为文件的文件名
    else:
        filename = filetitle  # 假设为文件夹的文件名

    # 检查重复文件名
    if is_dup_filename(filename, check_dirpath):
        # 生成无重复的文件名，一直循环后缀编号累加，直到不存在重复文件名
        count = 1
        while True:
            # 组合文件名
            if filename_extension.strip():
                filename = f'{filetitle}{add_suffix}{count}.{filename_extension.strip()}'  # 假设为文件的文件名
            else:
                filename = f'{filetitle}{add_suffix}{count}'  # 假设为文件夹的文件名

            # 检查
            if is_dup_filename(filename, check_dirpath):
                count += 1
            else:
                break

    return filename


def get_shortcut_target_path(shortcut_path: str) -> str:
    """获取快捷方式指向的路径
    :param shortcut_path: str，快捷方式路径
    :return: 快捷方式指向的路径"""
    try:
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        return shortcut.Targetpath
    except Exception as e:
        raise f'报错提示：{e}'


def set_hidden_attrib(path: str, is_hidden: bool = False) -> bool:
    """设置文件/文件及的隐藏属性
    :param path: str，文件/文件夹路径
    :param is_hidden: bool，是否隐藏文件/文件夹
    :return: bool，True为显示，False为隐藏"""
    if is_hidden:
        subprocess.run(['attrib', '+h', path])
        return False
    else:
        subprocess.run(['attrib', '-h', path])
        return True


def release_nesting_folder(check_path: str, target_dirpath: str) -> str:
    """解除套娃文件夹，将最深一级的非单层文件/文件夹移动至指定文件夹
    :param check_path: str，需要检查的路径
    :param target_dirpath: str，移动的目标文件夹
    :return: str，最终移动后的路径
    """
    if not os.path.exists(check_path):
        raise Exception('路径不存在')

    # 如果目标文件夹不存在，则新建该文件夹
    if not os.path.exists(target_dirpath):
        os.makedirs(target_dirpath)

    if not os.path.isdir(target_dirpath):
        raise Exception(f'传入文件夹参数错误，【{target_dirpath}】不是文件夹路径')

    # 提取需要移动的路径（如果传参是文件，则直接为该路径，如果传参是文件夹，则为最深一级非单层文件夹
    if os.path.isfile(check_path):
        need_move_path = check_path
    else:
        need_move_path = get_first_multi_file_dirpath(check_path)

    # 检查需要移动的路径是否和目标文件夹一致，如果一致，则不需要进行移动
    if need_move_path == target_dirpath:
        return need_move_path

    # 提取原始文件名，生成目标文件夹下无重复的文件夹名
    parent_dirpath, filetitle, file_extension = split_path(need_move_path)
    nodup_filename = create_nodup_filename_standard_digital_suffix(filetitle, target_dirpath, file_extension)

    # 移动前先重命名
    move_path_renamed = need_move_path
    _origin_filename = f'{filetitle}.{file_extension.strip(".")}'
    if nodup_filename == _origin_filename:  # 如果该文件名与原文件名一致，则不需要进行重命名
        pass
    else:  # 否则，先重命名为随机文件名（防止同目录存在重复文件名）
        _random_filename = f'{create_random_string()}.{create_random_string(4)}'
        _path_with_random_filename = os.path.normpath(os.path.join(parent_dirpath, _random_filename))
        move_path_renamed = _path_with_random_filename
        # 重命名时会遇到权限问题导致报错
        try:
            os.rename(need_move_path, _path_with_random_filename)
        except PermissionError:  # PermissionError: [WinError 5] 拒绝访问。尝试等待0.2秒后再次重命名
            time.sleep(0.2)
            try:
                os.rename(need_move_path, _path_with_random_filename)
            except Exception as e:
                raise e

    # 再进行移动
    try:
        shutil.move(move_path_renamed, target_dirpath)
    except OSError:  # OSError: [WinError 145] 目录不是空的。原始文件夹下有残留文件夹，如果为空则尝试直接删除
        delete_empty_folder(move_path_renamed)

    # 拼接最终路径
    final_path = os.path.normpath(os.path.join(target_dirpath, nodup_filename))
    delete_empty_folder(check_path)  # 如果原始文件夹为空，则直接删除

    return final_path
