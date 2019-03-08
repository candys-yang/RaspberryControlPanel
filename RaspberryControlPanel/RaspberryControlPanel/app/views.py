"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import psutil
import json,sys,django,os,threading
import configparser

from app.models import BaseProperty


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
def home_system_boottime():
    '''获取启动时间'''
    txt = "";
    try:
        txt = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    except :
        txt = "0";
    return txt;
    pass



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    getdate = BaseProperty.objects.all().last()
    return render(
        request,
        'app/index.html',
        {
            'title':'RCP-admin',
            'year':datetime.now().year,
            'redata_baseinfo':datetime.now,
            'cpu': str(psutil.cpu_percent(percpu=True)),
            'ram': str(psutil.virtual_memory().percent) + '%',
            'hd':  str(psutil.disk_usage('/').percent) + '%',
            'netio':str(psutil.net_io_counters().bytes_sent // 1024) + ',' + str(psutil.net_io_counters().bytes_recv // 1024) + "(KB)",
            'netint':str(home_netint_json()),
            'boottime':home_system_boottime,
            'python_ev':sys.version,
            'dj_ev':django.VERSION,
            'pi_info':os.popen('cat /proc/device-tree/model').read(),
         }
    )
def admin(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    config = configparser.ConfigParser()
    config.readfp(open(os.path.curdir + '/app/mypy.ini'))

   

    #request.POST['hoststr']
    if request.method == 'POST':
        if 'property' in request.POST:
            config.set("mypy","property",request.POST['property'])
        else:
            config.set("mypy","property",'off')
        if 'meg_to_uart' in request.POST:
            config.set("mypy","meg_to_uart",request.POST['meg_to_uart'])
        else:
            config.set("mypy","meg_to_uart",'off')
        if 'hardwareinfo' in request.POST:
            config.set("mypy","hardwareinfo",request.POST['hardwareinfo'])
        else:
            config.set("mypy","hardwareinfo",'off')

        config.set("mypy","tohost",request.POST['hoststr'])
        config.set("mypy","jsonstr",request.POST['jsonstr'])
        #config.set("mypy","property",request.POST['property'])
        with open(os.path.curdir + '/app/mypy.ini', 'w') as fw:   #循环写入
            config.write(fw)
        pass

    return render(
        request,
        'app/admin.html',
        {
            'title':'Raspberry Control Panel Administrator Page',
            'message':'Here Manage Raspberry system.',
            'year':datetime.now().year,
            'jsonstr':config.get("mypy","jsonstr"),
            'hoststr':config.get("mypy","tohost"),
            'property':config.get("mypy","property"),
            'meg_to_uart':config.get("mypy","meg_to_uart"),
            'hardwareinfo':config.get("mypy","hardwareinfo")
        }
    )

def BaseProperty_add():
    ''' 向数据库添加当前的数据 '''
    '''这个方法会在定时任务中调用'''
    vals = BaseProperty(
        cpu_data = str(psutil.cpu_percent(percpu=True)),
        ram_data = str(psutil.virtual_memory().percent),
        hd_data = str(psutil.disk_usage('/').percent),
        netio_data = str(psutil.net_io_counters().bytes_sent // 1024) + ',' + str(psutil.net_io_counters().bytes_recv // 1024),
        netint_data = str(home_netint_json())
        )
    vals.save()

def BassProperty_get():
    
    re = ' "cpu":"' + str(psutil.cpu_percent(percpu=True)) + '","ram":"' 
    re = re + str(psutil.virtual_memory().percent) + '","hd":"' + str(psutil.disk_usage('/').percent) + '","netio":"' 
    re = re + str(psutil.net_io_counters().bytes_sent // 1024) + ',' + str(psutil.net_io_counters().bytes_recv // 1024) + '","netint":"'
    re = re + str(home_netint_json()) + '"'
    return re
    pass