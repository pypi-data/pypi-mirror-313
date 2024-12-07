import io
import os
import zipfile
from typing import Union

import cv2
import imagehash
import numpy
import rarfile
from PIL import Image, ImageFile

from lzytools.archive._src import read_image, get_infolist

ImageFile.LOAD_TRUNCATED_IMAGES = True  # 允许加载截断的图像 防止报错OSError: image file is truncated


def read_image_to_numpy(image_path: str) -> numpy.ndarray:
    """读取本地图片，返回numpy图片对象
    :param image_path: 图片路径
    :return: numpy图片对象"""
    image_numpy = cv2.imdecode(numpy.fromfile(image_path, dtype=numpy.uint8), -1)

    return image_numpy


def read_image_to_bytes(image_path: str) -> bytes:
    """读取本地图片，返回bytes图片对象
    :param image_path: 图片路径
    :return: bytes图片对象"""
    if os.path.exists(image_path):
        with open(image_path, 'rb') as file:
            image_bytes = file.read()
    else:
        image_bytes = rb''

    return image_bytes


def bytes_to_numpy(bytes_image: bytes) -> numpy.ndarray:
    """将bytes图片对象转换为numpy图片对象
    :param bytes_image: bytes图片对象
    :return: numpy图片对象"""
    bytesio_image = io.BytesIO(bytes_image)  # 转为BytesIO对象
    pil_image = Image.open(bytesio_image)  # 转PIL.Image
    numpy_image = numpy.array(pil_image)  # 转NumPy数组

    return numpy_image


def numpy_to_bytes(numpy_image: numpy.ndarray) -> bytes:
    """将numpy图片对象转换为bytes图片对象
    :param numpy_image: numpy图片对象
    :return: bytes图片对象"""
    image = Image.fromarray(numpy_image)  # 换为PIL Image对象
    bytes_image = io.BytesIO()  # 转为BytesIO对象
    image.save(bytes_image, format=image.format)
    bytes_image = bytes_image.getvalue()

    return bytes_image


def save_bytes_image(bytes_image: bytes, dirpath: str, filename: str) -> str:
    """将一个bytes图片对象保存至本地
    :param bytes_image: bytes，bytes图片对象
    :param dirpath: str，保存至该目录下
    :param filename: str，保存的文件名（不含文件扩展名）
    :return: str，保存的本地图片路径"""
    image = Image.open(io.BytesIO(bytes_image))

    # 转换图像模式，防止报错OSError: cannot write mode P as JPEG
    image = image.convert('RGB')

    # 提取文件后缀
    file_extension = image.format  # 备忘录 找一个读取bytes图片后缀的方法

    # 组合保存路径
    save_path = os.path.normpath(os.path.join(dirpath, filename + file_extension))

    # 保存到本地
    if not os.path.exists(dirpath):
        os.mkdir(save_path)
    image.save(save_path)

    return save_path


def save_numpy_image(numpy_image: numpy.ndarray, dirpath: str, filename: str) -> str:
    """将一个numpy图片对象保存至本地
    :param numpy_image: numpy.ndarray，numpy图片对象
    :param dirpath: str，保存至该目录下
    :param filename: str，保存的文件名（不含文件扩展名）
    :return: str，保存的本地图片路径"""
    # 转换为uint8类型
    numpy_image = numpy_image.astype(numpy.uint8)

    # 转换为Pillow图像对象
    image = Image.fromarray(numpy_image)

    # 提取文件后缀
    file_extension = image.format

    # 组合保存路径
    save_path = os.path.normpath(os.path.join(dirpath, filename + file_extension))

    # 保存到本地
    if not os.path.exists(dirpath):
        os.mkdir(save_path)
    image.save(save_path)

    return save_path


def resize_image_numpy(image: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    """缩放numpy图片对象至指定宽高
    :param image: numpy图片对象
    :param width: int，新的宽度
    :param height: int，新的高度"""
    image_ = cv2.resize(image, dsize=(width, height))
    return image_


def resize_image_numpy_ratio(image: numpy.ndarray, ratio: float) -> numpy.ndarray:
    """按比例缩放numpy图片对象
    :param image: numpy图片对象
    :param ratio: float，缩放比例（>0）"""
    width, height = image.size
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    image_ = cv2.resize(image, dsize=(new_width, new_height))
    return image_


def rgb_to_gray_numpy(image: numpy.ndarray) -> numpy.ndarray:
    """将numpy图片对象转为灰度图"""
    image_ = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image_


def get_image_filesize_from_archive(archive_path: str, image_path: str) -> int:
    """获取压缩文件中指定图片的文件大小（字节）
    :param archive_path: str，压缩文件路径
    :param image_path: str，压缩包内部图片路径
     :return: int，压缩文件中指定图片的文件大小（字节）"""
    infolist = get_infolist(archive_path)
    for info in infolist:
        info: Union[zipfile.ZipInfo, rarfile.RarInfo]
        path = info.filename
        if image_path.lower() == path.lower():
            size = info.file_size
            return size

    return 0  # 兜底


def get_image_size_from_archive(archive_path: str, image_path: str) -> tuple[int, int]:
    """获取压缩文件中指定图片的尺寸
    :param archive_path: str，压缩文件路径
    :param image_path: str，压缩包内部图片路径
     :return: tuple，(宽, 高）"""
    image_bytes = read_image(archive_path, image_path)
    image_stream = io.BytesIO(image_bytes)
    image_pil = Image.open(image_stream)
    size = image_pil.size
    return size


def get_image_size(image_path: str):
    """获取图片的宽高
    :param image_path: str，本地图片路径"""
    image = Image.open(image_path)
    size = image.size
    return size


def calc_hash(image: ImageFile, hash_size: int = 8) -> dict:
    """计算图片的3种图片Hash值
    :param image: PIL.ImageFile图片对象
    :param hash_size: 计算的图片Hash值的边长
    :return: dict，{'ahash':None,'phash':None,'dhash':None}
    """
    hash_dict = {'ahash': None, 'phash': None, 'dhash': None}
    # 计算均值哈希
    ahash = imagehash.average_hash(image, hash_size=hash_size)
    ahash_str = numpy_hash_to_str(ahash)
    hash_dict['ahash'] = ahash_str
    # 感知哈希
    phash = imagehash.phash(image, hash_size=hash_size)
    phash_str = numpy_hash_to_str(phash)
    hash_dict['phash'] = phash_str
    # 差异哈希
    dhash = imagehash.dhash(image, hash_size=hash_size)
    dhash_str = numpy_hash_to_str(dhash)
    hash_dict['dhash'] = dhash_str

    return hash_dict


def numpy_hash_to_str(numpy_hash: Union[imagehash.NDArray, imagehash.ImageHash]):
    """将numpy数组形式的图片Hash值(imagehash.hash)转换为01组成的字符串
    :param numpy_hash: numpy数组形式的图片Hash值
    :return: str，01组成的字符串"""
    if not numpy_hash:
        return None
    if isinstance(numpy_hash, imagehash.ImageHash):
        numpy_hash = numpy_hash.hash

    hash_str = ''
    for row in numpy_hash:
        for col in row:
            if col:
                hash_str += '1'
            else:
                hash_str += '0'

    return hash_str


def calc_hash_hamming_distance(hash_1: str, hash_2: str):
    """计算两个01字符串形式的图片Hash值的汉明距离"""
    hamming_distance = sum(ch1 != ch2 for ch1, ch2 in zip(hash_1, hash_2))
    return hamming_distance


def calc_hash_similar(hash_1: str, hash_2: str):
    """计算两个01字符串形式的图片Hash值的相似度（0~1)"""
    hash_int1 = int(hash_1, 2)
    hash_int2 = int(hash_2, 2)
    # 使用异或操作计算差异位数
    diff_bits = bin(hash_int1 ^ hash_int2).count('1')
    # 计算相似性
    similarity = 1 - diff_bits / len(hash_1)

    return similarity


def is_pure_color_image(image_path: str) -> bool:
    """是否为纯色图片
    :param image_path: str，图片路径"""
    # 考虑到库的大小，通过计算图片Hash值的方法来判断是否为纯色图片（不使用opencv库，该库太大）
    try:
        image_pil = Image.open(image_path)
        image_pil = image_pil.convert('L')  # 转灰度图
    except OSError:  # 如果图片损坏，会抛出异常OSError: image file is truncated (4 bytes not processed)
        return False

    dhash = imagehash.average_hash(image_pil, hash_size=16)
    hash_str = numpy_hash_to_str(dhash)

    if hash_str.count('0') == len(hash_str):
        return True
    else:
        return False


def calc_ssim(image_numpy_1: numpy.ndarray, image_numpy_2: numpy.ndarray) -> float:
    """计算两张图片的SSIM相似值（0~1，越大越相似）
    :param image_numpy_1: numpy图片对象
    :param image_numpy_2: numpy图片对象
    :return: float，SSIM相似值（0~1，越大越相似）"""
    # 计算均值、方差和协方差
    mean1, mean2 = numpy.mean(image_numpy_1), numpy.mean(image_numpy_2)
    var1, var2 = numpy.var(image_numpy_1), numpy.var(image_numpy_2)
    covar = numpy.cov(image_numpy_1.flatten(), image_numpy_2.flatten())[0][1]

    # 设置常数
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2

    # 计算SSIM
    numerator = (2 * mean1 * mean2 + c1) * (2 * covar + c2)
    denominator = (mean1 ** 2 + mean2 ** 2 + c1) * (var1 + var2 + c2)
    ssim = numerator / denominator

    return ssim
