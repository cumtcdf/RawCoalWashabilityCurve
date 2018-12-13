# -*- coding: utf-8 -*-
# @Time    : 2018-06-10 21:39
# @Author  : F
# @Email   : cumtcdf@126.com
# @File    : line.py
# @Software: PyCharm

__author__ = "cdf"
from scipy import interpolate
import numpy as np

from .config import *


class Line:
    def __init__(self, pointList, xMin, xMax, nk=3):
        self.nk = nk
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
