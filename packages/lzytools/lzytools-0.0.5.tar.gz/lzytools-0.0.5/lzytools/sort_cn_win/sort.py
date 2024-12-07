"""
以Windows本地环境的排序规则对传入列表/传入路径的内部文件列表进行排序（主要用于排序中文）

列表排序实现方法：
1. 初始化本地环境
2. 使用冒泡排序，对比两个键的顺序，将其每个字符拆分，逐级对比
3. 返回排序后的列表

路径排序实现方法：
1. 遍历传入路径，按需提取文件或文件夹
2. 对路径中的每一个文件夹及其自身进行列表排序
3. 返回排序后的列表
"""
from typing import Union

from lzytools.sort_cn_win import _src


def sort_list(_list: list, order_type: str = 'ASC') -> Union[list, SystemExit]:
    """排序列表
    :param _list: 需要排序的list
    :param order_type: 排序类型，'ASC' 升序或 'DESC' 降序，默认为升序
    :return: 排序后的list
    """
    return _src.sort_list(_list, order_type)


def sort_path(_dirpath: str, order_type: str = 'ASC', filetype: str = 'both', walk_depth: int = 0) -> list:
    """排序指定文件夹中的下级文件/文件夹
    :param _dirpath: 需要排序的文件夹路径
    :param order_type: 排序类型，'ASC' 升序或 'DESC' 降序，默认为升序
    :param filetype: 需要排序的文件类型，'file' 文件或 'folder' 文件夹或 'both' 两者皆有，默认为两者皆有
    :param walk_depth: 遍历的层级深度，默认为0（排序所有下级层数的文件/文件夹）
    :return: 排序后的内部文件完整路径list
    """
    return _src.sort_path(_dirpath, order_type, filetype, walk_depth)
