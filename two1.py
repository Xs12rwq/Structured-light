# 开发时间：2025/7/20 20:03
import os
import numpy as np
from numpy import mat, sqrt, zeros
from scipy.io import savemat
import matplotlib.pyplot as plt
import scipy.io as scio
from pylab import mpl

def calculateEquationParameters(x):
    parameter = []
    sizeOfInterval = len(x) - 1
    i = 1
    while i < len(x) - 1:
        data = init(sizeOfInterval * 3)
        data[(i - 1) * 3] = x[i] * x[i]
        data[(i - 1) * 3 + 1] = x[i]
        data[(i - 1) * 3 + 2] = 1
        data1 = init(sizeOfInterval * 3)
        data1[i * 3] = x[i] * x[i]
        data1[i * 3 + 1] = x[i]
        data1[i * 3 + 2] = 1
        temp = data[1:]
        parameter.append(temp)
        temp = data1[1:]
        parameter.append(temp)
        i += 1
    data = init(sizeOfInterval * 3 - 1)
    data[0] = x[0]
    data[1] = 1
    parameter.append(data)
    data = init(sizeOfInterval * 3)
    data[(sizeOfInterval - 1) * 3 + 0] = x[-1] * x[-1]
    data[(sizeOfInterval - 1) * 3 + 1] = x[-1]
    data[(sizeOfInterval - 1) * 3 + 2] = 1
    temp = data[1:]
    parameter.append(temp)
    i = 1
    while i < len(x) - 1:
        data = init(sizeOfInterval * 3)
        data[(i - 1) * 3] = 2 * x[i]
        data[(i - 1) * 3 + 1] = 1
        data[i * 3] = -2 * x[i]
        data[i * 3 + 1] = -1
        temp = data[1:]
        parameter.append(temp)
        i += 1
    return parameter

def init(size):
    return [0 for _ in range(size)]

def solutionOfEquation(parametes, y):
    sizeOfInterval = len(x) - 1
    result = init(sizeOfInterval * 3 - 1)
    i = 1
    while i < sizeOfInterval:
        result[(i - 1) * 2] = y[i]
        result[(i - 1) * 2 + 1] = y[i]
        i += 1
    result[(sizeOfInterval - 1) * 2] = y[0]
    result[(sizeOfInterval - 1) * 2 + 1] = y[-1]
    a = np.array(calculateEquationParameters(x))
    b = np.array(result)
    return np.linalg.solve(a, b)

def calculate(parameters, x):
    result = []
    for data_x in x:
        result.append(parameters[0] * data_x * data_x + parameters[1] * data_x + parameters[2])
    return result

# =======================主循环开始=======================

calib_folder = "D:\单目结构光系统"
dataFile_x = 'D:\单目结构光系统/xx_tie1.mat'
dataFile_y = 'D:\单目结构光系统/yy_tie1.mat'
dataX = scio.loadmat(dataFile_x)
dataY = scio.loadmat(dataFile_y)

aa = dataX['xx1']
bb = dataY['yy1']
gray = mat(zeros((1, 131610)))

for i in range(131610):
    print(i)
    x = [0, 0, 0]
    y = [0, 0, 0]

    x1 = aa[i]
    x[0] = int(x1[0])
    x[1] = int(x1[1])
    x[2] = int(x1[2])

    y1 = bb[i]
    y[0] = int(y1[0])
    y[1] = int(y1[1])
    y[2] = int(y1[2])

    print(x)
    print(y)

    try:
        result = solutionOfEquation(calculateEquationParameters(x), y)
    except Exception as e:
        print(f"i={i}, 解方程异常: {e}")
        gray[0, i] = 0
        continue

    new_data_x1 = np.arange(x[0], x[1], 1)
    new_data_y1 = calculate([0, result[0], result[1]], new_data_x1)
    new_data_x2 = np.arange(x[1], x[2], 1)
    new_data_y2 = calculate([result[2], result[3], result[4]], new_data_x2)

    # -----核心：安全二次反查+防呆处理-----
    A = result[2]
    B = result[3]
    C = result[4] - 250
    delta = B * B - 4 * A * C

    # A接近0则退化为一次方程
    if abs(A) < 1e-8:
        print(f"i={i}, 警告: 二次项为0，降为一次方程。")
        if abs(B) > 1e-8:
            r1 = -C / B
            print(f"用一次方程反解 r1={r1}")
            gray[0, i] = int(r1)
        else:
            print(f"i={i}, 警告: 一次项也为0，无法反解。填0。")
            gray[0, i] = 0
        continue

    if delta < 0:
        print(f"i={i}, 警告: 判别式<0，无法实数反解。区间内查找最大/最接近点处理。")
        s = [int(new_data_y2[k]) for k in range(len(new_data_x2))]
        max_data = max(s)
        if max_data <= 250:
            gray[0, i] = int(new_data_x2[s.index(max_data)])
        else:
            found = False
            for n in range(len(new_data_x2)):
                if s[n] == 250:
                    gray[0, i] = int(new_data_x2[n])
                    found = True
                    break
                if s[n] > 250:
                    gray[0, i] = int(new_data_x2[n-1])
                    found = True
                    break
            if not found:
                gray[0, i] = int(new_data_x2[0])  # 兜底
        continue

    # 正常二次方程反解
    r1 = (-B + sqrt(delta)) / (2 * A)
    r2 = (-B - sqrt(delta)) / (2 * A)

    # 选区间内的r1，否则修正
    if int(r1) < int(x[0]):
        print(f"i={i}, r1={r1}落在区间外，进入修正处理。")
        s = [int(new_data_y2[k]) for k in range(len(new_data_x2))]
        max_data = max(s)
        if max_data <= 250:
            gray[0, i] = int(new_data_x2[s.index(max_data)])
        else:
            found = False
            for n in range(len(new_data_x2)):
                if s[n] == 250:
                    gray[0, i] = int(new_data_x2[n])
                    found = True
                    break
                if s[n] > 250:
                    gray[0, i] = int(new_data_x2[n-1])
                    found = True
                    break
            if not found:
                gray[0, i] = int(new_data_x2[0])
    else:
        gray[0, i] = int(r1)

# 保存结果
savemat(os.path.join(calib_folder, "graytie6.mat"), {
        "gray": gray})

