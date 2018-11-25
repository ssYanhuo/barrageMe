#! C:\Users\wangj\AppData\Local\Programs\Python\Python37-32\python.exe
# -*- coding: UTF-8 -*- 
import cgi, cgitb ,os ,pymysql, time, datetime, codecs, sys

#初始化并获取弹幕内容

form = cgi.FieldStorage() 
bText = form.getvalue('btext')
ipAds = os.environ['REMOTE_ADDR']
nowTime = time.time()
dt=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
bColor = form.getvalue('bcolor')

#长度检测

if len(str(bText)) >= 32: 
    print("Content-type:text/html")
    print("")
    #print('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
    print("<body>")
    print("Failed!")
    print('<script charset="utf-8">alert("你输入的内容太长啦(╯‵□′)╯︵┻━┻")</script>')
    print("</body>")
    exit()

#连接数据库

db = pymysql.Connect(host="127.0.0.1",user="root",password="",db="barrage",port=3306)
cursor = db.cursor()

#向数据库中插入一条弹幕

cursor.execute("INSERT INTO barrage (ip,text,time,color) VALUES ('" + ipAds + "','" + bText[0] + "','" + dt + "','" + bColor[0] + "' )")
db.commit()

#print("INSERT INTO barrage (ip,text,time) VALUES ('" + ipAds + "','" + bText + "','" + str(nowTime) + "')")

#关闭连接

cursor.close()
db.close()

#DEBUG

print("Content-type:text/html")
print("")
print("<body>")
print("Success!")
print("弹幕内容:" + bText)
print("IP:" + ipAds)
print("时间:" + dt)
print("颜色:" + bColor)
print("<script>alert('发送成功！')</script>")
print("</body>")