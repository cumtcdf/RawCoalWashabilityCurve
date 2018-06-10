# -*- coding: utf-8 -*-
# @Time    : 2018-06-10 21:35
# @Author  : F
# @Email   : cumtcdf@126.com
# @File    : row.py
# @Software: PyCharm

__author__ = "cdf"


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
