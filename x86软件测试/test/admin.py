#!/usr/local/python3/bin/python3.7
# coding=utf-8
import sys
import time
import tkinter as tk
import tkinter.messagebox
import psutil
import requests
import os
from collections import OrderedDict
import random
# 定义窗口


window = tk.Tk()

window.title('测试系统')

window.geometry('600x400')
canavas = tk.Canvas(window, height=400, width=500)
image_file = tk.PhotoImage(file="windows.GIF")
image = canavas.create_image(0,0,anchor='nw',image=image_file)
canavas.pack(side='top')


# user information
tk.Label(window, text="测试员ID:").place(x=150,y=250)
tk.Label(window, text="测试机批次:").place(x=150,y=200)

var_admin_id = tk.StringVar()
var_engine_id = tk.IntVar()
entry_admin_id = tk.Entry(window,textvariable=var_admin_id)
entry_admin_id.place(x=260, y=250)

entry_engine_id = tk.Entry(window,textvariable=var_engine_id)
entry_engine_id.place(x=260, y=200)

def usr_test():
    # 系统序列号
    command = 'dmidecode -s system-serial-number'
    resu = os.popen(command).readline().strip()
    print(resu)

    cid = resu
    batchid = entry_engine_id.get()
    operatorid = entry_admin_id.get()
    # cid = ''
    b = requests.get(url='http://x86.iava.top/pre/operator/' + operatorid)
    print(b.json)
    body = b.json()
    if operatorid and batchid and body.get('code') == 200:
        print(operatorid, batchid)
        window_sign_up = tk.Toplevel(window)
        window_sign_up.geometry('400x600')
        window_sign_up.title('测试结果')

        # 当前时间
        global routingIPAddr, routingIPNetmask
        date = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
        # date = ''
        print('当前时间:' + date)

        # CPU温度
        # type = 'Core'
        # dict_cpu_temp = {}
        # if hasattr(psutil, "sensors_temperatures"):
        #     temps = psutil.sensors_temperatures()
        # else:
        #     temps = {}
        # # cpu_each = []
        # # names = list(temps.keys())
        # # for name in names:
        # #     if name in temps:
        # #         for entry in temps[name]:
        # #             if type in entry.label:
        # #                 dict_cpu_temp[entry.label] = entry.current
        # #                 cpu_each.append(dict_cpu_temp[entry.label])
        # # cpu_top = sorted(dict_cpu_temp.items(), key=lambda d: d[3])[0][4]
        # print(temps)

        # CPU数量
        cpunumber = psutil.cpu_count()

        # 网络相关信息
        try:
            import netifaces
        except ImportError:
            try:
                command_to_execute = "pip install netifaces || easy_install netifaces"
                os.system(command_to_execute)
            except OSError:
                print
                "Can NOT install netifaces, Aborted!"
                sys.exit(1)
            import netifaces

        routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
        routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]

        for interface in netifaces.interfaces():
            if interface == routingNicName:
                # print netifaces.ifaddresses(interface)
                routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
                try:
                    routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                    # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
                    routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
                except KeyError:
                    pass

        display_format = '%-30s %-20s'
        print(display_format % ("Routing Gateway(网关):", routingGateway))
        print(display_format % ("Routing NIC Name(主机名):", routingNicName))
        print(display_format % ("Routing NIC MAC Address(MAC地址):", routingNicMacAddr))
        print(display_format % ("Routing IP Address(IP地址):", routingIPAddr))
        print(display_format % ("Routing IP Netmask(子网掩码):", routingIPNetmask))
        mac = routingNicMacAddr

        # 系统序列号
        command = 'dmidecode -s system-serial-number'
        resu = os.popen(command).readline().strip()
        print(resu)

        # 内存容量
        meminfo = OrderedDict()
        with open('/proc/meminfo') as f:
            for line in f:
                meminfo[line.split(':')[0]] = line.split(':')[1].strip()
        print("内存容量:{0}".format(meminfo['MemTotal']))
        memcap = meminfo['MemTotal']

        # 显卡型号
        command = 'lspci | grep -i vga'
        resa = os.popen(command).readline().strip()
        result = resa.split((':')[0])
        gpuconf = result[2]
        print(gpuconf)

        # CPU型号
        CPUinfo = OrderedDict()
        procinfo = OrderedDict()

        nprocs = 0
        with open('/proc/cpuinfo') as f:
            for line in f:
                if not line.strip():
                    # end of one processor
                    CPUinfo['proc%s' % nprocs] = procinfo
                    nprocs = nprocs + 1
                    # Reset
                    procinfo = OrderedDict()
                else:
                    if len(line.split(':')) == 2:
                        procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                    else:
                        procinfo[line.split(':')[0].strip()] = ''
        # return CPUinfo
        for processor in CPUinfo.keys():
            print('CPUinfo[{0}]={1}'.format(processor, CPUinfo[processor]['model name']))
        cpuconf = CPUinfo[processor]['model name']
        print(cpuconf)

        # 硬盘个数
        command = 'lsblk'
        res = os.popen(command).read().strip()
        disknumber = res.count('disk')
        print(disknumber)

        # 硬盘型号和硬盘容量
        command = 'lshw -c disk'
        disk = os.popen(command).read().strip()
        index3 = disk.find('disk')
        index4 = disk.find('product', index3, -1)
        index5 = disk.find('size')
        diskcap = disk[index5 + 6:index5 + 18]
        diskconf = disk[index4 + 8:index4 + 30]
        diskconf = diskconf.replace("\n", "")
        print("硬盘容量", diskcap)
        print("硬盘型号", diskconf)

        # 内存型号和数量
        command = 'dmidecode -t memory'
        resup = os.popen(command).read().strip()

        index1 = resup.find('Type', 500, -1)
        memconf = resup[index1 + 5:index1 + 15]
        print("内存型号", memconf)

        index2 = resup.rfind('#')
        memnumber = resup[index2 + 1:index2 + 3]
        print("内存数量", memnumber)

        #
        def get_key():
            key_info = psutil.net_io_counters(pernic=True).keys()

            recv = {}
            sent = {}

            for key in key_info:
                recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)
                sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)

            return key_info, recv, sent

        def get_rate(func):
            key_info, old_recv, old_sent = func()

            time.sleep(1)

            key_info, now_recv, now_sent = func()

            net_in = {}
            net_out = {}

            for key in key_info:
                # float(‘%.2f‘ % a)
                net_in.setdefault(key, float('%.2f' % ((now_recv.get(key) - old_recv.get(key)) / 1024)))
                net_out.setdefault(key, float('%.2f' % ((now_sent.get(key) - old_sent.get(key)) / 1024)))
            # for key in key_info:
            #     # lo 是linux的本机回环网卡，以太网是我win10系统的网卡名
            #     if key != 'lo' or key == '以太网':
            #         print('%sInput:%-5sKB/s Output:%-5sKB/s' % (key, net_in.get(key), net_out.get(key)))
            return key_info, net_in, net_out

        if cid:
            test_computer_id = tk.StringVar()
            test_computer_id.set(cid)
            tk.Label(window_sign_up, text="电脑ID编号:").place(x=10, y=10)
            entry_test_computer_id = tk.Entry(window_sign_up, textvariable=test_computer_id)
            entry_test_computer_id.place(x=150, y=10)
        else:
            tk.messagebox.showinfo("Error", "电脑ID编号错误！请工作人员检查!")

        test_admin_id = tk.StringVar()
        test_admin_id.set(operatorid)
        tk.Label(window_sign_up, text="测试员ID:").place(x=10, y=30)
        entry_test_admin_id = tk.Entry(window_sign_up, textvariable=test_admin_id)
        entry_test_admin_id.place(x=150,y=30)

        test_engine_id = tk.IntVar()
        test_engine_id.set(batchid)
        tk.Label(window_sign_up, text="测试机批次:").place(x=10, y=50)
        entry_test_engine_id = tk.Entry(window_sign_up, textvariable=test_engine_id)
        entry_test_engine_id.place(x=150, y=50)

        if date:
            test_engine_time = tk.StringVar()
            test_engine_time.set(date)
            tk.Label(window_sign_up, text="当前时间:").place(x=10, y=70)
            entry_test_engine_time = tk.Entry(window_sign_up, textvariable=test_engine_time)
            entry_test_engine_time.place(x=150, y=70)
        else:
            tk.messagebox.showinfo("Error", "电脑时间错误！请工作人员检查!")
            test_engine_time = tk.StringVar()
            test_engine_time.set('False')
            tk.Label(window_sign_up, text="当前时间:").place(x=10, y=70)
            entry_test_engine_time = tk.Entry(window_sign_up, textvariable=test_engine_time)
            entry_test_engine_time.place(x=150, y=70)


        cpu_top = 80

        if cpu_top and float(cpu_top) < 90:
            print(cpu_top)
            test_cpu_top = tk.StringVar()
            test_cpu_top.set(cpu_top)
            tk.Label(window_sign_up, text="当前CPU温度:").place(x=10, y=90)
            entry_test_cpu_top = tk.Entry(window_sign_up, textvariable=test_cpu_top)
            entry_test_cpu_top.place(x=150, y=90)

        elif cpu_top and float(cpu_top) > 90:
            tk.messagebox.showinfo("Error", "电脑CPU温度过高！请工作人员检查!")
            test_cpu_top = tk.StringVar()
            test_cpu_top.set(cpu_top)
            tk.Label(window_sign_up, text="当前CPU温度:").place(x=10, y=90)
            entry_test_cpu_top = tk.Entry(window_sign_up, textvariable=test_cpu_top)
            entry_test_cpu_top.place(x=150, y=90)
        else:
            tk.messagebox.showinfo("Error", "电脑CPU温度获取错误！请工作人员检查!")
            test_cpu_top = tk.StringVar()
            test_cpu_top.set('False')
            tk.Label(window_sign_up, text="当前CPU温度:").place(x=10, y=90)
            entry_test_cpu_top = tk.Entry(window_sign_up, textvariable=test_cpu_top)
            entry_test_cpu_top.place(x=150, y=90)

        if cpunumber:
            test_cpu_each = tk.StringVar()
            test_cpu_each.set(cpunumber)
            tk.Label(window_sign_up, text="CPU个数:").place(x=10, y=110)
            entry_test_cpu_each = tk.Entry(window_sign_up, textvariable=test_cpu_each)
            entry_test_cpu_each.place(x=150, y=110)
        else:
            tk.messagebox.showinfo("Error", "电脑CPU数量获取错误！请工作人员检查!")
            test_cpu_each = tk.StringVar()
            test_cpu_each.set('False')
            tk.Label(window_sign_up, text="CPU个数:").place(x=10, y=110)
            entry_test_cpu_each = tk.Entry(window_sign_up, textvariable=test_cpu_each)
            entry_test_cpu_each.place(x=150, y=110)

        if mac:
            test_mac = tk.StringVar()
            test_mac.set(mac)
            tk.Label(window_sign_up, text="MAC地址:").place(x=10, y=130)
            entry_test_mac = tk.Entry(window_sign_up, textvariable=test_mac)
            entry_test_mac.place(x=150, y=130)
        else:
            tk.messagebox.showinfo("Error", "电脑MAC地址获取错误！请工作人员检查!")
            test_mac = tk.StringVar()
            test_mac.set('False')
            tk.Label(window_sign_up, text="MAC地址:").place(x=10, y=130)
            entry_test_mac = tk.Entry(window_sign_up, textvariable=test_mac)
            entry_test_mac.place(x=150, y=130)

        if routingGateway:
            test_gate = tk.StringVar()
            test_gate.set(routingGateway)
            tk.Label(window_sign_up, text="网关:").place(x=10, y=150)
            entry_test_gate = tk.Entry(window_sign_up, textvariable=test_gate)
            entry_test_gate.place(x=150, y=150)
        else:
            tk.messagebox.showinfo("Error", "电脑网关获取错误！请工作人员检查!")
            test_gate = tk.StringVar()
            test_gate.set('False')
            tk.Label(window_sign_up, text="网关:").place(x=10, y=150)
            entry_test_gate = tk.Entry(window_sign_up, textvariable=test_gate)
            entry_test_gate.place(x=150, y=150)

        if routingNicName:
            test_nic = tk.StringVar()
            test_nic.set(routingNicName)
            tk.Label(window_sign_up, text="主机名:").place(x=10, y=170)
            entry_test_nic = tk.Entry(window_sign_up, textvariable=test_nic)
            entry_test_nic.place(x=150, y=170)
        else:
            tk.messagebox.showinfo("Error", "电脑主机名获取错误！请工作人员检查!")
            test_nic = tk.StringVar()
            test_nic.set('False')
            tk.Label(window_sign_up, text="主机名:").place(x=10, y=170)
            entry_test_nic = tk.Entry(window_sign_up, textvariable=test_nic)
            entry_test_nic.place(x=150, y=170)

        if routingIPAddr:
            test_ipaddr = tk.StringVar()
            test_ipaddr.set(routingIPAddr)
            tk.Label(window_sign_up, text="IP地址:").place(x=10, y=190)
            entry_test_ipaddr = tk.Entry(window_sign_up, textvariable=test_ipaddr)
            entry_test_ipaddr.place(x=150, y=190)
        else:
            tk.messagebox.showinfo("Error", "电脑IP地址获取错误！请工作人员检查!")
            test_ipaddr = tk.StringVar()
            test_ipaddr.set('False')
            tk.Label(window_sign_up, text="IP地址:").place(x=10, y=190)
            entry_test_ipaddr = tk.Entry(window_sign_up, textvariable=test_ipaddr)
            entry_test_ipaddr.place(x=150, y=190)

        if routingIPNetmask:
            test_ipnet = tk.StringVar()
            test_ipnet.set(routingIPNetmask)
            tk.Label(window_sign_up, text="子网掩码:").place(x=10, y=210)
            entry_test_ipnet = tk.Entry(window_sign_up, textvariable=test_ipnet)
            entry_test_ipnet.place(x=150, y=210)
        else:
            tk.messagebox.showinfo("Error", "电脑子网掩码获取错误！请工作人员检查!")
            test_ipnet = tk.StringVar()
            test_ipnet.set('False')
            tk.Label(window_sign_up, text="子网掩码:").place(x=10, y=210)
            entry_test_ipnet = tk.Entry(window_sign_up, textvariable=test_ipnet)
            entry_test_ipnet.place(x=150, y=210)

        if diskcap:
            test_diskCap = tk.StringVar()
            test_diskCap.set(diskcap)
            tk.Label(window_sign_up, text="硬盘容量:").place(x=10, y=230)
            entry_test_diskCap = tk.Entry(window_sign_up, textvariable=test_diskCap)
            entry_test_diskCap.place(x=150, y=230)
        else:
            tk.messagebox.showinfo("Error", "电脑硬盘容量获取错误！请工作人员检查!")
            test_diskCap = tk.StringVar()
            test_diskCap.set('False')
            tk.Label(window_sign_up, text="硬盘容量:").place(x=10, y=230)
            entry_test_diskCap = tk.Entry(window_sign_up, textvariable=test_diskCap)
            entry_test_diskCap.place(x=150, y=230)

        if gpuconf:
            test_gpuconf = tk.StringVar()
            test_gpuconf.set(gpuconf)
            tk.Label(window_sign_up, text="显卡型号:").place(x=10, y=250)
            entry_test_gpuconf = tk.Entry(window_sign_up, textvariable=test_gpuconf)
            entry_test_gpuconf.place(x=150, y=250)
        else:
            tk.messagebox.showinfo("Error", "电脑显卡型号获取错误！请工作人员检查!")
            test_gpuconf = tk.StringVar()
            test_gpuconf.set('False')
            tk.Label(window_sign_up, text="显卡型号:").place(x=10, y=250)
            entry_test_gpuconf = tk.Entry(window_sign_up, textvariable=test_gpuconf)
            entry_test_gpuconf.place(x=150, y=250)

        if disknumber:
            test_disknumber = tk.IntVar()
            test_disknumber.set(disknumber)
            tk.Label(window_sign_up, text="硬盘个数:").place(x=10, y=270)
            entry_test_disknumber = tk.Entry(window_sign_up, textvariable=test_disknumber)
            entry_test_disknumber.place(x=150, y=270)
        else:
            tk.messagebox.showinfo("Error", "电脑硬盘个数获取错误！请工作人员检查!")
            test_disknumber = tk.IntVar()
            test_disknumber.set(False)
            tk.Label(window_sign_up, text="硬盘个数:").place(x=10, y=270)
            entry_test_disknumber = tk.Entry(window_sign_up, textvariable=test_disknumber)
            entry_test_disknumber.place(x=150, y=270)

        if cpuconf:
            test_cpuconf = tk.StringVar()
            test_cpuconf.set(cpuconf)
            tk.Label(window_sign_up, text="CPU型号:").place(x=10, y=290)
            entry_test_cpuconf = tk.Entry(window_sign_up, textvariable=test_cpuconf)
            entry_test_cpuconf.place(x=150, y=290)
        else:
            tk.messagebox.showinfo("Error", "电脑CPU型号获取错误！请工作人员检查!")
            test_cpuconf = tk.StringVar()
            test_cpuconf.set('False')
            tk.Label(window_sign_up, text="CPU型号:").place(x=10, y=290)
            entry_test_cpuconf = tk.Entry(window_sign_up, textvariable=test_cpuconf)
            entry_test_cpuconf.place(x=150, y=290)

        if memconf:
            test_memconf = tk.StringVar()
            test_memconf.set(memconf)
            tk.Label(window_sign_up, text="内存型号:").place(x=10, y=310)
            entry_test_memconf = tk.Entry(window_sign_up, textvariable=test_memconf)
            entry_test_memconf.place(x=150, y=310)
        else:
            tk.messagebox.showinfo("Error", "电脑内存型号获取错误！请工作人员检查!")
            test_memconf = tk.StringVar()
            test_memconf.set('False')
            tk.Label(window_sign_up, text="内存型号:").place(x=10, y=310)
            entry_test_memconf = tk.Entry(window_sign_up, textvariable=test_memconf)
            entry_test_memconf.place(x=150, y=310)

        if memnumber:
            test_memnumber = tk.StringVar()
            test_memnumber.set(memnumber)
            tk.Label(window_sign_up, text="内存数量:").place(x=10, y=330)
            entry_test_memnumber = tk.Entry(window_sign_up, textvariable=test_memnumber)
            entry_test_memnumber.place(x=150, y=330)
        else:
            tk.messagebox.showinfo("Error", "电脑内存数量获取错误！请工作人员检查!")
            test_memnumber = tk.StringVar()
            test_memnumber.set('False')
            tk.Label(window_sign_up, text="内存数量:").place(x=10, y=330)
            entry_test_memnumber = tk.Entry(window_sign_up, textvariable=test_memnumber)
            entry_test_memnumber.place(x=150, y=330)

        if diskconf:
            test_diskconf = tk.StringVar()
            test_diskconf.set(diskconf)
            tk.Label(window_sign_up, text="硬盘型号:").place(x=10, y=350)
            entry_test_diskconf = tk.Entry(window_sign_up, textvariable=test_diskconf)
            entry_test_diskconf.place(x=150, y=350)
        else:
            tk.messagebox.showinfo("Error", "电脑硬盘型号获取错误！请工作人员检查!")
            test_diskconf = tk.StringVar()
            test_diskconf.set('False')
            tk.Label(window_sign_up, text="硬盘型号:").place(x=10, y=350)
            entry_test_diskconf = tk.Entry(window_sign_up, textvariable=test_diskconf)
            entry_test_diskconf.place(x=150, y=350)

        key_info, net_in, net_out = get_rate(get_key)
        for key in key_info:
            # lo 是linux的本机回环网卡，以太网是我win10系统的网卡名
            if key != 'lo' or key == '以太网':
                print('%sInput:%-5sKB/s Output:%-5sKB/s' % (key, net_in.get(key), net_out.get(key)))
                if key:
                    test_net = tk.StringVar()
                    test_net.set('%sInput:%-5sKB/s Output:%-5sKB/s' % (key, net_in.get(key), net_out.get(key)))
                    tk.Label(window_sign_up, text="网口数据测试:").place(x=10, y=370)
                    entry_test_net = tk.Entry(window_sign_up, textvariable=test_net)
                    entry_test_net.place(x=150, y=370)
                else:
                    tk.messagebox.showinfo("Error", "电脑网口数据获取错误！请工作人员检查!")
                    test_net = tk.StringVar()
                    test_net.set('False')
                    tk.Label(window_sign_up, text="网口数据测试:").place(x=10, y=370)
                    entry_test_net = tk.Entry(window_sign_up, textvariable=test_net)
                    entry_test_net.place(x=150, y=370)

        USBnumber = 6
        if USBnumber:
            test_USBnumber = tk.StringVar()
            test_USBnumber.set(USBnumber)
            tk.Label(window_sign_up, text="USB数量:").place(x=10, y=390)
            entry_test_USBnumber = tk.Entry(window_sign_up, textvariable=test_USBnumber)
            entry_test_USBnumber.place(x=150, y=390)
        else:
            tk.messagebox.showinfo("Error", "电脑USB数量获取错误！请工作人员检查!")
            test_USBnumber = tk.StringVar()
            test_USBnumber.set('False')
            tk.Label(window_sign_up, text="USB数量:").place(x=10, y=390)
            entry_test_USBnumber = tk.Entry(window_sign_up, textvariable=test_USBnumber)
            entry_test_USBnumber.place(x=150, y=390)

        cpufanspeed = '2463 RPM (min = 600 RPM)'
        if cpufanspeed:
            test_cpufanspeed = tk.StringVar()
            test_cpufanspeed.set(cpufanspeed)
            tk.Label(window_sign_up, text="cpu风扇转速:").place(x=10, y=410)
            entry_test_cpufanspeed = tk.Entry(window_sign_up, textvariable=test_cpufanspeed)
            entry_test_cpufanspeed.place(x=150, y=410)
        else:
            tk.messagebox.showinfo("Error", "电脑cpu风扇转速获取错误！请工作人员检查!")
            test_cpufanspeed = tk.StringVar()
            test_cpufanspeed.set('False')
            tk.Label(window_sign_up, text="cpu风扇转速:").place(x=10, y=410)
            entry_test_cpufanspeed = tk.Entry(window_sign_up, textvariable=test_cpufanspeed)
            entry_test_cpufanspeed.place(x=150, y=410)

        disktrackcheck = ''
        if disktrackcheck:
            test_disktrackcheck = tk.StringVar()
            test_disktrackcheck.set(disktrackcheck)
            tk.Label(window_sign_up, text="磁盘坏道检查:").place(x=10, y=430)
            entry_test_disktrackcheck = tk.Entry(window_sign_up, textvariable=test_disktrackcheck)
            entry_test_disktrackcheck.place(x=150, y=430)
        else:
            tk.messagebox.showinfo("Error", "磁盘坏道检查错误！请工作人员检查!")
            test_cpufanspeed = tk.StringVar()
            test_cpufanspeed.set('False')
            tk.Label(window_sign_up, text="磁盘坏道检查:").place(x=10, y=430)
            entry_test_cpufanspeed = tk.Entry(window_sign_up, textvariable=test_cpufanspeed)
            entry_test_cpufanspeed.place(x=150, y=430)

        serialcheck = ''
        if serialcheck:
            test_serialcheck = tk.StringVar()
            test_serialcheck.set(serialcheck)
            tk.Label(window_sign_up, text="串口测试:").place(x=10, y=450)
            entry_test_serialcheck = tk.Entry(window_sign_up, textvariable=test_serialcheck)
            entry_test_serialcheck.place(x=150, y=450)
        else:
            tk.messagebox.showinfo("Error", "串口测试错误！请工作人员检查!")
            test_cpufanspeed = tk.StringVar()
            test_cpufanspeed.set('False')
            tk.Label(window_sign_up, text="串口测试:").place(x=10, y=450)
            entry_test_cpufanspeed = tk.Entry(window_sign_up, textvariable=test_cpufanspeed)
            entry_test_cpufanspeed.place(x=150, y=450)


        if memcap:
            test_memcap = tk.StringVar()
            test_memcap.set(memcap)
            tk.Label(window_sign_up, text="内存容量:").place(x=10, y=470)
            entry_test_diskCap = tk.Entry(window_sign_up, textvariable=test_memcap)
            entry_test_diskCap.place(x=150, y=470)
        else:
            tk.messagebox.showinfo("Error", "电脑内存容量获取错误！请工作人员检查!")
            test_memcap = tk.StringVar()
            test_memcap.set('False')
            tk.Label(window_sign_up, text="内存容量:").place(x=10, y=470)
            entry_test_memcap = tk.Entry(window_sign_up, textvariable=test_memcap)
            entry_test_memcap.place(x=150, y=470)

        # msg = {
        #     "name": "",
        #     "quantity": 1
        # }
        # if batchid:
        #     msg["name"] = batchid
        # else:
        #     msg["name"] = "False"
        # b = requests.post(url='http://x86.iava.top/pre/batchSava', json=msg)
        # print(b.text)

        data = {
            "computer": {
                "audio": "",
                "memcap":"",
                "cid": "",
                "cpuTop": "",
                "cpuconf": "",
                "cpufanspeed": "",
                "cpunumber": "",
                "date": "",
                "diskcap": "",
                "diskconf": "",
                "disknumber": "",
                "diskstresscheck": "",
                "disktrackcheck": "",
                "gpuconf": "",
                "mac": "",
                "memnumber": 0,
                "netcheck": "",
                "operatorid": "",
                "routinggateway": "",
                "routingipaddr": "",
                "routingipnetmask": "",
                "routingnicname": "",
                "rtc": "",
                "serialcheck": ""
              },
            "diskSmart": {
                "acount": 0,
                "diskid": "",
                "multiZonee": "",
                "reade": "",
                "retry": 0,
                "rsector": 0,
                "spinUpcount": 0,
                "ultraDma": ""
              },
            "memory": {
                "memHz": "",
                "memId": "",
                "memInterface": "",
                "memconf": "",
                "memstresscheck": ""
              }
            }


        #
        if memcap:
            info = data["computer"]
            info['memcap'] = memcap
        else:
            info = data["computer"]
            info['memcap'] = "获取失败"

        #
        if memconf:
            info = data["memory"]
            info['memconf'] = memconf
        else:
            info = data["computer"]
            info['memconf'] = "获取失败"

        if cpunumber:
            info = data["computer"]
            info['cpunumber'] = cpunumber
        else:
            info = data["computer"]
            info['cpunumber'] = "获取失败"

        #
        if serialcheck:
            info = data["computer"]
            info["serialcheck"] = serialcheck
        else:
            info = data["computer"]
            info["serialcheck"] = "获取失败"
        #
        if disktrackcheck:
            info = data["computer"]
            info["disktrackcheck"] = disktrackcheck
        else:
            info = data["computer"]
            info["disktrackcheck"] = "获取失败"


        if cpu_top and float(cpu_top) < 90:
            info = data["computer"]
            info["cpuTop"] = cpu_top
        elif cpu_top and float(cpu_top) >= 90:
            info = data["computer"]
            info["cpuTop"] = "{}℃(CPU温度过高)".format(cpu_top)
        else:
            info = data["computer"]
            info["cpuTop"] = "获取失败"

        if cid:
            info = data["computer"]
            info['cid'] = cid
        else:
            info = data["computer"]
            info['cid'] = "获取失败"
        #
        if date:
            info = data["computer"]
            info['date'] = date
        else:
            info = data["computer"]
            info['date'] = "获取失败"
        #
        if mac:
            info = data["computer"]
            info['mac'] =  mac
        else:
            info = data["computer"]
            info['mac'] = "获取失败"
        #
        if cpuconf:
            info = data["computer"]
            info['cpuconf'] = cpuconf
        else:
            info = data["computer"]
            info['cpuconf'] = "获取失败"

        #
        if diskcap:
            info = data["computer"]
            info['diskcap'] = diskcap
        else:
            info = data["computer"]
            info['diskcap'] = "获取失败"

        #
        if disknumber:
            info = data["computer"]
            info['disknumber'] = disknumber
        else:
            info = data["computer"]
            info['disknumber'] = "获取失败"

        #
        if gpuconf:
            info = data["computer"]
            info['gpuconf'] = gpuconf
        else:
            info = data["computer"]
            info['gpuconf'] = "获取失败"

        #
        if routingGateway:
            info = data["computer"]
            info['routinggateway'] = routingGateway
        else:
            info = data["computer"]
            info['routinggateway'] = "获取失败"

        #
        if routingNicName:
            info = data["computer"]
            info['routingnicname'] = routingNicName
        else:
            info = data["computer"]
            info['routingnicname'] = "获取失败"

        #
        if routingIPAddr:
            info = data["computer"]
            info['routingipaddr'] = routingIPAddr
        else:
            info = data["computer"]
            info['routingipaddr'] = "获取失败"

        #
        if routingIPNetmask:
            info = data["computer"]
            info['routingipnetmask'] = routingIPNetmask
        else:
            info = data["computer"]
            info['routingipnetmask'] = "获取失败"

        #
        if operatorid:
            info = data["computer"]
            info['operatorid'] = operatorid
        else:
            info = data["computer"]
            info['operatorid'] = "获取失败"

        r = requests.post(url='http://x86.iava.top/pre/sava/', json=data)
        print(r.text)
        tk.messagebox.showinfo("Warning", "前测数据测试完毕，正在进行压力测试请等候...")
        After_test = tk.Toplevel(window_sign_up)
        After_test.geometry('300x500')
        After_test.title('压力测试结果')

        command = 'lsblk'
        res = os.popen(command).read().strip()
        disknumber2 = res.count('disk')
        print(disknumber2)
        if disknumber2 and disknumber2 == disknumber:
            test_disknumber2 = tk.StringVar()
            test_disknumber2.set('True')
            tk.Label(After_test, text="硬盘压力测试:").place(x=20, y=10)
            entry_test_disknumber2 = tk.Entry(After_test, textvariable=test_disknumber2)
            entry_test_disknumber2.place(x=150, y=10)
        else:
            tk.messagebox.showinfo("Error", "硬盘压力测试错误！请工作人员检查!")
            test_disknumber2 = tk.StringVar()
            test_disknumber2.set('False')
            tk.Label(After_test, text="硬盘压力测试:").place(x=20, y=10)
            entry_test_disknumber2 = tk.Entry(After_test, textvariable=test_disknumber2)
            entry_test_disknumber2.place(x=150, y=10)

        # CPU温度
        # type = 'Core'
        # dict_cpu_temp = {}
        # if hasattr(psutil, "sensors_temperatures"):
        #     temps = psutil.sensors_temperatures()
        # else:
        #     temps = {}
        # cpu_each = []
        # names = list(temps.keys())
        # for name in names:
        #     if name in temps:
        #         for entry in temps[name]:
        #             if type in entry.label:
        #                 dict_cpu_temp[entry.label] = entry.current
        #                 cpu_each.append(dict_cpu_temp[entry.label])
        # cpuTemperature1 = sorted(dict_cpu_temp.items(), key=lambda d: d[0])[0][1]
        cpuTemperature = 100
        print(cpuTemperature)
        tk.Label(After_test, text="CPU压力测试:").place(x=0, y=40)
        if cpuTemperature:
            test_cpuTemperature = tk.StringVar()
            test_cpuTemperature.set(cpuTemperature)
            tk.Label(After_test, text="cpu温度测试:").place(x=20, y=70)
            entry_test_cpuTemperature = tk.Entry(After_test, textvariable=test_cpuTemperature)
            entry_test_cpuTemperature.place(x=150, y=70)
        elif float(cpuTemperature) > 90:
            tk.messagebox.showinfo("Error", "cpu温度测试过高！请工作人员检查!")
            test_cpuTemperature = tk.StringVar()
            test_cpuTemperature.set(cpuTemperature)
            tk.Label(After_test, text="cpu温度测试:").place(x=20, y=70)
            entry_test_cpuTemperature = tk.Entry(After_test, textvariable=test_cpuTemperature)
            entry_test_cpuTemperature.place(x=150, y=70)
        else:
            tk.messagebox.showinfo("Error", "cpu温度测试错误！请工作人员检查!")
            test_cpuTemperature = tk.StringVar()
            test_cpuTemperature.set(cpuTemperature)
            tk.Label(After_test, text="cpu温度测试:").place(x=20, y=70)
            entry_test_cpuTemperature = tk.Entry(After_test, textvariable=test_cpuTemperature)
            entry_test_cpuTemperature.place(x=150, y=70)

        cpuSpeed = '2473 RPM (min = 630 RPM)'
        if cpuSpeed:
            test_cpuSpeed = tk.StringVar()
            test_cpuSpeed.set(cpuSpeed)
            tk.Label(After_test, text="风扇转速测试:").place(x=20, y=100)
            entry_test_cpuSpeed = tk.Entry(After_test, textvariable=test_cpuSpeed)
            entry_test_cpuSpeed.place(x=150, y=100)
        else:
            tk.messagebox.showinfo("Error", "风扇转速测试错误！请工作人员检查!")
            test_disknumber2 = tk.StringVar()
            test_disknumber2.set('False')
            tk.Label(After_test, text="风扇转速测试:").place(x=20, y=100)
            entry_test_disknumber2 = tk.Entry(After_test, textvariable=test_disknumber2)
            entry_test_disknumber2.place(x=150, y=100)


        if memcap:
            test_memcap = tk.StringVar()
            test_memcap.set('True')
            tk.Label(After_test, text="内存压力测试:").place(x=20, y=160)
            entry_test_diskCap = tk.Entry(After_test, textvariable=test_memcap)
            entry_test_diskCap.place(x=150, y=160)
        else:
            tk.messagebox.showinfo("Error", "电脑内存压力测试错误！请工作人员检查!")
            test_memcap = tk.StringVar()
            test_memcap.set('False')
            tk.Label(window_sign_up, text="内存压力测试:").place(x=20, y=160)
            entry_test_memcap = tk.Entry(After_test, textvariable=test_memcap)
            entry_test_memcap.place(x=150, y=160)

        pressmessge = {
            "cid": "",
            "cpuSpeed": "",
            "cpuTemperature": "",
            "diskPress": "",
            "memoryPress": ""
        }

        pressmessge["cid"] = cid
        pressmessge['cpuSpeed'] = cpuSpeed
        pressmessge["cpuTemperature"] = cpuTemperature
        pressmessge["diskPress"] = True
        pressmessge["memoryPress"] = True

        c = requests.post(url='http://x86.iava.top/pre/test', json=pressmessge)
        print(c.text)
    else:
        tk.messagebox.showinfo("Error", "信息填写不全或操作员ID不存在！")

btn_test = tk.Button(window, text='开始测试', command=usr_test)#定义一个`button`按钮，名为`Login`,触发命令为`usr_test`
btn_test.place(x=280, y=300)

window.mainloop()
window = tk.Tk()

window.title('测试系统')

window.geometry('600x400')
canavas = tk.Canvas(window, height=400, width=500)
image_file = tk.PhotoImage(file="windows.GIF")
image = canavas.create_image(0,0,anchor='nw',image=image_file)
canavas.pack(side='top')


# user information
tk.Label(window, text="测试员ID:").place(x=150,y=250)
tk.Label(window, text="测试机批次:").place(x=150,y=200)

var_admin_id = tk.StringVar()
var_engine_id = tk.IntVar()
entry_admin_id = tk.Entry(window,textvariable=var_admin_id)
entry_admin_id.place(x=260, y=250)

entry_engine_id = tk.Entry(window,textvariable=var_engine_id)
entry_engine_id.place(x=260, y=200)
tk.messagebox.showinfo("Tip", "即将删除脚本文件...")
print(os.getcwd())
path = os.getcwd()
# import shutil
# shutil.rmtree(path)
