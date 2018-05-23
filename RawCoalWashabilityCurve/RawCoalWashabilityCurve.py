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
        self.y = np.array(self.GetValues(self.x))

    def _GetPlotFitData(self):
        if self.xData[0] > self.xData[-1]:
            self.xData.reverse()
            self.yData.reverse()
        fx = interpolate.splrep(self.xData, self.yData)
        return fx

    def Add(self, x, y):
        self.xData.append(x)
        self.yData.append(y)

    def GetValues(self, x):
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
        self._axs = []
        self._GetSinksData()
        self._GetFloatsLine()
        self._GetRawAshLine()
        self._GetNear01Line()
        self._GetDensityLine()
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
            y += d.Productivity
            temp += d.Productivity * d.Ash
            x = temp / y if y != 0 else d.Ash
            pointList.append((x, y))
        line = Line(pointList=pointList, xMin=x, xMax=100)
        self._lines['沉物曲线'] = line
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
            y += d.Productivity
            temp += d.Productivity * d.Ash
            x = round(temp / y, 2) if y != 0 else d.Ash
            pointList.append((x, y))
        line = Line(pointList=pointList, xMin=0, xMax=x)
        self._lines['浮物曲线'] = line
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

        def _getNearest0Value(data_x, data_y):
            '''
            获取最接近0的值,因为浮物曲线/沉物曲线在
            :param data_x:
            :param data_y:
            :return:
            '''
            distance = data_y[0]
            position = data_x[0]
            for x, y in zip(data_x, data_y):
                position, distance = (x, y) if abs(distance) > abs(y) else (position, distance)
            return round(position, 2), round(distance, 2)

        self._data.sort()
        xData = [d.Ash for d in self._data]
        yData = [d.Productivity for d in self._data]
        yData = _getY1(yData)

        line = self._lines['浮物曲线']
        x1_begin, y1_begin = _getNearest0Value(line.x, line.y)
        xData.insert(0, x1_begin)
        yData.insert(0, y1_begin)
        line = self._lines['沉物曲线']
        x1_end, y1_end = _getNearest0Value(line.x, line.y)
        xData.append(x1_end)
        yData.append(100 - y1_begin)
        line = Line(pointList=list(zip(xData, yData)), xMin=0, xMax=100)
        self._lines['基元灰分曲线'] = line

    def _GetNear01Line(self):
        '''
        正负0.1含量曲线
        :return:
        '''
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
        self._lines['±0.1含量曲线'] = line

    def _GetDensityLine(self):
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
        line = Line(list(zip(xData, yData)), 1.3, 1.9)
        self._lines['密度曲线'] = line


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
