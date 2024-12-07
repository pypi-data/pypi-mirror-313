import numpy

from pptools.image import _src


def bytes_to_numpy(bytes_image: bytes) -> numpy.ndarray:
    """将bytes图片对象转换为numpy图片对象
    :param bytes_image: bytes图片对象
    :return: numpy图片对象"""
    if isinstance(bytes_to_numpy, bytes):
        raise Exception('传入图片数据类型错误')

    return _src.bytes_to_numpy(bytes_image)


def numpy_to_bytes(numpy_image: numpy.ndarray) -> bytes:
    """将numpy图片对象转换为bytes图片对象
    :param numpy_image: numpy图片对象
    :return: bytes图片对象"""
    if isinstance(numpy_image, numpy.ndarray):
        raise Exception('传入图片数据类型错误')

    return _src.numpy_to_bytes(numpy_image)

def resize_image_numpy(image: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    """缩放numpy图片对象至指定宽高
    :param image: numpy图片对象
    :param width: int，新的宽度
    :param height: int，新的高度"""
    return _src.resize_image_numpy(image,width, height )

def resize_image_numpy_ratio(image: numpy.ndarray, ratio: float) -> numpy.ndarray:
    """按比例缩放numpy图片对象
    :param image: numpy图片对象
    :param ratio: float，缩放比例（>0）"""
    return _src.resize_image_numpy_ratio(image,ratio )

def rgb_to_gray_numpy(image: numpy.ndarray) -> numpy.ndarray:
    """将numpy图片对象转为灰度图"""
    return _src.rgb_to_gray_numpy(image)