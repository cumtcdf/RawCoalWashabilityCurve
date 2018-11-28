# -*- coding: utf-8 -*-
# @Time    : 2018-06-10 21:35
# @Author  : F
# @Email   : cumtcdf@126.com
# @File    : row.py
# @Software: PyCharm

__author__ = "cdf"

from RawCoalWashabilityCurve import Row, Curve
from RcwcGui.application import Application
if __name__ == '__main__':
    # test_data = [
    #     Row(0.0, 1.3, 3.46, 10.69),
    #     Row(1.3, 1.4, 8.23, 46.15),
    #     Row(1.4, 1.5, 15.50, 20.14),
    #     Row(1.5, 1.6, 25.50, 5.17),
    #     Row(1.6, 1.7, 34.28, 2.55),
    #     Row(1.7, 1.8, 42.94, 1.62),
    #     Row(1.8, 2.0, 52.91, 2.13),
    #     Row(2.0, 2.5, 79.64, 11.55),
    # ]
    # cur = Curve(test_data)
    # cur.show()
    app = Application(False)
    app.run()



