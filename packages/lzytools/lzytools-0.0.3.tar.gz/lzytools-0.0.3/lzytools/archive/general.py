import zipfile
from typing import Union

import rarfile

from pptools.archive import _src


def read_archive(archive_path: str) -> Union[zipfile.ZipFile, rarfile.RarFile, bool]:
    """读取压缩文件，并返回压缩文件对象（仅支持zip和rar）
    :param archive_path: str，压缩文件路径
    :return: 返回zip/rar对象，或正确读取文件时返回False"""
    return _src.read_archive(archive_path)


def get_infolist(archive_path: str) -> list:
    """获取压缩文件的内部信息list（仅支持zip和rar）
    :param archive_path: str，压缩文件路径
    :return: list，zipfile/rarfile库读取的压缩文件的infolist"""
    return _src.get_infolist(archive_path)


def get_structure(archive_path: str) -> list:
    """获取压缩文件的内部文件结构（仅支持zip和rar）
    :param archive_path: str，压缩文件路径
    :return: list，内部文件和文件夹，按层级排序"""
    return _src.get_structure(archive_path)


def get_real_size(archive_path: str) -> int:
    """获取一个压缩文件的内部文件大小（解压后的原始文件大小）
    :param archive_path: str，压缩文件路径
    :return: int，压缩包内部文件的实际大小（字节）"""
    return _src.get_real_size(archive_path)


def read_image(archive_path: str, image_path: str) -> bytes:
    """读取压缩文件中的指定图片，返回一个bytes图片对象
    :param archive_path: str，压缩文件路径
    :param image_path: str，压缩包内部图片路径"""
    return _src.read_image(archive_path, image_path)


def is_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为压缩文件
    :param filename: str，文件名（包含文件扩展名）
    :return: bool，是否为压缩包
    """
    return _src.is_archive_by_filename(filename)


def is_archive(filepath: str) -> bool:
    """通过文件头判断是否为压缩文件
    :param filepath: str，文件路径
    :return: bool，是否为压缩包
    """
    return _src.is_archive(filepath)


def is_volume_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为分卷压缩文件
    :param filename: str，文件名（包含文件扩展名）"""
    return _src.is_volume_archive_by_filename(filename)


def guess_first_volume_archive_filename(filename: str) -> Union[str, bool]:
    """根据传入的文件名，生成分卷压缩文件的首个分卷包文件名
    :param filename: str，文件名（包含文件扩展名）
    :return: 生成的首个分卷包文件名，或未生成时False"""
    return _src.guess_first_volume_archive_filename(filename)
