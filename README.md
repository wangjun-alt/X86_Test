#  X86软件测试平台测试端设计文档

[toc]

## 1 开发环境

### 1.1 硬件平台

- Linux系统开发+Linux测试
- Linux系统发布

### 1.2 开发语言和开发平台

- Python  Python-3.7
- Linux系统(推荐CentOS)
- Pycharm-2021.1.1

### 1.3 开源库

- sys——系统的信息和接口使用
- time——获取系统时间
- tkinter ——测试系统可视化界面
  
- psutil——多系统下硬件信息获取
- requests——与服务端数据交互
- os——提供通用的、基本的操作系统交互功能

### 1.4 版本控制工具

- 使用Git作为版本控制工具
- 使用第三方git版本控制服务商gitee

## 2 测试数据

### 2.1 前测数据


| 数据名称         | 数据说明                | 数据类型 |
| ---------------- | ----------------------- | -------- |
| audio            | 音频接口测试            | 字符串   |
| cid              | 电脑id编号              | 字符串   |
| cpuTop           | CPU温度                 | 字符串   |
| cpuconf          | cpu型号                 | 字符串   |
| cpufanspeed      | cpu风扇转速             | 字符串   |
| cpunumber        | cpu数量                 | 字符串   |
| date             | 日期                    | 字符串   |
| diskcap          | 内存容量                | 字符串   |
| diskconf         | 磁盘                    | 字符串   |
| disknumber       | 磁盘数量                | 字符串   |
| disktrackcheck   | 磁盘坏道检查            | 字符串   |
| gpuconf          | gpu型号                 | 字符串   |
| mac              | mac                     | 字符串   |
| memnumber        | 内存数量                | 字符串   |
| netcheck         | 网口数据测试            | 字符串   |
| operatorid       | 操作员id                | 字符串   |
| routinggateway   | 网关                    | 字符串   |
| routingipaddr    | ip地址                  | 字符串   |
| routingipnetmask | 子网掩码                | 字符串   |
| routingnicname   | 主机名                  | 字符串   |
| rtc              | rtc测试结果             | 字符串   |
| serialcheck      | 串口测试                | 字符串   |
| acount           | 加电次数                | 整数     |
| diskid           | 硬盘序列序列号          | 字符串   |
| multiZonee       | 多区域错误率            | 字符串   |
| reade            | 错误读取率              | 字符串   |
| retry            | 磁盘校准重试次数        | 整数     |
| rsector          | 重新分配扇区数          | 整数     |
| spinUpcount      | 硬盘启动重试次数        | 整数     |
| ultraDma         | ULTRA DMA奇偶校验错误率 | 字符串   |
| memHz            | 内存条频率              | 字符串   |
| memId            | 内存序列号              | 字符串   |
| memInterface     | 接口型号                | 字符串   |
| memconf          | 内存型号                | 字符串   |




### 2.2 压力测试（后测数据）
| 数据名称        | 数据说明                    | 数据类型 |
| --------------- | --------------------------- | -------- |
| diskstresscheck | 磁盘压力检测                | 字符串   |
| memstresscheck  | 内存压力测试                | 字符串   |
| cpuTemperature  | cpu温度（6小时高强运行后）  | 字符串   |
| cpuSpeed        | 风扇转速（6小时高强运行后） | 字符串   |



## 3 界面功能预览

### 3.1 测试首页



![image-20220418135347717](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20220418135347717.png)

![image-20220418135410292](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20220418135410292.png)

### 3.2 前测测试中

![image-20220418135459794](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20220418135459794.png)

### 3.3 前测结束，返回测试结果

![image-20220418135725439](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20220418135725439.png)

### 3.4 前测完毕，开始压力测试

![image-20220418135805057](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20220418135805057.png)

### 3.5 压力测试结果

![image-20220418135914581](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20220418135914581.png)

### 3.6 删除脚本文件

![image-20220418140043720](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20220418140043720.png)
