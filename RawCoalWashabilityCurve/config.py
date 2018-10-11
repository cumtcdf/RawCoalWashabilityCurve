# -*- coding: utf-8 -*-
# @Time    : 2018-06-10 22:30
# @Author  : F
# @Email   : cumtcdf@126.com
# @File    : config.py
# @Software: PyCharm

__author__ = "cdf"

import numpy as np

LINE_POINT_COUNT = 1000
# ================    ===============================
# character           description
# ================    ===============================
# ``'-'``             solid line style
# ``'--'``            dashed line style
# ``'-.'``            dash-dot line style
# ``':'``             dotted line style
# ``'.'``             point marker
# ``','``             pixel marker
# ``'o'``             circle marker
# ``'v'``             triangle_down marker
# ``'^'``             triangle_up marker
# ``'<'``             triangle_left marker
# ``'>'``             triangle_right marker
# ``'1'``             tri_down marker
# ``'2'``             tri_up marker
# ``'3'``             tri_left marker
# ``'4'``             tri_right marker
# ``'s'``             square marker
# ``'p'``             pentagon marker
# ``'*'``             star marker
# ``'h'``             hexagon1 marker
# ``'H'``             hexagon2 marker
# ``'+'``             plus marker
# ``'x'``             x marker
# ``'D'``             diamond marker
# ``'d'``             thin_diamond marker
# ``'|'``             vline marker
# ``'_'``             hline marker
# ================    ===============================
RED, YELLOW, BLUE, GREEN, MAGENTA, BLACK, WHITE, CYAN = \
    'r', 'y', 'b', 'g', 'm', 'k', 'w', 'c'

LINES_STYLE = {
    '基元灰分曲线': (RED, "*"),
    '浮物曲线': (GREEN, "*"),
    '沉物曲线': (MAGENTA, "*"),
    '±0.1含量曲线': (YELLOW, "*"),
    '密度曲线': (BLUE, "*")
}

LABELS_VISIBLE = True
BBOX_TO_ANCHOR = (1.05, 1)
TICKS_0_110 = np.linspace(0, 100, 11)
TICKS_12_22 = np.linspace(1.2, 2.2, 11)

FONTS = {
    "FANGSONG": "C:\\WINDOWS\\FONTS\\STFANGSO.TTF",
}

LABLE_FONT = FONTS["FANGSONG"]
LEGEND_FONT=FONTS["FANGSONG"]


