import os
import time
import psutil
from threading import Thread

logRoot = "..\\Log"
logName = "Log_"+ time.strftime("%Y%m%d",time.localtime(time.time()))



def printLog(content):
    f = open(logName,'a+')
    f.writelines(content)
    f.close()

if __name__ == '__main__':
    chackFirst("C:\\Users\\5403_50\\PycharmProjects\\USB_bak\\src\\test")