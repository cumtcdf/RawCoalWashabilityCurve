# -*- coding: utf-8 -*-
# @Time    : 05/21/2018 21:04
# @Email   : cumtcdf@126.com
# @File    : RawCoalWashabilityCurve.py
__author__ = "cdf"

import matplotlib.pyplot as plt
from scipy import interpolate
from collections import Iterable
import numpy as np
from decimal import Decimal

LINE_POINT_COUNT = 10000
LABELS = ['基元灰分曲线', '浮物曲线', '沉物曲线', '±0.1含量曲线', '密度曲线']
LABELS_VISIBLE = True
BBOX_TO_ANCHOR = (1.05, 1)
TICKS_0_110 = [i for i in range(0, 110, 10)]
TICKS_12_22 = [i / 10 for i in range(12, 23, 1)]


class Row:
    def __init__(self, flow, ceil, ash, productivity):
        self.FlowDensity = flow
        self.CeilDensity = ceil
        self.Ash = round(ash * 100)
        self.Productivity = round(productivity * 100)

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
    def __init__(self, pointList):
        self.xData = []
        self.yData = []
        for x, y in pointList:
            self.Add(x, y)
        self._fx = self._GetPlotFitDataX()
        # self._fy = self._GetPlotFitDataY()

    def _GetPlotFitDataX(self):
        fx = interpolate.splrep(self.xData, self.yData)
        return fx

    # def _GetPlotFitDataY(self):
    #     fy = interpolate.splrep(self.yData, self.xData)
    #     return fy

    def Add(self, x, y):
        self.xData.append(x)
        self.yData.append(y)

    def GetValueX(self, x):
        intFlag = False
        if isinstance(x, int):
            intFlag = True
            x = [x]
        y = interpolate.splev(x, self._fx)
        return [i for i in y] if not intFlag else y[0]

    # def GetValuesY(self, y):
    #     intFlag = False
    #     if isinstance(y, int):
    #         intFlag = True
    #         y = [y]
    #     x = interpolate.splev(y, self._fx)
    #     return [i for i in x] if not intFlag else x[0]


class RawCoalWashabilityCurve(object):

    def __init__(self, data):
        if not isinstance(data, Iterable):
            raise TypeError('data must be Iterable!')
        temp = 0
        for d in data:
            if not isinstance(d, Row):
                raise TypeError('data member need Row class!')
            else:
                temp += d.Productivity

        if temp != 10000:
            raise ValueError('浮沉数据中产率之和不为100!')

        self._data = data
        self._lines = {}
        self._interps = []
        self._fig = None
        self._axs = []
        self._GetSinksData()
        self._GetFloatsLine()
        pass

    def _GetSinksData(self):
        '''
        获取沉物曲线值
        :return:
        '''
        pointList = []
        x, y, temp = 0, 0, 0
        self._data.sort(reverse=True)
        for d in self._data:
            x += d.Productivity
            temp += d.Productivity * d.Ash
            y = temp / x if x != 0 else d.Ash
            pointList.append((x, y))
        line = Line(pointList=pointList)
        self._lines['sink'] = line
        return

    def _GetFloatsLine(self):
        '''
        获取浮物曲线值
        :return:
        '''
        pointList = []
        x, y, temp = 0, 0, 0
        self._data.sort()
        for d in self._data:
            x += d.Productivity
            temp += d.Productivity * d.Ash
            y = temp / x
            pointList.append((x, y))
        line = Line(pointList=pointList)
        self._lines['float'] = line
        return


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
