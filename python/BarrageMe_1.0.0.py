# -*- coding: utf-8 -*-

'''
Developed by 三生烟火(Chinese) or ss_Yanhuo(Engilsh).
An easy and light barrage program.
Just link to Apache and Mysql
Then have FUN!!!
'''

#导入模块~

import sys, datetime, pymysql, time, colorlog, threading, multiprocessing
from multiprocessing import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

#读取和呈现

def qSleep(t):
    dieTime = QTime.currentTime()
    dieTime.addMSecs(t)
    while QTime.currentTime() < dieTime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


def getPos():
    global vPos
    vPos += 60
    if vPos >= 800:
        vPos = 40
    return vPos


def readBarrage():
    #检测并获取弹幕
    global num
    global db
    global cursor
    cursor.execute("SELECT * FROM BARRAGE limit " + str(num) + "," + str(num+1))
    rs = cursor.fetchone()
    if rs == None:
        showInfo("No More Barrages, Try to Get Some.")
        cursor.close()
        db.close()
        db = pymysql.Connect(host="127.0.0.1",user="root",password="",db="barrage",port=3306)
        cursor = db.cursor()
        time.sleep(1)
        return
    print(rs)
    num = num + 1
    return rs

def showInfo(s):
    #控制台输出一条INFO级别的LOG
    t = time.strftime('%H:%M:%S',time.localtime(time.time()))
    print('\033[0;32m[INFO]\033[0m'+ '[' + t + ']' + s)
    return

def showErr(s):
    #控制台输出一条ERROR级别的LOG
    t = time.strftime('%H:%M:%S',time.localtime(time.time()))
    print('\033[0;31m[ERROR]\033[0m'+ '[' + t + ']' + s)
    return

def showFatal(s):
    #控制台输出一条FATAL级别的LOG
    t = time.strftime('%H:%M:%S',time.localtime(time.time()))
    print('\033[0;35m[FATAL]\033[0m'+ '[' + t + ']' + s)
    return

def div():
    #分隔线
    print()
    print("+--------------------------------------------+")
    print()

class fetchBarrages(QThread):
    showBarragesig = pyqtSignal(tuple)
    def __int__(self):
        super(fetchBarrages , self).__init__()
    def run(self):
        global cursor      
        while 1:
            time.sleep(0.5)
            barrage = readBarrage()
            if barrage == None:
                continue
            if barrage[3] == 'Stop()':
                app.quit()
            #c = Communicate()
            #c.showBarrage.connect(barrageUI.showBarrage(barrage[3],barrage[4]))
            self.showBarragesig.emit((barrage[3],barrage[4]))
            #barrageUI.showBarrage(barrage[3],barrage[4])
  
class UI(QWidget):
    def __init__(self):
        super().__init__()
        global backend
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        qbtn = QPushButton('Pause', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)  
        #backend = fetchBarrages()
        showInfo("UI init succeed!")
        #self.fetch()
        #timer = QTimer()
        #timer.timeout.connect(self.fetch)
        #timer.start(500)
        self.setGeometry(0, 0, 1920, 1080)
        backend.showBarragesig.connect(self.showBarrage)
        self.show()
        qbtn.setVisible(False)      

    def showBarrage(self, barrage):
        global UI
        global barrageLabel
        global nowPos
        #print(barrage)
        nowPos = getPos()
        barrageLabel = QLabel(barrageUI)
        barrageLabel.setText(barrage[0])
        barrageLabel.move(1920 , nowPos)
        barrageLabel.setStyleSheet("font: bold 20pt '微软雅黑'")
        barragePalette = QPalette()
        barragePalette.setColor(QPalette.WindowText,QColor(barrage[1]))
        barrageLabel.setPalette(barragePalette)
        barrageAnim = QPropertyAnimation(barrageLabel,b"pos")
        barrageAnim.setDuration(10000)
        barrageAnim.setStartValue(QPoint(1920, nowPos))
        barrageAnim.setEndValue(QPoint(0-barrageLabel.width()-300, nowPos))
        barrageLabel.show()
        barrageAnim.start()
        dieTime = QTime.currentTime().addSecs(10)
        while QTime.currentTime() < dieTime:
            QCoreApplication.processEvents(QEventLoop.AllEvents, 1)


#Here we go~

div()
print("BarrageMe Beta Verson 1.0.0")
print("Developed by 三生烟火 or ssYanhuo")
div()
showInfo("Connecting to Database...")
#连接数据库

try:
    db = pymysql.Connect(host="127.0.0.1",user="root",password="",db="barrage",port=3306)
    cursor = db.cursor()
except:
    showFatal("Connect to Database Failed.Exiting...")
    input()
    exit()
else:
    showInfo("Connect to database Succeed.")
    showInfo("Host:127.0.0.1")
    div()


input("Press Enter to Start")
div()

showInfo("Starting fetch Barrages...")
div()




#初始化UI
global num
num = 0
vPos = 0
barrageLabel = 0


backend = fetchBarrages()
app = QApplication(sys.argv)
barrageUI = UI()

backend.start()
#qbtn.setVisible(False)

app.exec()



#关闭连接
div()
showInfo("Connection Closed.")
cursor.close()
db.close()
div()
#exit()
