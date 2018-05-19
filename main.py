# encoding utf-8
'''
    原煤可选性曲线绘制
'''
import matplotlib.pyplot as plt
from scipy import interpolate

LINE_POINT_COUNT = 1000
LABELS = ['基元灰分曲线', '浮物曲线', '沉物曲线', '±0.1含量曲线', '密度曲线']
LABELS_VISIBLE = True
BBOX_TO_ANCHOR = (1.05, 1)
TICKS_0_110 = [i for i in range(0, 110, 10)]
TICKS_12_22 = [i / 10 for i in range(12, 23, 1)]


def GetPlotFitData(data_x, data_y, xMin, xMax):
    '''
    样条插值拟合
    :param data_x:  x轴源数据
    :param data_y:  y轴元数据
    :param xMin:    拟合后的x轴下限
    :param xMax:    拟合后的x轴上限
    :return:        拟合后的x,y轴数据
    '''
    t = interpolate.splrep(data_x, data_y)
    # fq = interp1d(data_x, data_y, kind='spline')
    x = [xMin + (xMax - xMin) * i / LINE_POINT_COUNT for i in range(LINE_POINT_COUNT)]
    # x = np.linspace(min(data_x), max(data_x), 1000 , endpoint=True)
    # y = fq(x)
    y = interpolate.splev(x, t)
    return x, [i for i in y]


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
    distance = data_y[0]
    for point in zip(data_x, data_y):
        x, y = point
        distance = y if abs(distance) > abs(y) else distance
    return data_x[data_y.index(distance)], distance


'''
    基元灰分曲线
'''
data_x1 = [3.46, 8.23, 15.50, 25.50, 34.28, 42.94, 52.91, 79.64, ]
data_y1 = [10.69, 46.15, 20.14, 5.17, 2.55, 1.62, 2.13, 11.55, ]

'''
    浮物曲线
'''
data_x2 = [3.46, 7.33, 9.47, 10.48, 11.19, 11.79, 12.78, 20.50, ]
data_y2 = [10.69, 56.84, 76.98, 82.15, 84.70, 86.32, 88.45, 100.00, ]

'''
    沉物曲线
'''
data_x3 = [20.50, 22.54, 37.85, 57.40, 66.64, 72.04, 75.48, 79.64, ]
data_y3 = [100.00, 89.31, 43.16, 23.02, 17.85, 15.30, 13.68, 11.55, ]

'''
    ±0.1含量曲线
'''
data_x4 = [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, ]
data_y4 = [56.84, 66.29, 25.31, 7.72, 4.17, 2.69, 2.13, ]

'''
    密度曲线
'''
data_x5 = [1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, ]
data_y5 = [10.69, 56.84, 76.98, 82.15, 84.70, 86.32, 88.45, ]


def main():
    '''
        画可选性曲线
    :return:
    '''

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

    '''
        获取数据
    '''
    global data_y1
    data_y1 = _getY1(data_y1)

    x2, y2 = GetPlotFitData(data_x2, data_y2, 0, 100)

    x3, y3 = GetPlotFitData(data_x3, data_y3, 2, 100)

    x4, y4 = GetPlotFitData(data_x4, data_y4, 1.3, 1.9)
    x5, y5 = GetPlotFitData(data_x5, data_y5, 1.3, 1.9)

    '''
        用浮物曲线/沉物曲线拟合出的点,矫正基元灰分曲线.
    '''
    x1_begin, y1_begin = _getNearest0Value(x2, y2)
    x1_begin = 2.2 - x1_begin / 100 * (2.2 - 1.2)
    data_x1.insert(0, x1_begin)
    data_y1.insert(0, y1_begin)
    x1_end, y1_end = _getNearest0Value(x3, y3)
    data_x1.append(x1_end)
    data_y1.append(100 - y1_begin)
    x1, y1 = GetPlotFitData(data_x1, data_y1, 0, 100)
    '''
        绘制曲线
    '''
    line1, = ax1.plot(x1, y1, 'r')
    line2, = ax1.plot(x2, y2, 'g')
    line3, = ax2.plot(x3, y3, 'c')
    line4, = ax3.plot(x4, y4, 'y')
    line5, = ax3.plot(x5, y5, 'b')

    if LABELS_VISIBLE:
        plt.legend(
            handles=[
                line1,
                line2,
                line3,
                line4,
                line5,
            ],
            labels=LABELS,
            bbox_to_anchor=BBOX_TO_ANCHOR
        )
    plt.show()


if __name__ == "__main__":
    main()
