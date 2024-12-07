import os
import pickle
import socket
from typing import Union

import filetype
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


def set_transparent_background(widget: QWidget):
    """设置Widget的背景为透明"""
    widget.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框
    widget.setAttribute(Qt.WA_TranslucentBackground)  # 设置透明背景
    widget.setStyleSheet("background-color: transparent; border: none;")


def calculate_keep_aspect_ratio_resize(qsize_widget: QSize, qsize_pic: QSize) -> QSize:
    """计算图片显示控件上时，为了保持图片纵横比而计算的控件的新尺寸"""
    label_width = qsize_widget.width()
    label_height = qsize_widget.height()
    pic_width = qsize_pic.width()
    pic_height = qsize_pic.height()

    label_rate = label_width / label_height
    pic_rate = pic_width / pic_height

    if label_rate >= pic_rate:  # 符合则按高缩放
        resize_height = label_height
        resize_width = int(pic_width / pic_height * resize_height)
        resize_qsize = QSize(resize_width, resize_height)
    else:  # 否则按宽缩放
        resize_width = label_width
        resize_height = int(pic_height / pic_width * resize_width)
        resize_qsize = QSize(resize_width, resize_height)

    """
    后续操作示例
    pixmap = pixmap.scaled(resize_qsize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
    label.setPixmap(pixmap)
    """

    return resize_qsize


class TabelWidgetHiddenOverLengthText(QTableWidget):
    """文本框控件，自动隐藏长文本（abcd->a...）
    备注：利用tableWidget的文本单元格自动隐藏长文本的特性"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        # 设置列宽度为自动适应控件大小
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # 隐藏行列
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        # 设置为单行单列
        self.setColumnCount(1)
        self.insertRow(0)
        # 固定控件高度、单元格行高
        self.setFixedHeight(18)
        self.setRowHeight(0, 16)
        # 设置文本单元格
        self.item_filename = QTableWidgetItem('')
        self.setItem(0, 0, self.item_filename)
        # 禁止编辑单元格
        self.item_filename.setFlags(self.item_filename.flags() & ~Qt.ItemIsEditable)

    def set_text(self, text: str):
        """设置文本"""
        self.item_filename.setText(text)

    def set_tooltip(self, tool_tip: str):
        """设置控件提示"""
        self.item_filename.setToolTip(tool_tip)

    def set_height(self, height: int):
        """设置控件高度
        :param height: int，高度"""
        self.setFixedHeight(height + 2)  # 控件高度
        self.setRowHeight(0, height)  # 单元格行高


class LabelHiddenOverLengthText(QLabel):
    """文本框控件，自动隐藏长文本（abcd->a...）"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_origin = ''

    def setText(self, text):
        super().setText(text)
        self.text_origin = text
        self.check_over_length_text()

    def check_over_length_text(self):
        """检查文本是否超限"""
        # 获取字体度量
        font_metrics = self.fontMetrics()
        label_width = self.width()

        # 检查文本是否超出label宽度
        if font_metrics.horizontalAdvance(self.text_origin) > label_width:
            elided_text = font_metrics.elidedText(self.text_origin, Qt.ElideRight, label_width)
            self.setText(elided_text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.check_over_length_text()


class LineEditDropFiles(QLineEdit):
    """支持拖入多个文件/文件夹的文本框，设置文本为拖入的路径，并发送信号传递拖入路径的list"""

    signal_path_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setReadOnly(True)
        self.setPlaceholderText('拖入文件到此处...')

        self.path_dropped = []

    def update_paths(self, paths: list):
        """更新路径
        :param paths: list，包含完整路径的列表"""
        # 列表去重
        paths = list(dict.fromkeys(paths))
        # 重置参数
        self.path_dropped = paths
        # 更新文本
        self._update_text(paths)
        # 发送信号
        self._emit_signal(paths)

    def _update_text(self, paths: Union[list, str]):
        """更新文本"""
        if isinstance(paths, str):
            paths = [paths]
        self.setText(';'.join(paths))
        self.setToolTip('/n'.join(paths))

    def _emit_signal(self, paths: Union[list, str]):
        """发送信号"""
        if isinstance(paths, str):
            paths = [paths]
        self.signal_path_dropped.emit(paths)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            paths = []
            for index in range(len(urls)):
                path = urls[index].toLocalFile()
                paths.append(path)
            self.update_paths(paths)


class LineEditDropFile(LineEditDropFiles):
    """支持拖入单个文件/文件夹的文本框，设置文本为拖入的路径，并发送信号传递拖入路径的list
    新增功能：定时检查路径有效性"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置一个QTime，定时检查路径有效性
        self.is_exists = True
        self.stylesheet_not_exists = 'border: 1px solid red;'
        self.qtimer_check_path_exists = QTimer()
        self.qtimer_check_path_exists.timeout.connect(self._check_path_exists)
        self.qtimer_check_path_exists.setInterval(5000)  # 默认定时5秒
        self.qtimer_check_path_exists.start()

    def update_paths(self, paths: list):
        """更新路径
        :param paths: list，包含完整路径的列表"""
        # 提取首个路径
        path = paths[0]
        # 重置参数
        self.path_dropped = path
        # 更新文本
        self._update_text(path)
        # 发送信号
        self._emit_signal(path)

    def set_check_interval(self, second: float):
        """设置定时检查路径有效性的时间间隔"""
        self.qtimer_check_path_exists.setInterval(int(second * 1000))

    def set_stylesheet_not_exists(self, stylesheet: str):
        """设置路径不存在时的文本框样式"""
        self.stylesheet_not_exists = stylesheet

    def _check_path_exists(self):
        """检查路径有效性"""
        if self.path_dropped:
            if os.path.exists(self.path_dropped):
                self.is_exists = True
                self.setStyleSheet('')
            else:
                self.is_exists = False
                self.setStyleSheet(self.stylesheet_not_exists)
        else:
            self.is_exists = False


class LabelDropFiles(QLabel):
    """支持拖入多个文件/文件夹的标签控件，并发送信号传递拖入路径的list"""

    signal_path_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setScaledContents(True)

        self.path_dropped = []

    def update_paths(self, paths: list):
        """更新路径
        :param paths: list，包含完整路径的列表"""
        # 列表去重
        paths = list(dict.fromkeys(paths))
        # 重置参数
        self.path_dropped = paths
        # 发送信号
        self._emit_signal(paths)

    def _emit_signal(self, paths: Union[list, str]):
        """发送信号"""
        if isinstance(paths, str):
            paths = [paths]
        self.signal_path_dropped.emit(paths)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            paths = [url.toLocalFile() for url in urls]
            self.update_paths(paths)


class LabelDropFilesTip(LabelDropFiles):
    """支持拖入多个文件/文件夹的标签控件，并发送信号传递拖入路径的list
    新增功能：拖入时会提示"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon_drop = ''  # 拖入时的图标
        self.icon_last = None  # 拖入前的图标

    def set_drop_icon(self, icon_path: str):
        """拖入图标路径"""
        self.icon_drop = ''
        if os.path.exists(icon_path):
            self.icon_drop = icon_path

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            if self.icon_drop:
                self.icon_last = self.pixmap()
                self.setPixmap(QPixmap(self.icon_drop))  # 拖入时修改图标
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        if self.icon_drop:
            self.setPixmap(QPixmap(self.icon_last))  # 完成拖入后变回原图标
            self.icon_last = None


class LabelDropImageShow(LabelDropFiles):
    """拖入单个图片文件并显示"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def update_paths(self, paths: list):
        """更新路径
        :param paths: list，包含完整路径的列表"""
        # 提取首个路径并进行检查
        path = paths[0]
        self.path_dropped = ''
        if os.path.isfile(path) and filetype.is_image(path):
            self.path_dropped = path

        # 显示图片
        if self.path_dropped:
            self._show_image(self.path_dropped)
        else:
            self._clear_image()

        # 发送信号
        self._emit_signal(paths)

    def _show_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        resize = calculate_keep_aspect_ratio_resize(self.size(), pixmap.size())
        pixmap = pixmap.scaled(resize, spectRatioMode=Qt.KeepAspectRatio)  # 保持纵横比
        self.setPixmap(pixmap)

    def _clear_image(self):
        self.setPixmap(QPixmap())


class SliderMoved(QSlider):
    """移动后发送新值信号"""
    signal_moved = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def moved(self, value: int):
        """发生移动事件"""
        # 固定滑动块为新值
        self.setValue(value)
        # 发送信号
        self._emit_signal(value)

    def _emit_signal(self, value: int):
        """发送信号"""
        self.signal_moved.emit(value)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        value = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        self.moved(value)


class WidgetLineOpenDeleteText(QWidget):
    """控件组合，打开按钮-删除按钮-文本框"""
    signal_delete = Signal(str)
    signal_open = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.set_layout()
        self.toolButton_open = QToolButton()
        self._add_open_button()
        self.toolButton_delete = QToolButton()
        self._add_delete_button()
        self.text_label = QLabel()
        self._add_text_label()

        self.text = ''

    def set_text(self, text: str):
        """设置文本"""
        self.text_label.setText(text)
        self.text = text

    def set_tooltip(self, text: str):
        """设置文本提示"""
        self.text_label.setToolTip(text)

    def set_layout(self):
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setStretch(1, 1)

    def _open(self):
        self.signal_open.emit(self.text)

    def _delete(self):
        self.deleteLater()
        self.signal_delete.emit(self.text)

    def _add_open_button(self):
        self.toolButton_open.setText('□')
        set_transparent_background(self.toolButton_open)
        self.layout.addWidget(self.toolButton_open)
        self.toolButton_open.clicked.connect(self._open)

    def _add_delete_button(self):
        self.toolButton_delete.setText('×')
        set_transparent_background(self.toolButton_delete)
        self.layout.addWidget(self.toolButton_delete)
        self.toolButton_delete.clicked.connect(self._delete)

    def _add_text_label(self):
        self.text_label.setText('')
        self.layout.addWidget(self.text_label)


class ListWidgetFileList(QListWidget):
    """拖入文件/文件夹并显示在列表控件中，附带基础功能"""
    signal_update_list = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.paths = []

    def _add_items(self, paths: list):
        """新增行项目"""
        for path in paths:
            if path not in self.paths:
                self.paths.append(path)

        self._refresh()

    def _refresh(self):
        """刷新项目"""
        self.clear()
        for path in self.paths:
            # 创建子控件
            item = QListWidgetItem()
            item_widget = WidgetLineOpenDeleteText()
            item_widget.set_text(path)
            item_widget.signal_delete.connect(self._delete_item)
            # 插入子控件
            end_index = self.count()
            self.insertItem(end_index + 1, item)
            self.setItemWidget(item, item_widget)

        # 发送更新后的list
        self.signal_update_list.emit(self.paths)

    def _delete_item(self, deleted_path):
        """删除行项目"""
        # 删除变量中的对应数据
        if deleted_path in self.paths:
            self.paths.remove(deleted_path)
        # 刷新
        self._refresh()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            paths = [url.toLocalFile() for url in urls]
            self._add_items(paths)


class TopTip(QMainWindow):
    """显示一个置顶的提示文本
    新增功能：淡入淡出动画"""

    def __init__(self, text: str):
        super().__init__()

        # 添加显示文字的子控件
        self.label_showed = None
        self._add_label(str(text))

        # 设置定时器
        self.timer_fade = QTimer(self)
        self.timer_fade.timeout.connect(self._fade_out)
        self.timer_fade.start(2000)  # 留存2秒

        # 设置淡入淡出动画
        self.animation = QPropertyAnimation()
        self._set_animation()

        # 设置透明属性
        set_transparent_background(self)
        # 设置置顶显示
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # 更新控件大小（需要在添加子控件后更新）
        self.setFixedSize(self.sizeHint())

        # 显示
        self._show_in_center()
        self.animation.start()

    def set_duration(self, duration: int):
        """设置提示文本留存时间"""
        self.timer_fade.start(duration)

    def _add_label(self, text: str):
        """添加子控件"""
        label = QLabel(str(text))
        label.setStyleSheet("font-size: 15pt; color: blue")
        self.setCentralWidget(label)

    def _show_in_center(self):
        """在屏幕中心显示"""
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = int((screen.width() - size.width()) / 2)
        y = int((screen.height() - size.height()) / 2)
        print(x, y)
        self.move(x, y)

        self.show()

    def _set_animation(self):
        """设置动画"""
        opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacity_effect)
        self.animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    def _fade_out(self):
        """淡出效果"""
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.close)

        self.animation.start()


class QtimerSingleShot(QTimer):
    """单例单次触发的计时器"""
    _instance = None
    _is_init = False
    timeStart = Signal(name='开始信号')

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if not self._is_init:
            super().__init__(parent)
            self._is_init = True
        self.setSingleShot(True)  # 设置为单次触发

    def start(self):
        super().start()
        self.timeStart.emit()


class ThreadListenSocket(QThread):
    """监听本地端口的子线程"""
    signal_receive_args = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.host = '127.0.0.1'  # 主机地址
        self.port = '9527'  # 端口
        self.client_limit_count = 2  # 同时连接的客户端上限

    def set_host(self, host: str):
        """设置主机地址"""
        self.host = host

    def set_port(self, port: str):
        """设置端口"""
        self.port = port

    def set_client_limit_count(self, count: int):
        """设置同时连接的客户端上限"""
        self.client_limit_count = count

    def get_host(self):
        """获取绑定的主机地址"""
        return self.host

    def get_port(self):
        """获取绑定的端口"""
        return self.port

    def get_client_limit_count(self):
        """获取同时连接的客户端上限"""
        return self.client_limit_count

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(self.client_limit_count)
        while True:
            connection, client_address = sock.accept()
            try:
                # 接收数据
                data = connection.recv(1024)
                if data:
                    args = pickle.loads(data)
                    # 打印接收到的参数
                    print(f'接收参数：{args}')
                    self.signal_receive_args.emit(args)
            finally:
                connection.close()  # 关闭连接


class ToolButtonRightClick(QToolButton):
    """支持右键点击信号的QToolButton"""
    rightClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setMouseTracking(True)
        self.customContextMenuRequested.connect(self._emit_signal)

    def _emit_signal(self):
        self.rightClicked.emit()


class DialogGifPlayer(QDialog):
    """播放GIF动画的QDialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        set_transparent_background(self)

        # 添加label
        self.label_gif = QLabel('GIF PLAYER')
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label_gif)

        # 添加动画对象
        self.gif = None

    def set_gif(self, gif: str):
        """设置gif
        :param gif: str，gif文件路径"""
        self.gif = QMovie(gif)
        self.label_gif.setMovie(self.gif)

    def play(self):
        self.gif.start()
        self.show()

    def stop(self):
        self.gif.stop()
        self.close()


class LabelHoverInfo(QLabel):
    """自动隐藏的悬浮在控件左下角的label（用于显示提示信息）"""

    _instance = None
    _is_init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if not self._is_init:
            super().__init__(parent)
            self._is_init = True

            self.setMouseTracking(True)
            self.setStyleSheet("color: blue;")
            self.setWordWrap(True)
            self.hide()
            self.raise_()  # 置顶

            self.duration = 1  # 显示时长，秒
            self.position = 'LB'  # 显示位置，RT/RB/LT/LB

            # 设置定时器
            self.timer_hidden = QTimer()
            self.timer_hidden.setSingleShot(True)
            self.timer_hidden.timeout.connect(self.hide)

    def set_duration(self, duration: float):
        """设置显示时长，秒"""
        self.duration = duration

    def set_position(self, position: str):
        """设置显示位置
        :param position: str，RT/RB/LT/LB"""
        if position.upper() not in ['RT', 'RB', 'LT', 'LB']:
            raise Exception('参数错误，请选择RT/RB/LT/LB')
        self.position = position.upper()

    def _show(self, text: str):
        """显示信息"""
        self.setText(text)
        self.reset_position()
        self.show()
        self.timer_hidden.start(self.duration * 1000)

    def reset_position(self):
        """重设坐标轴位置"""
        width, height = self.sizeHint()
        parent_width, parent_height = self.parent().size()

        if self.position == 'LT':  # LT左上角
            self.setGeometry(0, 0, width, height)
        elif self.position == 'LB':  # LB左下角
            self.setGeometry(0, parent_height - height, width, height)
        elif self.position == 'RT':  # RT右上角
            self.setGeometry(parent_width - width, 0, width, height)
        elif self.position == 'RB':  # RB右下角
            self.setGeometry(parent_width - width, parent_height - height, width, height)


class WidgetAutoHidden(QWidget):
    """悬停时显示，离开时隐藏的Widget"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置计时器
        self.qtimer_hidden = QTimer()
        self.qtimer_hidden.setInterval(500)
        self.qtimer_hidden.setSingleShot(True)
        self.qtimer_hidden.timeout.connnect(self.hide)

    def set_interval(self, second: float):
        """设置延迟隐藏的时间间隔"""
        self.qtimer_hidden.setInterval(int(second * 1000))

    def enterEvent(self, event):
        super().enterEvent(event)
        self.show()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.qtimer_hidden.start()


class StyledItemDelegateImage(QStyledItemDelegate):
    """项目视图委托QStyledItemDelegate，在QStandardItem中显示自适应大小的图像
    注意：图像路径需在保存在QStandardItem的UserRole属性中"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        # 获取QStandardItem中的图片数据
        pixmap = index.data(Qt.UserRole)
        if not pixmap:
            raise Exception('错误，图像路径需在保存在QStandardItem的UserRole属性中')

        # 创建绘制工具
        item_rect = option.rect
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)

        # 缩放图片以适应QStandardItem
        scaled_pixmap = pixmap.scaled(QSize(item_rect.width(), item_rect.height()),
                                      Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # 在QStandardItem上绘制图片
        painter.drawPixmap(item_rect.x() + (item_rect.width() - scaled_pixmap.width()) / 2,
                           item_rect.y() + (item_rect.height() - scaled_pixmap.height()) / 2,
                           scaled_pixmap.width(), scaled_pixmap.height(), scaled_pixmap)
