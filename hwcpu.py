#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :hwcpu.py
@说明        :
@时间        :2022/07/25 17:46:58
@作者        :shitao.li
@版本        :1.0
'''
'''
 使用脚本：hwcpu.sh抓取的top信息即可
 #!/bin/bash 

trap 'onCtrlC' INT
function onCtrlC () {
    echo 'Ctrl+C is captured'
    exit
}
while true; do
  echo "-------------start------------"
  top -b -n 1 >> hwcpu$1.info
  echo "-------------end sleep--------"
  sleep 3
done

'''

'''
若hw更新commond，则使用如下命令生成新的commond列表，然后复制到hw_cm变量中
 sed 's/^/"&/g' hwcommand.list  > temp
sed 's/$/&"/g' temp  > t1
sed 's/$/&,/g' t1  > hwcommand.list
'''
import os
from cmath import e
from signal import pause
from time import sleep

import commands
import sh
import xlsxwriter as xw

file_name = "hwcpu.info"
excelfile = 'hwcpu.xlsx'

hw_cm = ["lidar_a",
"someipd",
"CameraServiceEx",
"ap2mfr_adaptorE",
"LidarDetectionE",
"FTPExec",
"LidarServiceExe",
"LocalizationExe",
"CPPlanningExec",
"SensorServiceEx",
"CameraDetection"]



os.system("rm -rf hwcpu.xlsx")
sleep(1)
print('---------------------------create excel-----------------------')
workbook = xw.Workbook(excelfile)  # 创建工作簿
worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
worksheet1.activate()  # 激活表
title = ['command', 'avg', 'max', 'min']  # 设置表头
worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
row_index = 2  # 从第二行开始写入数据

#get name
print('--------------------------get command---------------------------')
return_code, output = commands.getstatusoutput("cat " + file_name + "| awk '{print $12}' | grep -v [0-9].[0-9]| grep -v COMMAND"  )
outputs = output.split('\n')
# print(output)
cur_names = list(set(outputs))
while '' in cur_names:
    cur_names.remove('')
cur_names.sort()


def xw_toExcel(name, avg, max, min):  # xlsxwriter库储存数据到excel
    global row_index
    insertData = [name, avg, max, min]
    row = 'A' + str(row_index)
    print(row, insertData)
    worksheet1.write_row(row, insertData)
    row_index += 1

def cal_values(name_outpus):
    for pid_name in name_outpus:
        print(pid_name)
        if pid_name in cur_names:
            cur_names.remove(pid_name)
        average = 0
        max_val = 0
        min_val = 200
        count = 1
        try:
            return_code, output = commands.getstatusoutput("cat " + file_name +"|grep -ie " + pid_name + "| awk '{print $9}'")
            # print('----------'+output)
            # if pid_name == 'CameraServiceEx':
            #     print(output)
            outputs = output.split('\n')
            # print(outputs)
            values = []
            for num in outputs:
                values.append(float(num))
            for value in values:
                # print(value)
                average = value + average
                count = count + 1
                if max_val < value:
                    max_val = value
                if min_val > value:
                    min_val = value
            average = average/count        
            xw_toExcel(pid_name, average, max_val, min_val)
            # print(average, max_val, min_val)
        except Exception as e:
            print(e)
            xw_toExcel(pid_name, 0, 0, 0)
            continue

name_outpus = hw_cm
print(name_outpus)
print('----------------------calu values-------------------------')
cal_values(name_outpus)

print('----------------------write other pid to excel------------')
print(cur_names)
cal_values(cur_names)

workbook.close()  # 关闭表





