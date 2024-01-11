# coding=utf-8
import arcpy
from arcpy import env

env.workspace = r"E:\城市与区域生态\大熊猫和竹\道路对大熊猫栖息地的影响\道路距离分析\15all条带1229"  # 设置工作空间，用于后面遍历矢量文件
fcl = arcpy.ListFeatureClasses()  # 遍历工作空间路径内的所有矢量，生成列表存放矢量文件名
for fc in fcl:  # 遍历矢量文件，逐一增加属性字段“所属乡”，类型为text，长度为50
    # arcpy.AddField_management(fc, "distance", "TEXT", "", "", "50", "distance", "NULLABLE", "NON_REQUIRED")
    # arcpy.DeleteField_management(fc, "No")
    arcpy.AddField_management(fc, "No", "SHORT", "", "", "50", "no", "NULLABLE", "NON_REQUIRED")

for i in range(len(fcl)):  # 调用字段计算器将fc矢量的"所属乡"字段赋值为"fc"(print(fc)可以发现，fc就是"文件名.shp")
    str = fcl[i].encode("utf-8")
    n = int(str.split('_')[1])
    # str = "{0}_{1}".format(n, n + 500)
    # arcpy.CalculateField_management(fcl[i], "distance", "\"" + str + "\"")
    # str = "{}".format(n / 500 + 1)
    arcpy.CalculateField_management(fcl[i], "No", n / 500 + 1)
