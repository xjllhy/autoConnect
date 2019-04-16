import ctypes
import os,time
import sys
import configparser
import ntplib
import win32api

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

cfg=configparser.ConfigParser()
cfg.read('cfg.ini')
pingIp=cfg.get('cfg','pingIp')
pingNum=int(cfg.get('cfg','pingNum'))
pingRestart=int(cfg.get('cfg','pingRestart'))
pingSleep=float(cfg.get('cfg','pingSleep'))
ntpTimeIP=cfg.get('cfg','ntpTimeIp')
connectName=cfg.get('cfg','connectName')

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

connect('1')
while 1:
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
    elif i>=pingRestart:
        #os.system('shutdown -r')
        pass
    time.sleep(pingSleep)

