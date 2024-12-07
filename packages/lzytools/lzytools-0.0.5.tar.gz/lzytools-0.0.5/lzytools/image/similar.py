from typing import Union

import imagehash
import numpy
from PIL import ImageFile

from lzytools.image import _src


def calc_hash(image: ImageFile, hash_size: int = 8) -> dict:
    """计算图片的3种图片Hash值
    :param image: PIL.ImageFile图片对象
    :param hash_size: 计算的图片Hash值的边长
    :return: dict，{'ahash':None,'phash':None,'dhash':None}
    """
    return _src.calc_hash(image, hash_size)


def numpy_hash_to_str(numpy_hash: Union[imagehash.NDArray, imagehash.ImageHash]):
    """将numpy数组形式的图片Hash值(imagehash.hash)转换为01组成的字符串
    :param numpy_hash: numpy数组形式的图片Hash值
    :return: str，01组成的字符串"""
    return _src.numpy_hash_to_str(numpy_hash)


def calc_hash_hamming_distance(hash_1: str, hash_2: str):
    """计算两个01字符串形式的图片Hash值的汉明距离"""
    return _src.calc_hash_hamming_distance(hash_1, hash_2)


def calc_hash_similar(hash_1: str, hash_2: str):
    """计算两个01字符串形式的图片Hash值的相似度（0~1)"""
    return _src.calc_hash_similar(hash_1, hash_2)


def calc_ssim(image_numpy_1: numpy.ndarray, image_numpy_2: numpy.ndarray) -> float:
    """计算两张图片的SSIM相似值（0~1，越大越相似）
    :param image_numpy_1: numpy图片对象
    :param image_numpy_2: numpy图片对象
    :return: float，SSIM相似值（0~1，越大越相似）"""
    return _src.calc_ssim(image_numpy_1, image_numpy_2)
