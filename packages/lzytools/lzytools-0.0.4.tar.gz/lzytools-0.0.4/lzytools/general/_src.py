"""
一般方法
"""
import ctypes
import inspect
import os
import pickle
import random
import socket
import string
import subprocess
import time
from typing import Union

import unicodedata
from opencc import OpenCC


def print_function_info(mode: str = 'current'):
    """
    打印当前/上一个函数的信息
    :param mode: str，'current' 或 'last'
    """

    def _print_function_info(_stack_trace: inspect.FrameInfo):
        """打印函数信息"""
        # 打印当前时间
        print('当前时间:', get_current_time('%H:%M:%S'))

        # 获取函数名
        caller_function_name = _stack_trace.function
        print("调用函数名:", caller_function_name)

        # 获取文件路径
        caller_file_path = _stack_trace.filename
        print("调用文件路径:", caller_file_path)

    # return  # 不需要print信息时取消该备注

    # 获取当前帧对象
    # frame = inspect.currentframe()
    # 获取调用栈
    stack_trace = inspect.stack()  # stack_trace[0]为本函数，stack_trace[1]为调用本函数的函数
    if mode == 'current':  # 打印当前函数信息
        _print_function_info(stack_trace[1])
    elif mode == 'last':  # 打印上一个函数信息
        if len(stack_trace) >= 3:
            _print_function_info(stack_trace[2])


def get_current_time(_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取当前时间的标准化格式str
    :param _format: str，自定义时间格式
    :return: str，时间格式表示的字符串"
    """
    return time.strftime(_format, time.localtime())


def convert_time(runtime: float):
    """将一个时间差转换为时分秒的字符串"""
    hours = int(runtime // 3600)
    minutes = int((runtime % 3600) // 60)
    seconds = int(runtime % 60)
    time_str = f'{hours}:{minutes:02d}:{seconds:02d}'

    return time_str


def create_random_string(length: int = 16, lowercase: bool = True, uppercase: bool = True, digits: bool = True) -> str:
    """生成一个指定长度的随机字符串
    :param length: int，字符串长度
    :param lowercase: bool，小写英文字母
    :param uppercase: bool，大写英文字母
    :param digits: bool，数字
    :return: str，随机字符串"""
    characters = ''
    if lowercase:
        characters += string.ascii_lowercase
    if uppercase:
        characters += string.ascii_uppercase
    if digits:
        characters += string.digits
    if not characters:
        raise Exception('没有选择字符')

    random_string = ''.join(random.choices(characters, k=length))

    return random_string


def merge_intersection_item(items: Union[list, tuple, set]) -> list:
    """合并有交集的集合/列表/元组 [(1,2),{2,3},(5,6)]->[(1,2,3),(5,6)]
    :return: 示例 [(1,2),{2,3},(5,6)]->[(1,2,3),(5,6)]"""
    merged_list = []

    for i in range(len(items)):
        set_merged = False

        for j in range(len(merged_list)):
            if set(items[i]) & set(merged_list[j]):
                merged_list[j] = set(set(items[i]) | set(merged_list[j]))
                set_merged = True
                break

        if not set_merged:
            merged_list.append(items[i])

    return merged_list


def filter_child_folder(folder_list: list) -> list:
    """过滤文件夹列表中的所有子文件夹，返回剔除子文件夹后的list"""
    child_folder = set()
    for folder in folder_list:
        # 相互比对，检查是否为当前文件夹的下级
        for other_folder in folder_list:
            # 统一路径分隔符（os.path.normpath无法实现）
            other_folder_replace = os.path.normpath(other_folder).replace('/', '\\')
            folder_replace = os.path.normpath(folder).replace('/', '\\')
            compare_path = os.path.normpath(folder + os.sep).replace('/', '\\')
            if other_folder_replace.startswith(str(compare_path)) and other_folder_replace != folder_replace:
                child_folder.add(other_folder)

    for i in child_folder:
        if i in folder_list:
            folder_list.remove(i)

    return folder_list


def get_subclasses(cls):
    """获取所有子类对象"""
    subclasses = []
    for subclass in cls.__subclasses__():
        subclasses.append(subclass)
        subclasses.extend(get_subclasses(subclass))
    return subclasses


def to_half_width_character(text: str):
    """将传入字符串转换为半角字符"""
    # 先将字符串进行Unicode规范化为NFKC格式（兼容性组合用序列）
    normalized_string = unicodedata.normalize('NFKC', text)

    # 对于ASCII范围内的全角字符，将其替换为对应的半角字符
    half_width_string = []
    for char in normalized_string:
        code_point = ord(char)
        if 0xFF01 <= code_point <= 0xFF5E:
            half_width_string.append(chr(code_point - 0xFEE0))
        else:
            half_width_string.append(char)

    return ''.join(half_width_string)


def to_full_width_character(text: str):
    """将传入字符串转换为全角字符"""
    # 将字符串进行Unicode规范化为NFKC格式（兼容性组合用序列）
    normalized_string = unicodedata.normalize('NFKC', text)

    # 对于ASCII范围内的字符，将其替换为对应的全角字符
    full_width_string = []
    for char in normalized_string:
        code_point = ord(char)
        if 0x0020 <= code_point <= 0x007E:
            full_width_string.append(chr(code_point + 0xFF00 - 0x0020))
        else:
            full_width_string.append(char)

    return ''.join(full_width_string)


def to_chs_character(text: str):
    """将字符串中的中文转换为简体中文"""
    cc = OpenCC('t2s')
    text_converted = cc.convert(text)
    return text_converted


def to_cht_character(text: str):
    """将字符串中的中文转换为繁体中文"""
    cc = OpenCC('s2t')
    text_converted = cc.convert(text)
    return text_converted


def flush_dns():
    """刷新DNS缓存"""
    subprocess.run(['ipconfig', '/flushdns'], shell=True)


def send_data_to_socket(data, host: str, port: str):
    """向本地端口传递数据（使用socket）
    :param data: 任意类型的数据
    :param host: str，主机地址
    :param port: str，端口"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)

    try:
        # 发送数据
        serialized_data = pickle.dumps(data)  # 用pickle序列化，传递更多类型的数据
        sock.sendall(serialized_data)
    finally:
        # 关闭连接
        sock.close()


def check_mutex(mutex_name: str):
    """使用互斥体检查是否已经打开了一个程序实例
    :param mutex_name: str，互斥体名称，建议使用程序名称"""
    # 创建互斥体
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    # 如果创建时报错，则说明已经创建过该互斥体，即已经有一个程序在运行了
    if ctypes.windll.kernel32.GetLastError() == 183:
        ctypes.windll.kernel32.CloseHandle(mutex)
        return True
    return False
