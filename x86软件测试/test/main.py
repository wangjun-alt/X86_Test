#coding=utf-8
from __future__ import print_function
import psutil
from collections import OrderedDict
import time
import requests
import sys
from test2 import *
import tkinter
# 首先导入tk
import tkinter as tk

# 定义窗口
window = tk.Tk()

window.title('测试系统')

window.geometry('600x400')

def event():
    """按钮事件,获取文本信息"""
    a = entry.get()
    B = entry1.get()
    print(B)
    print(a)
    window.destroy()
# 定义一个文本框
label1 = tk.Label(window, text="测试员id", font=('Arial', 12))
label1.pack()
entry1 = tk.Entry(window)
# 对文本框内容进行打包
entry1.pack()

label2 = tk.Label(window, text="产品批次", font=('Arial', 12))
label2.pack()
entry = tk.Entry(window)
# 对文本框内容进行打包
entry.pack()

# 定义按钮
b1 = tk.Button(window, text='开始测试',  command=event)
# 打包按钮
b1.pack()

# str = t.get()
# print(str)
window.mainloop()

root2 = tk.Tk()
root2.title("测试结果")
root2.geometry('600x400')
data = {
    "audioCheck": True,
    "cid": "176`",
    "cpuConf": "12",
    "cpuFanSpeed": "6",
    "cpuNumber": 1123,
    "diskConf": "123",
    "diskNumber": 123,
    "diskSmartCheck": True,
    "diskStressCheck": True,
    "diskTrackCheck": True,
    "gpuConf": "qwe",
    "macCheck": True,
    "memConf": "",
    "memStressCheck": True,
    "netCheck": True,
    "rtc": "",
    "serialCheck": True,
    "usbCheck": True
    }
var2 = tk.StringVar()
var2.set(())
lab_1 = tk.Listbox(root2, listvariable=data)
lab_1.grid(row=0, column=0, sticky="w"+"e")
# # 定义按钮
# b2 = tk.Button(root2, text='开始测试',  command=event)
# # 打包按钮
# b2.pack()
root2.mainloop()

# def main():
#     localtime = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
#     print(localtime)
#     type = 'Core'
#     dict_cpu_temp = {}
#     if hasattr(psutil, "sensors_temperatures"):
#         temps = psutil.sensors_temperatures()
#     else:
#         temps = {}
#     cpu_each = []
#     names = list(temps.keys())
#     for name in names:
#         if name in temps:
#             for entry in temps[name]:
#                 if type in entry.label:
#                     dict_cpu_temp[entry.label] = entry.current
#                     cpu_each.append(dict_cpu_temp[entry.label])
#     cpu_top = sorted(dict_cpu_temp.items(), key=lambda d: d[0])[0][1]
#     print({"cpu_top": cpu_top, "cpu_each": cpu_each})
#
#     display_format = '%-30s %-20s'
#     print(display_format % ("Routing Gateway(网关):", routingGateway))
#     print(display_format % ("Routing NIC Name(主机名):", routingNicName))
#     print(display_format % ("Routing NIC MAC Address(MAC地址):", routingNicMacAddr))
#     print(display_format % ("Routing IP Address(IP地址):", routingIPAddr))
#     print(display_format % ("Routing IP Netmask(子网掩码):", routingIPNetmask))
#     print(os.system('lspci |grep VGA'))
#     print(os.system('fdisk -l'))
#
#     CpuCount = psutil.cpu_count()  # CPU数量
#
#     data = {
#         "audioCheck": True,
#         "cid": "176`",
#         "cpuConf": "12",
#         "cpuFanSpeed": "6",
#         "cpuNumber": 1123,
#         "diskConf": "123",
#         "diskNumber": 123,
#         "diskSmartCheck": True,
#         "diskStressCheck": True,
#         "diskTrackCheck": True,
#         "gpuConf": "qwe",
#         "macCheck": True,
#         "memConf": "",
#         "memStressCheck": True,
#         "netCheck": True,
#         "rtc": "",
#         "serialCheck": True,
#         "usbCheck": True
#     }
#     if CpuCount:
#         data["cpuNumber"] = CpuCount
#     else:
#         data["cpuNumber"] = "获取失败"
#     if cpu_top:
#         data["cpuConf"] = cpu_top
#     else:
#         data["cpuConf"] = "获取失败"
#     if CpuCount:
#         data["cpuNumber"] = CpuCount
#     else:
#         data["rtc"] = "获取失败"
#
#     if localtime:
#         data["rtc"] = localtime
#     else:
#         data["rtc"] = "获取失败"
#
#     if routingNicMacAddr:
#         data["macCheck"] = True
#     else:
#         data["macCheck"] = False
#     operator_id = '123'
#     r = requests.post(url='http://192.168.3.193:8080/pre/sava/' + operator_id, json=data)
#     print(r.text)
#
# if __name__ == '__main__':
#     main()
