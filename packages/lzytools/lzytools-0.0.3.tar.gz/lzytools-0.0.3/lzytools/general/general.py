from typing import Union

from pptools.general import _src


def print_function_info(mode: str = 'current'):
    """
    打印当前/上一个函数的信息
    :param mode: str，'current' 或 'last'
    """
    return _src.print_function_info(mode)


def get_current_time(_format: str = '%Y-%m-%d %H:%M:%S') -> str:
    """获取当前时间的标准化格式str
    :param _format: str，自定义时间格式
    :return: str，时间格式表示的字符串"
    """
    return _src.get_current_time(_format)


def convert_time(runtime: float):
    """将一个时间差转换为时分秒的字符串"""
    return _src.convert_time(runtime)


def create_random_string(length: int = 16, lowercase: bool = True, uppercase: bool = True, digits: bool = True) -> str:
    """生成一个指定长度的随机字符串
    :param length: int，字符串长度
    :param lowercase: bool，小写英文字母
    :param uppercase: bool，大写英文字母
    :param digits: bool，数字
    :return: str，随机字符串"""
    return _src.create_random_string(length, lowercase, uppercase, digits)


def merge_intersection_item(items: Union[list, tuple, set]):
    """合并有交集的集合/列表/元组 [(1,2),{2,3},(5,6)]->[(1,2,3),(5,6)]
    :return: 示例 [(1,2),{2,3},(5,6)]->[(1,2,3),(5,6)]"""
    return _src.merge_intersection_item(items)


def filter_child_folder(folder_list: list) -> list:
    """过滤文件夹列表中的所有子文件夹，返回剔除子文件夹后的list"""
    return _src.filter_child_folder(folder_list)


def get_subclasses(cls):
    """获取所有子类对象"""
    return _src.get_subclasses(cls)


def to_half_width_character(text: str):
    """将传入字符串转换为半角字符"""
    return _src.to_half_width_character(text)


def to_full_width_character(text: str):
    """将传入字符串转换为全角字符"""
    return _src.to_full_width_character(text)


def to_chs_character(text: str):
    """将字符串中的中文转换为简体中文"""
    return _src.to_chs_character(text)


def to_cht_character(text: str):
    """将字符串中的中文转换为繁体中文"""
    return _src.to_cht_character(text)


def flush_dns():
    """刷新DNS缓存"""
    return _src.flush_dns()


def send_data_to_socket(data, host: str, port: str):
    """向本地端口传递数据（使用socket）
    :param data: 任意类型的数据
    :param host: str，主机地址
    :param port: str，端口"""
    return _src.send_data_to_socket(data, host, port)


def check_mutex(mutex_name: str):
    """使用互斥体检查是否已经打开了一个程序实例
    :param mutex_name: str，互斥体名称，建议使用程序名称"""
    return _src.check_mutex(mutex_name)
