# -*- coding: utf-8 -*-
#/usr/bin/env python
import xlrd
xlsfile = '/home/clay/test.xlsx'
book = xlrd.open_workbook(xlsfile)

# 获取sheet对象
# 方法1
# sheet_name = book.sheet_names()[0]
# print sheet_name
# sheet1=book.sheet_by_name(sheet_name)  #通过sheet名字来获取，当然如果你知道sheet名字了可以直接指定  
# sheet0=book.sheet_by_index(0)     #通过sheet索引获得sheet对象  

# 获取行数和列数

sheet1 = book.sheet_by_index(0)
# nrows = sheet1.nrows
# nclos = sheet1.ncols

# 打印每列的值
# for clonum in range(sheet1.ncols):
    # print sheet1.col_values(clonum)

# 打印每行的数据
# for rownum in range(sheet1.nrows):
    # print rownum
    # print sheet1.row_values(rownum)

# 打印每行的数据,排除第一行标题行
nrows = sheet1.nrows
for num in range(1,nrows):
    a =  sheet1.row_values(num)
    for i in a:
        print i
        print type(i)