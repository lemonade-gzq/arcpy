#-*- encoding:utf-8 -*-
import sys   #reload()之前必须要引入模块
reload(sys)
sys.setdefaultencoding('utf-8')

import arcpy
from arcpy import env
from arcpy.sa import *

env.workspace = r"E:\\城市与区域生态\\大熊猫和竹\\平武种群动态模拟\\only_ndr\\考虑季节性迁徙的模拟结果\\2"  # 设置工作空间，用于后面遍历矢量文件
point_ds = arcpy.ListFeatureClasses()  # 遍历工作空间路径内的所有矢量，生成列表存放矢量文件名
arcpy.env.extent = r"E:\\城市与区域生态\\大熊猫和竹\\种群动态模拟\\平武dem.tif"
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 UTM Zone 48N")
pdensout = []
for line in point_ds:  # 遍历矢量文件
    out = LineDensity(line, "NONE", cell_size=500, area_unit_scale_factor="SQUARE_KILOMETERS",
                       search_radius=4000)
    out.save('E:\\城市与区域生态\\大熊猫和竹\\平武种群动态模拟\\only_ndr\\考虑季节性迁徙的模拟结果\\轨迹密度' + '\\pointdensity' + line.split('.')[0] + '.tif')
    print (line.split('.')[0])