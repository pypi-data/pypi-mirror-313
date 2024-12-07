from typing import Union

import numpy

from lzytools.image import _src


def save_local(image: Union[bytes, numpy.ndarray], dirpath: str, filename: str) -> str:
    """将一个bytes/numpy图片对象保存至本地
    :param image: bytes/numpy图片对象
    :param dirpath: str，保存至该目录下
    :param filename: str，保存的文件名（不含文件扩展名）
    :return: str，保存的本地图片路径"""
    if isinstance(image, bytes):
        return _src.save_bytes_image(image, dirpath, filename)
    elif isinstance(image, numpy.ndarray):
        return _src.save_numpy_image(image, dirpath, filename)
    else:
        raise Exception(f'不支持的图片类型：{type(image)}')
