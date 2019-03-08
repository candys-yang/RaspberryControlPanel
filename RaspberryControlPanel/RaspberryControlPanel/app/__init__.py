# coding=utf-8
"""
Package for the application.
"""

''' -------------------------------------
定义服务线程，用于监控系统动态
'''
import time;
import threading , requests , json ,os
import configparser
import app
import datetime,psutil

def HardwareInfo_get():
    ''' 生成硬件信息 '''
    text = '"hw":{'
    cpu = os.popen('lscpu').read()
    cpus = cpu.find("Model name:") + 12
    text = text + '"cpu":"' + cpu[cpus:cpu.find('\n',cpus)].strip() + '",'  
    cpus = cpu.find("CPU max MHz") + 12
    text = text + '"cpu_b":"' + cpu[cpus:cpu.find('\n',cpus)].strip() + '",' 
    cpu = os.popen('cat /proc/cpuinfo').read()
    cpus = cpu.find("Hardware") + 8
    text = text + '"cpu_h":"' + cpu[cpus:cpu.find('\n',cpus)].strip(':').strip() + '",'
    #-----mem----------
    mem = os.popen("cat /proc/meminfo").read()
    mems = mem.find("MemTotal:") + 9
    text = text + '"mem_t":"' + mem[mems:mem.find('\n',mems)].strip() + '",'
    mems = mem.find("MemFree:") + 8
    text = text + '"mem_f":"' + mem[mems:mem.find('\n',mems)].strip() + '",'
    #----- Hd---------
    text = text + HardwareInfo_get_hd()


    text = text + '}'
    return text
    pass

def HardwareInfo_get_hd():
    #返回磁盘状态：json
    #r = os.popen('C:\\Users\\candy\\source\\repos\\ConsoleApp1\\ConsoleApp1\\bin\\Debug\\ConsoleApp1.exe').read()
    r = os.popen('lsblk -l').read()
    s = str(r).find('\n')
    oneline = r[:s]
    #---------------首行字段位置定位，用于下面行的数据定位
    oneline_list = []
    oneline_list.append(r.find("MAJ:MIN"))
    oneline_list.append(r.find("RM"))
    oneline_list.append(r.find("SIZE"))
    oneline_list.append(r.find("RO"))
    oneline_list.append(r.find("TYPE"))
    oneline_list.append(r.find('MOUNTPOINT'))
    line = []
    i = 0
    while i <= int(len(r)):
        s = str(r).find('\n',i)
        i = s+2    
        linetxt = str(r[i-2:r.find('\n',i)]).lstrip() 
        line.append(linetxt)
        pass 
    devname = [] 
    dev_main = [] 
    dev_son = [] 
    devrm = []
    devsize = []
    devro = []
    devtype = []
    devmoun = []
    for ls in line:
        if len(ls) > 1:
            devname.append(str(ls[:oneline_list[0]]).strip())
            dev_main.append(str(ls[oneline_list[0]: ls.find(":",oneline_list[0])]  ))
            dev_son.append(str(ls[ls.find(":",oneline_list[0])+1:oneline_list[1]]).strip())
            devrm.append(str(ls[oneline_list[1]:oneline_list[2]-1]).strip())
            devsize.append(str( ls[ oneline_list[2] -1 : oneline_list[3] ] ).strip())
            devro.append(str( ls[ oneline_list[3] : oneline_list[4] ] ).strip() )
            dt = str( ls[ oneline_list[4]: oneline_list[5] ] ).strip()
            devtype.append( dt )
            if dt == 'disk':
                devmoun.append("")
            else:
                devmoun.append( str( ls[ oneline_list[5]: ] ).strip() )
        pass
    relist = []
    relist.append(devname)
    relist.append(dev_main)
    relist.append(dev_son)
    relist.append(devrm)
    relist.append(devsize)
    relist.append(devro)
    relist.append(devtype)
    relist.append(devmoun)
    #------------ 取主设备号
    allmainid=sorted(set(dev_main),key=dev_main.index)  #取设备号
    retext = '"hd":{'
    for ami in allmainid:
        #主设备号的循环
        ami_son = [i for i,a in enumerate(dev_main) if a==str(ami)]   #返回当前主设备号的子设备索引
        so_txt = ''
        for so in ami_son:
            #循环子设备，组织数据
            if str(dev_son[so]) == "0":
                #组织主设备
                so_txt = '"'+ str(devname[so]) +'":{\n'
                pass
            else:
                so_txt = so_txt + '"' + devname[so] +'":{"rm":"' + devrm[so] + '","size":"' + devsize[so] + '","ro":"' + devro[so] + '",'
                so_txt = so_txt + '"type":"' + devtype[so] + '","moun":"' + devmoun[so] + '"},'
                pass
            pass
        pass
        so_txt = so_txt[:len(so_txt) -1]
        so_txt = so_txt + "},"
        retext = retext + so_txt

    if len(retext) <= 7:
        retext = retext + ' '
        pass
    retext = retext[:len(retext) - 1] + '}'
    return retext
    pass

def GPIO_get():
    ''' 生成GPIO信息 '''
    ''' 作者暂未涉及到需要调式gpio接口的硬件开发，这里只预留函数在这里  '''
    pass
def ServiceInfo_get():
    ''' 生成进程信息 '''
    config = configparser.ConfigParser()
    config.readfp(open(os.path.curdir + '/app/mypy.ini'))
    text =  '"ps":['
    for pnum in psutil.pids():
        time.sleep(0.01)
        try:
            p = psutil.Process(pnum)
            not_name = config.get("mypy","property_process_name")
            if str(p.name()) in not_name :
                #print ( str(pnum) + ' | ' + str(p.name()) )
                text = text + '{' + '"i":' + str(pnum)+ ',"n":"' + p.name() 
                text = text + '","s":"'+ p.status() + '","mem":"'+ str(p.memory_percent()) 
                text = text + '","cpu_s":"'+ str(p.cpu_times().system) +'","cpu_u":"'+ str(p.cpu_times().user) +'"},'
        except:
            pass
    text = text[:len(text)-1]
    text = text + '],'
    return text
    pass
def BaseHardWareInfo_get():
    ''' 生成性能信息 '''
    retext = ' "bhw":[{ '
    retext = retext + BassProperty_get()
    retext = retext + '}],'
    return retext
    pass

#---------------复制于 app.views-----------------------
#   程序是基于 Windows 下的 visualstudio 2017 开发的
#   但是，部署到 树莓派后，发现无法调用 app.views 的方法。

def BassProperty_get():
    ''' 获取主要硬件利用率 '''
    re = ' "cpu":"' + str(psutil.cpu_percent(percpu=True)) + '","ram":"' 
    re = re + str(psutil.virtual_memory().percent) + '","hd":"' + str(psutil.disk_usage('/').percent) + '","netio":"' 
    re = re + str(psutil.net_io_counters().bytes_sent // 1024) + ',' + str(psutil.net_io_counters().bytes_recv // 1024) + '","netint":"'
    re = re + str(home_netint_json()) + '"'
    return re
    pass
def home_netint_json():
    '''获取网络接口'''
    netcard_info = []
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if item[0] == 2 and not item[1] == '127.0.0.1':
                netcard_info.append((k, item[1]))
    htmltxt = ""
    for x in netcard_info:
        htmltxt = htmltxt + "<br/> " + x[0] + ":" + x[1];

    return htmltxt
#-----------------------------------------------

def heartbeat_main():
    config = configparser.ConfigParser()
    #线程主循环
    while True:
        print(datetime.datetime.now())
        config.readfp(open(os.path.curdir + '/app/mypy.ini'))
        jsonstr = config.get("mypy","jsonstr")
        hoststr = config.get("mypy","tohost")
        looptime = config.get("mypy","looptime")

        #json化-----------------------------------
        jsonstr = '{ "base":' + jsonstr + ' ,'
        #加入进程信息
        if config.get("mypy","property") == "on":
            jsonstr = jsonstr + ServiceInfo_get()
            jsonstr = jsonstr + BaseHardWareInfo_get()
            pass
        #加入硬件信息         hardwareinfo 
        if config.get("mypy","hardwareinfo") == "on":
            jsonstr = jsonstr + HardwareInfo_get()
            pass


        #--------------------------------------#
        jsonstr = jsonstr + '}'

        #传送基础uart
        if config.get("mypy","meg_to_uart") == "on":
            os.system("ifconfig > /dev/ttyS0")

        # Post 数据到远程服务器
        try:
            r = requests.post(hoststr,json = json.loads(jsonstr))
            print("sent data start: 200")
        except :
            print("sent data start: fail")

            pass

        # 写入基础数据到数据库
        try:
            #app.views.BaseProperty_add()
            #print("database update!")
            pass
        except:
            print("数据已发送，但数据库写入异常！")

        # 阻塞线程，阻塞时间由mypy.ini的配置项决定
        time.sleep(int(looptime))
        pass

    pass



t= threading.Thread(target=heartbeat_main)#创建线程,args=(111,112)
t.setDaemon(True)#设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
print(t.setName("heartbeat"))

t.start()#开启线程
print("线程名：" + str(t.getName()))
print(t.name)


'''--------------------------------------'''

import RaspberryControlPanel.settings;
print (RaspberryControlPanel.settings.BASE_DIR)