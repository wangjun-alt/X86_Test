from __future__ import print_function
from collections import OrderedDict
import os
import sys

def meminfo():
    '''return the info of /proc/meminfo
    as a dictionary
    '''
    meminfo = OrderedDict()

    with open('/proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    # return meminfo
    print("内存容量:{0}".format(meminfo['MemTotal']))

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




# def CPUinfo():
#     '''Return the info in /proc/cpuinfo
#     as a dirctionary in the follow format:
#     CPU_info['proc0']={...}
#     CPU_info['proc1']={...}
#     '''
#
#     CPUinfo = OrderedDict()
#     procinfo = OrderedDict()
#
#     nprocs = 0
#     with open('/proc/cpuinfo') as f:
#         for line in f:
#             if not line.strip():
#                 # end of one processor
#                 CPUinfo['proc%s' % nprocs] = procinfo
#                 nprocs = nprocs + 1
#                 # Reset
#                 procinfo = OrderedDict()
#             else:
#                 if len(line.split(':')) == 2:
#                     procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
#                 else:
#                     procinfo[line.split(':')[0].strip()] = ''
#     # return CPUinfo
#     for processor in CPUinfo.keys():
#         print('CPUinfo[{0}]={1}'.format(processor, CPUinfo[processor]['model name']))


# def get_key():
#     key_info = psutil.net_io_counters(pernic=True).keys()
#
#     recv = {}
#     sent = {}
#
#     for key in key_info:
#         recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)
#         sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)
#
#     return key_info, recv, sent
#
#
# def get_rate(func):
#     key_info, old_recv, old_sent = func()
#
#     time.sleep(1)
#
#     key_info, now_recv, now_sent = func()
#
#     net_in = {}
#     net_out = {}
#
#     for key in key_info:
#         # float(‘%.2f‘ % a)
#         net_in.setdefault(key, float('%.2f' % ((now_recv.get(key) - old_recv.get(key)) / 1024)))
#         net_out.setdefault(key, float('%.2f' % ((now_sent.get(key) - old_sent.get(key)) / 1024)))
#     # for key in key_info:
#     #     # lo 是linux的本机回环网卡，以太网是我win10系统的网卡名
#     #     if key != 'lo' or key == '以太网':
#     #         print('%sInput:%-5sKB/s Output:%-5sKB/s' % (key, net_in.get(key), net_out.get(key)))
#
#     return key_info, net_in, net_out


def Routing_info():
    display_format = '%-30s %-20s'
    print(display_format % ("Routing Gateway(网关):", routingGateway))
    print(display_format % ("Routing NIC Name(主机名):", routingNicName))
    print(display_format % ("Routing NIC MAC Address(MAC地址):", routingNicMacAddr))
    print(display_format % ("Routing IP Address(IP地址):", routingIPAddr))
    print(display_format % ("Routing IP Netmask(子网掩码):", routingIPNetmask))
    print(os.system('lspci |grep VGA'))
    print(os.system('fdisk -l'))
    # print(os.system('dmidecode -t memory'))
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
    # if routingNicMacAddr:
    #     data["macCheck"] = True
    # else:
    #     data["macCheck"] = False
    # operator_id = '123'
    # r = requests.post(url='http://192.168.3.193:8080/pre/sava/' + operator_id, json=data)
    # print(r.text)


# def main():
#     print('CPU数量:', CPUcount())
#
#     print('CPU的各个型号分别为:')
#     CPUinfo()
#     printTIME()
#     GetCPUorDiskTemper()
#     meminfo()
#     Routing_info()
    key_info, net_in, net_out = get_rate(get_key)
    for key in key_info:
        # lo 是linux的本机回环网卡，以太网是我win10系统的网卡名
        if key != 'lo' or key == '以太网':
            print('%sInput:%-5sKB/s Output:%-5sKB/s' % (key, net_in.get(key), net_out.get(key)))


# if __name__ == '__main__':
#     main()
#     # data = {'operatorId': '123455'}
#     # r = requests.post(url='http://192.168.3.193:8080/pre/sava/', params=data)
#     # print(r.text)

