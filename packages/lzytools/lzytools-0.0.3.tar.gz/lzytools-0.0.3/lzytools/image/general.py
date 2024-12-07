from pptools.image import _src


def get_image_filesize_from_archive(archive_path: str, image_path: str) -> int:
    """获取压缩文件中指定图片的文件大小（字节）
    :param archive_path: str，压缩文件路径
    :param image_path: str，压缩包内部图片路径
     :return: int，压缩文件中指定图片的文件大小（字节）"""
    return _src.get_image_filesize_from_archive(archive_path, image_path)


def get_image_size_from_archive(archive_path: str, image_path: str) -> tuple[int, int]:
    """获取压缩文件中指定图片的尺寸
    :param archive_path: str，压缩文件路径
    :param image_path: str，压缩包内部图片路径
     :return: tuple，(宽, 高）"""
    return _src.get_image_size_from_archive(archive_path, image_path)


def get_image_size(image_path: str):
    """获取图片的宽高
    :param image_path: str，本地图片路径"""
    return _src.get_image_size(image_path)


def is_pure_color_image(image_path: str) -> bool:
    """是否为纯色图片
    :param image_path: str，图片路径"""
    return _src.is_pure_color_image(image_path)
