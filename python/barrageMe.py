# -*- coding: utf-8 -*-

'''
Developed by 三生烟火(Chinese) or ss_Yanhuo(Engilsh).
An easy and light barrage program.
Just link to Apache and Mysql
Then have FUN!!!
'''

#导入模块~

import sys, datetime, pymysql, time, colorlog
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
    global db
    global cursor
    global num
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

def initUI():#不再使用
    #尝试使用Qtime进行延时操作
    #w.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    #w.setAttribute(Qt.WA_TransparentForMouseEvents)
    #w.setAttribute(Qt.WA_TranslucentBackground)
    qbtn = QPushButton('Quit', w)
    qbtn.clicked.connect(QCoreApplication.instance().quit)
    qbtn.resize(qbtn.sizeHint())
    qbtn.move(50, 50)  
    w.setGeometry(0, 0, 1920, 1080)
    w.show()
    showInfo("UI init succeed!")
    

class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        qbtn = QPushButton('Pause', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)  
        showInfo("UI init succeed!")
        #self.fetch()
        #timer = QTimer()
        #timer.timeout.connect(self.fetch)
        #timer.start(500)
        qbtn.clicked.connect(self.fetch)
        self.setGeometry(0, 0, 1920, 1080)
        self.show()
        #qbtn.setVisible(False)


        
    def fetch(self):
        barrage = readBarrage()
        if barrage == None:
            return
        if barrage[3] == 'Stop()':
            app.quit()
        self.showBarrage(barrage[3],barrage[4])
        global barrageLabel
        

    def showBarrage(nothing, bText, bColor):
        global UI
        global barrageLabel
        global nowPos
        print(nothing,bText,bColor)
        nowPos = getPos()
        barrageLabel = QLabel(barrageUI)
        barrageLabel.setText(bText)
        barrageLabel.move(1920,nowPos)
        barrageLabel.setStyleSheet("font: bold 20pt '微软雅黑'")
        barragePalette = QPalette()
        barragePalette.setColor(QPalette.WindowText,QColor(bColor))
        barrageLabel.setPalette(barragePalette)
        barrageAnim = QPropertyAnimation(barrageLabel,b"pos")
        barrageAnim.setDuration(10000)
        barrageAnim.setStartValue(QPoint(1920, nowPos))
        barrageAnim.setEndValue(QPoint(0-barrageLabel.width()-100, nowPos))
        barrageLabel.show()
        barrageAnim.start()
        #qSleep(10000)
        dieTime = QTime.currentTime().addSecs(10)
        #print(str(dieTime))
        #dieTime.addSecs(10)
        #print(dieTime)
        while QTime.currentTime() < dieTime:
            QCoreApplication.processEvents(QEventLoop.AllEvents, 1)


#Here we go~

div()
print("BarrageMe Beta Verson 0.0.5")
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
'''app = QApplication(sys.argv)
w = QWidget()
initUI()
app.exec_()'''
global num
num = 0
vPos = 0
barrageLabel = 0
app = QApplication(sys.argv)
barrageUI = UI()
app.exec_()



'''while 1:
    barrage = readBarrage()
    if barrage == None:
        time.sleep(0.5)
        continue
    if barrage[3] == 'Stop()':
        if input("Stop Command Founded, Do You Want to Stop Fetching?(Y/N)") == 'Y':
            break
        else:
            continue
    time.sleep(0.5)'''
    

#关闭连接
div()
showInfo("Connection Closed.")
cursor.close()
db.close()
div()
#exit()