# -*- encoding:utf-8 -*-
import sys  # reload()之前必须要引入模块
import arcpy
import numpy as np
from collections import Counter
from arcpy.sa import *
reload(sys)
sys.setdefaultencoding('utf-8')

arcpy.env.workspace = "E:\\result\\ECOSERVICE"
arcpy.ClearWorkspaceCache_management()  # 在指明工作空间后使用
arcpy.Delete_management("in_memory")
rasters = arcpy.ListRasters("*", "tif")
for raster in rasters:
    path = arcpy.env.workspace + "\\" + raster
    data = Int(path)
    data = arcpy.RasterToNumPyArray(data)

    nodata = data[0, 0]
    cols = data.shape[1]
    rows = data.shape[0]
    print(cols, rows)
    print (data.shape)
    print (data[0])
    value_count = {}
    for i in range(rows):
        data_1d = data[i]
        data_list = data_1d.tolist()
        value_count_1 = Counter(data_list)
        common_keys = set(value_count.keys()) & set(value_count_1.keys())
        different_keys = set(value_count_1.keys()) - set(value_count.keys())
        for key in common_keys:
            value_count[key] = value_count[key] + value_count_1[key]
        for key in different_keys:
            value_count[key] = value_count_1[key]
        del value_count_1

    del value_count[nodata]  # 删除无效值
    print(value_count)
    print("-" * 20)

    value_multiply = dict()  # value * count并放入该字典的值中
    for key, value in value_count.items():
        value_multiply[key] = float(key * value / 1000)
    print("value_multiply,乘积字典", value_multiply)
    print("-" * 20)
    # value_order_multiply = sorted(zip(value_multiply.values(), value_multiply.keys()))  # 对（值键对）排序，并返回一个元素为元组的列表
    # for i in range(len(value_order_multiply)):
    #     value_count[value_order_multiply[i][1]] = value_order_multiply[i][0]
        # value_order_multiply[i] = list(value_order_multiply[i])
        # value_order_multiply[i][0] = i
    # print("order key value", value_count)
    # print(value_order_multiply[1])
    # print(type(value_order_multiply))
    print("-" * 20)

    order_multiply = []  # 提取排好序的value*count
    for value in value_multiply.values():
        order_multiply.append(value)
    print("order multiply list", order_multiply)
    print("-" * 20)
    order_multiply = np.array(order_multiply)
    order_accumulate = np.cumsum(order_multiply)  # 每个元素和前面的所有元素相加
    print("accumulate array", order_accumulate)
    print("-" * 20)

    level_1, level_2, level_3, level_4 = [], [], [], []
    # value_order_multiply = dict(value_order_multiply)
    value_count = list(value_count.items())
    Threshold75 = order_accumulate[-1] * 0.75
    Threshold90 = order_accumulate[-1] * 0.9
    Threshold50 = order_accumulate[-1] * 0.5
    Threshold25 = order_accumulate[-1] * 0.25
    Threshold10 = order_accumulate[-1] * 0.1
    for i in range(len(order_accumulate)):
        if (order_accumulate[i] < Threshold50) and (order_accumulate[i] >= Threshold25):
            level_3.append(value_count[i][0])
        elif (order_accumulate[i] < Threshold25) and (order_accumulate[i] >= Threshold10):
            level_2.append(value_count[i][0])
        elif (order_accumulate[i] < Threshold10) and (order_accumulate[i] >= 0):
            level_1.append(value_count[i][0])
        else:
            level_4.append(value_count[i][0])
            # level_4.append(value_order_multiply[order_multiply[i]])
    print("level1", level_1)
    print("level2", level_2)
    print("level3", level_3)
    print("level4", level_4)

    remap = []
    for i in range(len(level_1)):
        remap.append([level_1[i], 1])
    for i in range(len(level_2)):
        remap.append([level_2[i], 2])
    for i in range(len(level_3)):
        remap.append([level_3[i], 3])
    for i in range(len(level_4)):
        remap.append([level_4[i], 4])

    outReclass1 = Reclassify(path, "VALUE", RemapValue(remap))
    outReclass1.save("E:\\result\\ECOSERVICE\\rc\\" + raster)



    del path, data, data_1d, data_list, value, value_count, value_multiply, order_multiply, order_accumulate, level_4, level_1, level_2, level_3
    arcpy.ClearWorkspaceCache_management()  # 在代码结束后使用
    arcpy.Delete_management("in_memory")
