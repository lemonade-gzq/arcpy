# encoding:utf-8


import arcpy, os
import sys

reload(sys)
from arcpy.sa import *
import pandas as pd

ws = r"F:\pro\proraster"  # 输入栅格路径
arcpy.env.workspace = ws
arcpy.CheckOutExtension("Spatial")
rasters = arcpy.ListRasters("*")

for raster in rasters:
    try:
        print(raster)
        # rasloc = ws + os.sep + raster
        rasloc = arcpy.gp.Int_sa(raster)
        print(rasloc)
        lstFlds = arcpy.ListFields(rasloc)
        header = ["{0}".format(lstFlds[0].name), "{0}".format(lstFlds[1].name), "{0}".format(lstFlds[2].name)]
        if len(lstFlds) != 0:
            f = open(os.path.join(r"F:\pro\pro5", raster.split('.')[0] + '.csv'), "w")
            f.write(header[0] + "\t" + header[1] + "\t" + header[2] + '\n')  # 写入表头
            with arcpy.da.SearchCursor(rasloc, ["OID", "Value", "Count"]) as cursor:  # 游标访问字段["OID","Value","Count"]
                for row in cursor:
                    f.write("{0}\t{1}\t{2}\n".format(row[0], row[1], row[2]))
            f.close()
            print("hello")
        del row

        data1 = os.path.join(r"F:\pro\pro5", raster.split('.')[0] + '.csv')
        data1 = pd.read_csv(data1, sep="\t")
        print (data1.head())
        df = data1[pd.to_numeric(data1['OID'], errors='coerce').isnull()]
        print (df)
        data1 = data1.sort_values(['Value'], ascending=(False))
        data1['all'] = data1['Value'] * data1['Count']
        hld = data1['all'].sum()
        data1['ljdata'] = data1['all'].cumsum() / hld  # .cumsum()计算累加

        print(data1.head())
        print(hld)


        def ljper(x):
            if x < 0.5:
                x = 4
            elif x > 0.5 and x < 0.75:
                x = 3
            elif x > 0.75 and x < 0.9:
                x = 2
            else:
                x = 1
            return x


        data1['re'] = data1['ljdata'].apply(lambda x: ljper(x))
        data1.to_excel(os.path.join(r"F:\pro\pro5", raster.split('.')[0] + '.xls'))
        # data1=pd.read_excel(r"F:\pro\pro3\rer88.xls")
        a1 = data1["Value"].tolist()
        b1 = data1["re"].tolist()
        c1 = list(zip(a1, b1))
        list1 = []
        for i in c1:
            list1.append(list(i))
        print(list1, "yyyyy")

        outReclass1 = Reclassify(rasloc, "Value",
                                 RemapValue(list1))
        outReclass1.save(os.path.join(r"F:\pro\profinal", raster))
        #
    except:
        print ("error:!!!!!!!", raster)
