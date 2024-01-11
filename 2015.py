#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arcpy

arcpy.env.workspace = 'E:\\城市与区域生态\\大熊猫和竹\\道路对大熊猫栖息地的影响\\道路数据\\road_lzc\\1229'
for i in range(85):
    dis = "{} Meters".format(i * 500 + 500)
    outname = "2015XD_{}".format(i * 500 + 500)
    arcpy.Buffer_analysis("研究区县道15非隧道.shp", "E:\\城市与区域生态\\大熊猫和竹\\道路对大熊猫栖息地的影响\\道路距离分析\\15县道缓冲区1229\\" + outname,
                          dis, "FULL", "ROUND", "ALL")

