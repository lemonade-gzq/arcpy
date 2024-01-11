#-*- encoding:utf-8 -*-
import sys   #reload()之前必须要引入模块
reload(sys)
sys.setdefaultencoding('utf-8')

import arcpy
from arcpy import env
from arcpy.sa import *

# env.workspace = r"E:\城市与区域生态\大熊猫和竹\平武种群动态模拟\考虑季节性迁徙的模拟结果\独立个体"  # 设置工作空间，用于后面遍历矢量文件
# point_ds = arcpy.ListFeatureClasses()  # 遍历工作空间路径内的所有矢量，生成列表存放矢量文件名
# arcpy.env.extent = r"E:\\城市与区域生态\\大熊猫和竹\\种群动态模拟\\平武dem.tif"
# arcpy.env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 UTM Zone 48N")
# pdensout = []
# for point in point_ds:  # 遍历矢量文件
#     out = PointDensity(point, "NONE", cell_size=500, area_unit_scale_factor="SQUARE_KILOMETERS",
#                        neighborhood=NbrCircle(4000, "MAP"))
#     out.save('E:\\城市与区域生态\\大熊猫和竹\\平武种群动态模拟\\考虑季节性迁徙的模拟结果\\独立个体模拟密度' + '\\pointdensity' + point.split('.')[0] + '.tif')
#     print (point.split('.')[0])


env.workspace = "E:\\城市与区域生态\\大熊猫和竹\\平武种群动态模拟\\考虑季节性迁徙的模拟结果\\独立个体模拟密度"
rasters = arcpy.ListRasters()  # 遍历工作空间路径内的所有栅格
Sum1 = 0
for raster in rasters:
    Sum1 = Sum1 + Raster(raster)
Sum1 /= len(rasters)
Sum1.save(env.workspace + '\\moniaverage_4k.tif')
