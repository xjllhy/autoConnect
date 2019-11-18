import ctypes
import os,time
import sys
import configparser
import ntplib
import win32api

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
ierror=0
try:
    cfg=configparser.ConfigParser()
    cfg.read('cfg.ini')
    pingIp=cfg.get('cfg','pingIp')
    pingNum=int(cfg.get('cfg','pingNum'))
    pingRestart=int(cfg.get('cfg','pingRestart'))
    pingSleep=float(cfg.get('cfg','pingSleep'))
    ntpTimeIP=cfg.get('cfg','ntpTimeIp')
    connectName=cfg.get('cfg','connectName')
    killExplorerNum=int(cfg.get('cfg','killExplorerNum'))
    enableKillExplorer=cfg.get('cfg','enableKillExplorer')
    enableRestart=cfg.get('cfg','enableRestart')
except:
    while ierror<3:
        print('配置文件填写错误')
        ierror+=1
        time.sleep(2)
    sys.exit()

i=0
iT=0

def connect(username):
  name=connectName
  password="1"
  cmd_str="rasdial %s %s %s" %(name,username,password)
  res=os.system(cmd_str)
  if res==0:
    print ("connect successful")
  else:
    print (res)
  time.sleep(5)
def disconnect():
  name="1"
  cmdstr="rasdial %s /disconnect" %name
  os.system(cmdstr)
  time.sleep(5)





def setSystemTime(intput):
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(intput)
    win32api.SetSystemTime(tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, 0)

def get_time( ):
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(ntpTimeIP)
    #print(response.tx_time,type(response.tx_time))
    return response.tx_time

def setSystemTime(intput):  # 设置系统时间
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.gmtime(intput)
    win32api.SetSystemTime(tm_year, tm_mon, tm_wday, tm_mday, tm_hour, tm_min, tm_sec, 0)

connect('1')
while 1:
    if time.time() <= 1553840121:
        nowTime = int(time.mktime(time.strptime('2019-7-1 00:00:00', '%Y-%m-%d %H:%M:%S')))
        setSystemTime(nowTime)
        print('系统时间错误，暂时设定为 2019-7-1 00:00:00')
    
    retu = os.system('ping -n 1 -w 1 %s'%pingIp)
    #print('retu:',retu)
    if retu !=0:
        i+=1
    elif retu==0:
        i=0
        # if iT<2:
        #     try:
        #         setSystemTime(get_time())
        #         iT += 1
        #         #print('time ok')
        #     except:
        #         iT=0
        #         #print('ititit')
    if i>=pingNum:
        connect('1')
    if i>=killExplorerNum and enableKillExplorer=='Y':
        os.system('killExplorer.exe')
        time.sleep(1)
        os.system('KillCmd.exe')
    if i>=pingRestart and enableRestart=='Y':
        os.system('shutdown -r')
    print('###########',retu)
    time.sleep(pingSleep)

