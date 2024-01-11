#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arcpy

arcpy.env.workspace = 'E:\\城市与区域生态\\大熊猫和竹\\道路对大熊猫栖息地的影响\\道路数据\\road_lzc\\1229'
for i in range(85):
    dis = "{} Meters".format(i * 500 + 500)
    outname = "2015all_{}".format(i * 500 + 500)
    arcpy.Buffer_analysis("研究区15PCS2_1229.shp", "E:\\城市与区域生态\\大熊猫和竹\\道路对大熊猫栖息地的影响\\道路距离分析\\15缓冲区1229all\\" + outname,
                          dis, "FULL", "ROUND", "ALL")
