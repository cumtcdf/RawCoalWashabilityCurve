# -*- coding: utf-8 -*-
# @Time    : 05/21/2018 21:04
# @Email   : cumtcdf@126.com
# @File    : RawCoalWashabilityCurve.py
__author__ = "cdf"

import matplotlib.pyplot as plt
from scipy import interpolate
from collections import Iterable
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


class Row:
    def __init__(self, flow, ceil, ash, productivity):
        self.FlowDensity = flow
        self.CeilDensity = ceil
        self.Ash = round(ash, 2)
        self.Productivity = round(productivity, 2)

    def __cmp__(self, other):
        if self.FlowDensity < other.FlowDensity:
            return -1
        elif self.FlowDensity > other.FlowDensity:
            return 1
        else:
            return 0

    def __lt__(self, other):
        return self.FlowDensity < other.FlowDensity

    def __repr__(self):
        return 'Row({0} , {1} , {2:.2f} , {3:.2f})'.format(self.FlowDensity, self.CeilDensity, self.Ash / 100,
                                                           self.Productivity / 100)


class Line:
    def __init__(self, pointList, xMin, xMax):
        self.xData = []
        self.yData = []
        self.xMin, self.xMax = xMin, xMax
        for x, y in pointList:
            self.Add(x, y)
        self._fx = self._GetPlotFitData()
        self.x = np.linspace(xMin, xMax, num=LINE_POINT_COUNT, endpoint=True)
        self.y = np.array(self._GetValues(self.x))
        self.fx = interpolate.interp1d(self.x, self.y)
        self.fy = interpolate.interp1d(self.y, self.x)

    def _GetPlotFitData(self):
        if self.xData[0] > self.xData[-1]:
            self.xData.reverse()
            self.yData.reverse()
        fx = interpolate.splrep(self.xData, self.yData)
        return fx

    def Add(self, x, y):
        self.xData.append(x)
        self.yData.append(y)

    def _GetValues(self, x):
        intFlag = False
        if isinstance(x, int):
            intFlag = True
            x = [x]
        y = interpolate.splev(x, self._fx)
        return y if not intFlag else y[0]


class RawCoalWashabilityCurve(object):

    def __init__(self, data):
        if not isinstance(data, Iterable):
            raise TypeError('data must be Iterable!')
        temp = 0
        for d in data:
            if not isinstance(d, Row):
                raise TypeError('data member need Row class!')
            else:
                temp += round(d.Productivity, 2)

        if round(temp, 2) != 100:
            raise ValueError('浮沉数据中产率之和不为100!')

        self._data = data
        self._lines = {}
        self._interps = []
        self._fig = None
        self._axs = None
        self._plt = None
        self._GetFig()
        self._GetSinksData()
        self._GetFloatsLine()
        self._GetRawAshLine()
        self._GetNear01Line()
        self._GetDensityLine()
        pass

    def _GetFig(self):
        '''
                创建坐标系
            '''
        from pylab import mpl
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        fig, ax1 = plt.subplots()
        plt.grid(True, linestyle="-.", color=BLACK)
        plt.ylabel('浮物产率(%)')
        plt.xlabel('灰分(%)')
        plt.xlim((0, 100))
        plt.ylim((0, 100))
        plt.xticks(TICKS_0_110)
        plt.yticks(TICKS_0_110)
        plt.gca().invert_yaxis()
        ax2 = ax1.twinx()
        plt.ylabel('沉物产率(%)')
        plt.ylim((0, 100))
        plt.yticks(TICKS_0_110)
        ax3 = ax1.twiny()
        plt.xlabel('密度(g/L)')
        plt.xlim((1.2, 2.2))
        plt.xticks(TICKS_12_22)
        plt.gca().invert_xaxis()
        self._axs = (ax1, ax2, ax3)
        self._fig = fig

    def _GetSinksData(self):
        '''
        获取沉物曲线值
        :return:
        '''
        name = '沉物曲线'
        axindex = 1
        pointList = []
        x, y, temp = 0, 0, 0
        self._data.sort(reverse=True)
        for d in self._data:
            y += d.Productivity
            temp += d.Productivity * d.Ash
            x = temp / y if y != 0 else d.Ash
            pointList.append((x, y))
        line = Line(pointList=pointList, xMin=x, xMax=100)
        style = LINES_STYLE[name]
        self._lines[name] = (line, self._axs[axindex], style)
        return

    def _GetFloatsLine(self):
        '''
        获取浮物曲线值
        :return:
        '''
        name = '浮物曲线'
        axindex = 0
        pointList = []
        x, y, temp = 0, 0, 0
        self._data.sort()
        for d in self._data:
            y += d.Productivity
            temp += d.Productivity * d.Ash
            x = round(temp / y, 2) if y != 0 else d.Ash
            pointList.append((x, y))
        line = Line(pointList=pointList, xMin=0, xMax=x)
        style = LINES_STYLE[name]
        self._lines[name] = (line, self._axs[axindex], style)
        return

    def _GetRawAshLine(self):
        '''
        基元灰分曲线
        :return:
        '''

        def _getY1(datas):
            '''
            基元灰分曲线y值
            :param datas:   基元灰分源值
            :return:        对应y轴坐标值
            '''
            res = []
            sum = 0
            for i in range(len(datas)):
                sum += datas[i]
                res.append(sum - datas[i] / 2)
            return res

        name = '基元灰分曲线'
        axindex = 0
        self._data.sort()
        xData = [d.Ash for d in self._data]
        yData = [d.Productivity for d in self._data]
        yData = _getY1(yData)

        line, _, _ = self._lines['浮物曲线']
        x1_begin, y1_begin = line.fy(0), 0
        xData.insert(0, x1_begin)
        yData.insert(0, y1_begin)
        line, _, _ = self._lines['沉物曲线']
        x1_end, y1_end = line.fy(0), 0
        xData.append(x1_end)
        yData.append(100 - y1_begin)
        line = Line(pointList=list(zip(xData, yData)), xMin=0, xMax=100)
        style = LINES_STYLE[name]
        self._lines[name] = (line, self._axs[axindex], style)

    def _GetNear01Line(self):
        '''
        正负0.1含量曲线
        :return:
        '''
        name = '±0.1含量曲线'
        axindex = 2
        data = self._data
        data.sort()
        xData, yData = [], []
        for i in range(len(data) - 1):
            if data[i + 1].CeilDensity <= data[i].CeilDensity or data[i + 1].FlowDensity <= data[i].FlowDensity:
                raise ValueError('密度级参数错误,请检查!')
            if data[i + 1].FlowDensity != data[i].CeilDensity:
                raise ValueError('密度级不连续,请检查!')
            if round(data[i + 1].CeilDensity - data[i].CeilDensity, 1) == 0.1:
                xData.append(data[i].CeilDensity)
                yData.append(data[i].Productivity + data[i + 1].Productivity)
            elif round(data[i + 1].CeilDensity - data[i].CeilDensity, 1) == 0.2:
                xData.append(data[i].CeilDensity)
                yData.append(data[i].Productivity + data[i + 1].Productivity / 2)
            elif round(data[i].CeilDensity - data[i].FlowDensity, 1) == 0.2:
                xData.append(data[i].CeilDensity - 0.1)
                yData.append(data[i].Productivity)
        line = Line(list(zip(xData, yData)), 1.3, 1.9)
        style = LINES_STYLE[name]
        self._lines[name] = (line, self._axs[axindex], style)

    def _GetDensityLine(self):
        name = '密度曲线'
        axindex = 2
        sum = 0
        data = self._data
        data.sort()
        xData, yData = [], []
        for row in data:
            if row.CeilDensity > 2:
                continue
            sum += row.Productivity
            xData.append(row.CeilDensity)
            yData.append(sum)
            if round(row.CeilDensity - row.FlowDensity, 1) == .2:
                xData.append(row.FlowDensity + .1)
                yData.append(sum - row.Productivity / 2)
        xData.sort()
        yData.sort()
        line = Line(list(zip(xData, yData)), 1.3, 2.0)
        style = LINES_STYLE[name]
        self._lines[name] = (line, self._axs[axindex], style)

    def _GetFig(self):
        '''
                创建坐标系
            '''
        from pylab import mpl
        mpl.rcParams['font.sans-serif'] = ['SimHei']
        fig, ax1 = plt.subplots()
        plt.grid(True, linestyle="-.", color="k")
        plt.ylabel('浮物产率(%)')
        plt.xlabel('灰分(%)')
        plt.xlim((0, 100))
        plt.ylim((0, 100))
        plt.xticks(TICKS_0_110)
        plt.yticks(TICKS_0_110)
        plt.gca().invert_yaxis()
        ax2 = ax1.twinx()
        plt.ylabel('沉物产率(%)')
        plt.ylim((0, 100))
        plt.yticks(TICKS_0_110)
        ax3 = ax1.twiny()
        plt.xlabel('密度(g/L)')
        plt.xlim((1.2, 2.2))
        plt.xticks(TICKS_12_22)
        plt.gca().invert_xaxis()
        self._axs = (ax1, ax2, ax3)
        self._fig = fig
        self._plt = plt

    def show(self):
        lines = []
        labels = []
        for label, L in self._lines.items():
            l, ax, (color, marker) = L
            line, = ax.plot(l.x, l.y, color=color)
            ax.plot(l.xData, l.yData, marker)
            lines.append(line)
            labels.append(label)
        if LABELS_VISIBLE:
            self._plt.legend(handles=lines, labels=labels, bbox_to_anchor=BBOX_TO_ANCHOR)
        self._plt.show()


if __name__ == '__main__':
    test_data = [
        Row(0.0, 1.3, 3.46, 10.69),
        Row(1.3, 1.4, 8.23, 46.15),
        Row(1.4, 1.5, 15.50, 20.14),
        Row(1.5, 1.6, 25.50, 5.17),
        Row(1.6, 1.7, 34.28, 2.55),
        Row(1.7, 1.8, 42.94, 1.62),
        Row(1.8, 2.0, 52.91, 2.13),
        Row(2.0, 2.5, 79.64, 11.55),
    ]

    cur = RawCoalWashabilityCurve(test_data)
    cur.show()
