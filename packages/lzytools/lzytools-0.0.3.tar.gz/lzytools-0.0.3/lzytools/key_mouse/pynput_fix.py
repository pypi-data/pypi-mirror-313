"""
修复pynput模块中HotKey类的问题，使其能够正确识别小键盘数字（bug为小键盘数字的'_scan'属性没有被正确地赋值）
"""

from pptools.key_mouse import _src_pynput


class HotKeyFix(_src_pynput.HotKeyFix):
    """"""


class GlobalHotKeysFix(_src_pynput.GlobalHotKeysFix):
    """"""
