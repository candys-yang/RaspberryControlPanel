<h3>干嘛的？</h3>
<p>这是一个可以让你的树莓派不停向指定服务器发送自身性能信息的软件。</p>
<p>基于django开发，适用于 raspbian 
<p></p>
<p></p>
<h3>使用</h3>
1.将 RaspberryControlPanel 拷贝到树莓派中，你可以直接放在 /root/目录下。</br>
2. CD 到 RaspberryControlPanel 目录下，然后执行命令：nohup python3 manage.py runserver 0.0.0.0:8000</br>
<br/>
如果你想要开机启动，你可以向 /etc/rc.local 里添加命令，使其开机自动运行。</br>
又或者你可以配合 apache 来进行使用，这就是一个Django网站。

<h3>依赖</h3>
certifi==2018.11.29 </br>
chardet==3.0.4</br>
configparser==3.7.3</br>
Django>=2.1.7</br>
idna==2.8</br>
pip==10.0.1</br>
psutil==5.5.1</br>
pytz==2018.9</br>
requests==2.21.0</br>
setuptools==39.0.1</br>
urllib3>=1.24.1</br>
</br>
全新安装的raspbian系统，需要安装 python3 然后安装pip 。</br>
通过 pip 安装 configparser 以及 psutil


