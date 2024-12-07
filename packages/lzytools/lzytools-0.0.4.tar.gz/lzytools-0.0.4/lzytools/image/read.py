from typing import Union

import numpy

from lzytools.image import _src


def read_image(image_path: str, type_: str = 'bytes') -> Union[bytes, numpy.ndarray]:
    """读取本地图片，返回bytes图片对象
    :param image_path: 图片路径
    :param type_: 返回的数据类型，'bytes'/'numpy'
    :return: bytes/numpy图片对象"""
    _TYPE = ['bytes', 'numpy']
    if type_.lower() not in _TYPE:
        raise Exception('读取类型输入错误')

    if type_.lower() == 'bytes':
        img = _src.read_image_to_bytes(image_path)
    else:
        img = _src.read_image_to_numpy(image_path)

    return img


