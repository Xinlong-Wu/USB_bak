import os
import time
import psutil
from threading import Thread
import pandas as pd

logRoot = "..\\Log"
logName = "Log_"+ time.strftime("%Y%m%d",time.localtime(time.time()))
targetRoot = 'D:\CopyFileRoot'  # 目标目录
oldDiskName = []  # 旧的磁盘列表
number = 0  # 磁盘数，判断是否为第一次运行
bakpath = ""    # u盘验证文件路径
usbData = ""

'''
    初始化函数
'''
def chackFirst():  # 判断是否是第一次运行
    if not os.path.exists(logRoot):  # 判断本地log文件夹是否存在
        os.mkdir(logRoot)
    if not os.path.exists(targetRoot):  # 判断本地备份文件是否存在
        os.mkdir(targetRoot)

'''
    写Log函数
'''
def printLog(content):
    print(time.strftime("%H:%M:%S    ", time.localtime(time.time()))+content)
    # f = open(os.path.join(logRoot,logName),'a+')
    # f.write(time.strftime("%H:%M:%S    ",time.localtime(time.time())))
    # f.write(content+'\n')
    # f.close()

'''
    写USB.bak版本控制文件函数
'''
def csvRider():
    cf = open(bakpath, "a+")
    fieldname = ['name']
    rider = csv.DictReader(cf, fieldname=fieldname)

    cf.close()

def csvWriter(file):
    global usbData
    mtime = time.strftime("%Y%m%d",time.localtime(os.stat(file).st_mtime))
    # data = pd.DataFrame([[str(mtime)]],index=[str(file)])
    exist = usbData.loc[usbData["name"]==str(file)]
    if(exist.size == 0):
        usbData = usbData.append([{"name": str(file),"date":str(mtime)}], ignore_index=True)
    else:
        ti = usbData.loc[usbData["name"]==str(file)]
        if()
    usbData.to_csv(bakpath)
    f = pd.read_csv(bakpath)
    print(f)







'''
从sourcepath复制文件和目录到targetPath
'''


def copyfile(sourcePath, targetPath, threadName):
    for f in os.listdir(sourcePath):
        if (f == 'System Volume Information'):  # 过滤系统文件夹
            continue

        f1 = os.path.join(sourcePath, f)  # 连接源文件（目录）名
        f2 = os.path.join(targetPath, f)  # 连接目标文件（目录）名


        if os.path.isfile(f1):  # 如果为文件，则进行复制操作
            csvWriter(f1)
            if not os.path.exists(f2):
                file1 = open(f1, 'rb')
                file2 = open(f2, 'wb')
                printLog(threadName + '：-%s文件正在复制！' % (f1))
                file2.write(file1.read())
                printLog(threadName + '：-%s文件复制成功！' % (f1))
                file2.close()
                file1.close()
            else:
                printLog(threadName + '：%s文件已存在！' % (f1))
        else:  # 如果为目录，创建新一级的目标目录，并递归操作
            printLog(threadName + '：-%s目录正在复制！' % (f1))
            if not os.path.exists(f2):
                os.mkdir(f2)
                printLog(threadName + '：-%s目标目录创建成功！' % (f1))
            else:
                printLog(threadName + '：%s复制失败，原因：目录已存在！'% (f1))
            copyfile(f1, f2, threadName)
            printLog(threadName + '-%s目录复制成功！' % (f2))

'''
获取磁盘信息，并与上次获取的信息进行比较，判断是否有新的磁盘添加进来
'''


def getDiskMessage():
    global oldDiskName  # 声明全局变量
    global number

    if number == 0:  # 第一次操作，先获取一遍磁盘数据，然后返回
        for disk in psutil.disk_partitions():
            number = number + 1
            oldDiskName.append(disk.device[:2])  # 获取盘符信息
        return

    newDiskName = []  # 保存新获取的磁盘信息
    for disk in psutil.disk_partitions():
        newDiskName.append(disk.device[:2])  # 获取新的磁盘信息

    newDiskList = arrayCompare(oldDiskName, newDiskName)  # 获取新增盘符列表

    oldDiskName.clear()  # 清除旧盘符列表
    oldDiskName = newDiskName[:]  # 复制新盘符列表给旧盘符列表
    return newDiskList


'''
比较两个磁盘盘符列表，并返回新盘符列表中旧盘符列表没有的盘符名列表
'''


def arrayCompare(oldDiskName, newDiskName):
    newDiskList = []
    for name in newDiskName:
        if name not in oldDiskName:  # 旧盘符中没有，则添加这个到新增盘符列表中
            newDiskList.append(name)
    return newDiskList


'''
复制盘符name中的文件到目标目录中
'''


def copy(name, threadName):
        timeNow = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))  # 获取当前时间字串
        targetPath = os.path.join(targetRoot, name[:1])  # 创建一个新目录，使用目标目录+盘符作为名字
        if not os.path.exists(targetPath):
            os.mkdir(targetPath)  # 创建新的目录
        copyfile(name, targetPath, threadName)  # 复制文件
        printLog(threadName + '-新磁盘：%s盘 复制完毕！' % (name[:1]))



if __name__ == '__main__':
    getDiskMessage()  # 获取初始数据
    # targetRoot = chackFirst()  # 软件初始化
    threadCount = 0  # 线程计数
    printLog("开始运行")
    while True:

        newDiskList = getDiskMessage()  # 获取新数据
        if len(newDiskList) > 0:    # 检测到有新u盘插入
            printLog('当前磁盘列表：' + str(oldDiskName))
            printLog('新磁盘列表：' + str(newDiskList))
            time.sleep(10)      # 延迟等待u盘加载
            for name in newDiskList:  # 根据新获取到的数据去复制文件
                bakpath = os.path.join(name, 'USB.bak')
                t = os.path.exists(bakpath)
                if t:  # 没有文件则不是需要备份的u盘
                    usbData = pd.read_csv(bakpath,usecols=["name","date"]).infer_objects()    # 加载U盘数据文件
                    copy(name, 'thread_' + str(threadCount))
                    # thread = Thread(target=copy, args=(name, 'thread_' + str(threadCount),))  # 创建线程去复制指定磁盘
                    # thread.start()  # 开启线程
                    # printLog('thread_' + str(threadCount) + '-开始复制%s盘文件...' % (name[:1]))
                    # threadCount = threadCount + 1  # 线程计数+1
        time.sleep(10)   # 延时10秒进行下一次数据获取