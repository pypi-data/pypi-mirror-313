import os
import re
import zipfile
from typing import Union

import rarfile

from lzytools.file._src import guess_filetype

# 分卷压缩包正则
_PATTERN_7Z = r'^(.+)\.7z\.\d+$'  # test.7z.001/test.7z.002/test.7z.003
_PATTERN_RAR = r'^(.+)\.part(\d+)\.rar$'  # test.part1.rar/test.part2.rar/test.part3.rar
_PATTERN_RAR_WITHOUT_SUFFIX = r'^(.+)\.part(\d+)$'  # rar分卷文件无后缀时也能正常解压，test.part1/test.part2/test.part3
_PATTERN_ZIP = r'^(.+)\.zip$'  # zip分卷文件的第一个分卷包一般都是.zip后缀，所以.zip后缀直接视为分卷压缩文件 test.zip
_PATTERN_ZIP_VOLUME = r'^(.+)\.z\d+$'  # test.zip/test.z01/test.z02
_PATTERN_ZIP_TYPE2 = r'^(.+)\.zip\.\d+$'  # test.zip.001/test.zip.002/test.zip.003


def read_archive(archive_path: str) -> Union[zipfile.ZipFile, rarfile.RarFile, bool]:
    """读取压缩文件，并返回压缩文件对象（仅支持zip和rar）
    :param archive_path: str，压缩文件路径
    :return: 返回zip/rar对象，或正确读取文件时返回False"""
    try:
        archive = zipfile.ZipFile(archive_path)
    except zipfile.BadZipFile:
        try:
            archive = rarfile.RarFile(archive_path)
        except rarfile.NotRarFile:
            return False
    except FileNotFoundError:
        return False

    return archive


def get_infolist(archive_path: str) -> list:
    """获取压缩文件的内部信息list（仅支持zip和rar）
    :param archive_path: str，压缩文件路径
    :return: list，zipfile/rarfile库读取的压缩文件的infolist"""
    archive = read_archive(archive_path)
    if not archive:
        raise Exception('未正确读取文件，该文件不是压缩文件或文件不存在')

    infolist = archive.infolist()  # 中文等字符会变为乱码

    archive.close()

    return infolist


def get_structure(archive_path: str) -> list:
    """获取压缩文件的内部文件结构（仅支持zip和rar）
    :param archive_path: str，压缩文件路径
    :return: list，内部文件和文件夹，按层级排序"""
    infolist = get_infolist(archive_path)
    filenames = [i.filename for i in infolist]

    return filenames


def get_real_size(archive_path: str) -> int:
    """获取一个压缩文件的内部文件大小（解压后的原始文件大小）
    :param archive_path: str，压缩文件路径
    :return: int，压缩包内部文件的实际大小（字节）"""
    total_size = 0
    infolist = get_infolist(archive_path)
    for info in infolist:
        info: Union[zipfile.ZipInfo, rarfile.RarInfo]
        total_size += info.file_size

    return total_size


def read_image(archive_path: str, image_path: str) -> bytes:
    """读取压缩文件中的指定图片，返回一个bytes图片对象
    :param archive_path: str，压缩文件路径
    :param image_path: str，压缩包内部图片路径"""
    archive = read_archive(archive_path)
    if not archive:
        raise Exception('未正确读取文件，该文件不是压缩文件或文件不存在')

    try:
        img_data = archive.read(image_path)
    except KeyError:
        raise Exception('压缩文件中不存在该文件')

    archive.close()

    return img_data


def is_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为压缩文件
    :param filename: str，文件名（包含文件扩展名）
    :return: bool，是否为压缩包
    """
    _archive_file_extension = ['zip', 'rar', '7z', 'tar', 'gz', 'xz', 'iso']

    #  提取文件后缀名（不带.），判断一般的压缩文件
    file_extension = os.path.splitext(filename)[1].strip()
    if file_extension.lower() in _archive_file_extension:
        return True

    # 检查是否为分卷压缩文件
    if is_volume_archive_by_filename(filename):
        return True

    return False


def is_archive(filepath: str) -> bool:
    """通过文件头判断是否为压缩文件
    :param filepath: str，文件路径
    :return: bool，是否为压缩包
    """
    _archive_file_extension = ['zip', 'tar', 'rar', 'gz', '7z', 'xz']  # filetype库支持的压缩文件后缀名
    guess_type = guess_filetype(filepath)
    if guess_type and guess_type in _archive_file_extension:
        return True

    return False


def is_volume_archive_by_filename(filename: str) -> bool:
    """通过文件名判断是否为分卷压缩文件
    :param filename: str，文件名（包含文件扩展名）"""
    pattern_joined = [_PATTERN_7Z, _PATTERN_RAR, _PATTERN_RAR_WITHOUT_SUFFIX,
                      _PATTERN_ZIP, _PATTERN_ZIP_VOLUME, _PATTERN_ZIP_TYPE2]

    for pattern in pattern_joined:
        if re.match(pattern, filename, flags=re.I):
            return True

    return False


def guess_first_volume_archive_filename(filename: str) -> Union[str, bool]:
    """根据传入的文件名，生成分卷压缩文件的首个分卷包文件名
    :param filename: str，文件名（包含文件扩展名）
    :return: 生成的首个分卷包文件名，或未生成时False"""
    if not is_volume_archive_by_filename(filename):
        return False

    guess_filename = False

    # test.7z.001/test.7z.002/test.7z.003
    if re.match(_PATTERN_7Z, filename, flags=re.I):
        filetitle = re.match(_PATTERN_7Z, filename, flags=re.I).group(1)
        guess_filename = f'{filetitle}.7z.001'
    # test.part1.rar/test.part2.rar/test.part3.rar
    elif re.match(_PATTERN_RAR, filename, flags=re.I):
        filetitle = re.match(_PATTERN_RAR, filename, flags=re.I).group(1)
        number_length = len(re.match(_PATTERN_RAR, filename, flags=re.I).group(2))  # 处理part1.rar和part01.rar的情况
        guess_filename = f'{filetitle}.part{"1".zfill(number_length)}.rar'
    # test.part1/test.part2/test.part3
    elif re.match(_PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I):
        filetitle = re.match(_PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I).group(1)
        number_length = len(re.match(_PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I).group(2))
        guess_filename = f'{filetitle}.part{"1".zfill(number_length)}'
    # test.zip
    elif re.match(_PATTERN_ZIP, filename, flags=re.I):
        guess_filename = filename
    # test.zip/test.z01/test.z02
    elif re.match(_PATTERN_ZIP_VOLUME, filename, flags=re.I):
        filetitle = re.match(_PATTERN_ZIP_VOLUME, filename, flags=re.I).group(1)
        guess_filename = f'{filetitle}.zip'
    # test.zip.001/test.zip.002/test.zip.003
    elif re.match(_PATTERN_ZIP_TYPE2, filename, flags=re.I):
        filetitle = re.match(_PATTERN_ZIP_TYPE2, filename, flags=re.I).group(1)
        guess_filename = f'{filetitle}.zip.001'

    return guess_filename
