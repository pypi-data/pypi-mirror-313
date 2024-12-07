from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget

from pptools.qt_pyside6 import _src


def set_transparent_background(widget: QWidget):
    """设置Widget的背景为透明"""
    return _src.set_transparent_background(widget)


def calculate_keep_aspect_ratio_resize(qsize_widget: QSize, qsize_pic: QSize) -> QSize:
    """计算图片显示控件上时，为了保持图片纵横比而计算的控件的新尺寸"""
    return _src.calculate_keep_aspect_ratio_resize(qsize_widget, qsize_pic)


class TabelWidgetHiddenOverLengthText(_src.TabelWidgetHiddenOverLengthText):
    """文本框控件，自动隐藏长文本（abcd->a...）
    备注：利用tableWidget的文本单元格自动隐藏长文本的特性"""


class LabelHiddenOverLengthText(_src.LabelHiddenOverLengthText):
    """文本框控件，自动隐藏长文本（abcd->a...）"""


class LineEditDropFiles(_src.QLineEdit):
    """支持拖入多个文件/文件夹的文本框，设置文本为拖入的路径，并发送信号传递拖入路径的list"""


class LineEditDropFile(_src.LineEditDropFile):
    """支持拖入单个文件/文件夹的文本框，设置文本为拖入的路径，并发送信号传递拖入路径的list
    新增功能：定时检查路径有效性"""


class LabelDropFiles(_src.LabelDropFiles):
    """支持拖入多个文件/文件夹的标签控件，并发送信号传递拖入路径的list"""


class LabelDropFilesTip(_src.LabelDropFilesTip):
    """支持拖入多个文件/文件夹的标签控件，并发送信号传递拖入路径的list
    新增功能：拖入时会提示"""


class LabelDropImageShow(_src.LabelDropImageShow):
    """拖入单个图片文件并显示"""


class SliderMoved(_src.SliderMoved):
    """移动后发送新值信号"""


class WidgetLineOpenDeleteText(_src.WidgetLineOpenDeleteText):
    """控件组合，打开按钮-删除按钮-文本框"""


class ListWidgetFileList(_src.ListWidgetFileList):
    """拖入文件/文件夹并显示在列表控件中，附带基础功能"""


class TopTip(_src.TopTip):
    """显示一个置顶的提示文本
    新增功能：淡入淡出动画"""


class QtimerSingleShot(_src.QtimerSingleShot):
    """单例单次触发的计时器"""


class ThreadListenSocket(_src.ThreadListenSocket):
    """监听本地端口的子线程"""


class ToolButtonRightClick(_src.ToolButtonRightClick):
    """支持右键点击信号的QToolButton"""


class DialogGifPlayer(_src.DialogGifPlayer):
    """播放GIF动画的QDialog"""


class LabelHoverInfo(_src.LabelHoverInfo):
    """自动隐藏的悬浮在控件左下角的label（用于显示提示信息）"""


class WidgetAutoHidden(_src.WidgetAutoHidden):
    """悬停时显示，离开时隐藏的Widget"""


class StyledItemDelegateImage(_src.StyledItemDelegateImage):
    """项目视图委托QStyledItemDelegate，在QStandardItem中显示自适应大小的图像
    注意：图像路径需在保存在QStandardItem的UserRole属性中"""
