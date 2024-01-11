# -*- encoding:utf-8 -*-
import sys
import arcpy
import os

reload(sys)
sys.setdefaultencoding('utf-8')

# 设置 MXD 文件路径和其他参数
mxd_path = u'E:\\城市与区域生态\\大熊猫和竹\\平武种群d动态模拟新.mxd'
fc_path = r'E:/城市与区域生态/大熊猫和竹/种群动态模拟/平武保护区全.shp'
ddp_FieldName = 'BHDMC'
Export_NameField = 'BHDMC'
output = r'E:/城市与区域生态/其他/2023.07.23国家公园矢量数据审查'
rtion = 300

# 打开 MXD 文件
mxd = arcpy.mapping.MapDocument(mxd_path)

# 获取主要和鹰眼图数据框架
df_main = arcpy.mapping.ListDataFrames(mxd)[0]
df_overview = arcpy.mapping.ListDataFrames(mxd, "鹰眼图")[0]

# 获取主要数据框架中的图层列表
layers = arcpy.mapping.ListLayers(mxd, "", df_main)

# 创建一个字典，将 DDP 页面名称映射到导出 PNG 文件的名称
x = {}
cursor = arcpy.SearchCursor(fc_path)
for row in cursor:
    x[row.getValue(ddp_FieldName)] = row.getValue(Export_NameField)

# 对于字典中的每个页面，将其导出为 PNG 文件，并更新鹰眼图的范围
for pageName in x.keys():
    pageID = mxd.dataDrivenPages.getPageIDFromName(pageName)
    mxd.dataDrivenPages.currentPageID = pageID
    export_name = os.path.join(output, '{}.png'.format(x[pageName]))

    # 切换到主要数据框架并设置活动视图
    mxd.activeView = df_main.name
    arcpy.RefreshActiveView()

    # 获取当前 BHDMC 对应的要素，并将其高亮显示
    BHDMC = x[pageName]
    for layer in layers:
        if layer.isFeatureLayer:
            layer.definitionQuery = "{} = '{}'".format(ddp_FieldName, BHDMC)
            arcpy.RefreshActiveView()
            if isinstance(BHDMC, str):  # 如果 BHDMC 是字符串
                arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION",
                                                        "{} = '{}'".format(ddp_FieldName, BHDMC))
            else:  # 如果 BHDMC 是数字
                arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", "{} = {}".format(ddp_FieldName, BHDMC))
            arcpy.RefreshActiveView()
            arcpy.mapping.ExportToPNG(df_main, export_name, resolution=rtion)
            layer.definitionQuery = ""
            arcpy.RefreshActiveView()

    # 将高亮显示的要素添加到鹰眼图中
    arcpy.mapping.ExportToPNG(df_overview, export_name.replace('.png', '_overview.png'), resolution=rtion)
    df_overview_extent = df_overview.extent
    df_main_extent = df_main.extent
    df_main_extent.XMin, df_main_extent.YMin = df_overview_extent.XMin, df_overview_extent.YMin
    df_main_extent.XMax, df_main_extent.YMax = df_overview_extent.XMax, df_overview_extent.YMax
    df_main.extent = df_main_extent
    arcpy.RefreshActiveView()

# 删除 MXD 对象
del mxd