from flask import Flask
app = Flask(__name__)
from flask import Flask, request ,abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage ,LocationSendMessage

import requests
import time
import numpy as np
from bs4 import BeautifulSoup as soup
import pymysql
import urllib.request as req
import random

line_bot_api = LineBotApi('*')
handler = WebhookHandler('*')

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

local=time.localtime(time.time())
str(local.tm_min)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text == '@庫存':
        r = requests.get('http://192.124.20.184/iot/drink.php')
        r.encoding = 'utf-8'
        crawl = soup(r.text, 'lxml')
        names = []
        ow = []
        nw = []
        egg = []
        pos = []
        for i, data in enumerate(crawl.select('#name')):
            names.append(data.text + ' ' )
        for i, data in enumerate(crawl.select('#originalWeight')):
            ow.append(data.text + ' ' )
        for i, data in enumerate(crawl.select('#nowWeight')):
            nw.append(data.text + ' ' )
        nw1=int(nw[0])
        nw2=int(nw[1])
        ow1=int(ow[0])
        ow2=int(ow[1])
        message='庫存:\n'
        if nw1>0 and ow1>0:
            message+='1.'
            message+=names[0]
            number1=(int(nw[0])/int(ow[0]))
            number1*=100
            num1=str(round(number1,2))
            message+='剩下: '
            message+=num1
            message+='%\n'
        
        if nw2> 0 and ow2>0 :
            message+='2.'
            message+=names[1]
            number2=int(nw[1])/int(ow[1])
            number2*=100
            num2=str(round(number2,2))
            message+='剩下: '
            message+=str(num2)
            message+='%\n'
      
        e = requests.get('http://192.124.20.184/iot/egg.php')
        e.encoding = 'utf-8'
        crawl2 = soup(e.text, 'lxml')

        for i, data in enumerate(crawl2.select('#putInTime')):
            egg.append(data.text + ' ' )
        count=0

        egg1=float(egg[0])
        egg2=float(egg[1])
        if egg1>0:
            count+=1
        if egg2>0:
            count+=1
        
        message+='現在有'
        message+=str(count)
        message+='顆雞蛋'    
        
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))

    elif event.message.text=='@更新':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入新增品項'))
    elif event.message.text =='@排行榜':
        message='快來看本月零食王!\n'
        message+='http://192.124.20.184/iot/chart.php'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
    elif event.message.text =='@冰箱門':
        d = requests.get('http://192.124.20.184/iot/door.php')
        d.encoding = 'utf-8'
        crawl3 = soup(d.text, 'lxml')
        door=[]
        for i, data in enumerate(crawl3.select('#isOpen')):
            door.append(data.text + ' ' )
        door1=int(door[0])
        door2=int(door[1])
        if door1==1 or door2==1:
            message='冰箱門目前開啟'
        else:
            message='冰箱門目前關閉'

        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
    elif event.message.text =='@溫度':
        try:
            t = requests.get('http://192.124.20.184/iot/temperature.php')
            t.encoding = 'utf-8'
            crawl4 = soup(t.text, 'lxml')
            temperature=[]
            for i, data in enumerate(crawl4.select('#isHot')):
                temperature.append(data.text + ' ' )
            t1=int(temperature[0])
            if t1==1:
                message = [
                TextSendMessage(text='冰箱溫度異常'),
                StickerSendMessage(package_id=1,sticker_id=3)
                ]
            else:
                message = [
                TextSendMessage(text='冰箱溫度正常'),
                StickerSendMessage(package_id=1,sticker_id=13)
                ]

            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='溫度偵測失敗'))
    elif event.message.text =='@食譜推薦':
        try:
            url = "https://icook.tw/"
            request = req.Request(url, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
            with req.urlopen(request) as response:
                data=response.read().decode("utf-8")
            i = 0
            urls=[]
            root=soup(data, "html.parser")
            titles=root.find_all("a", class_="style-module__homepageRecipeCard___Sbhlz")
            for title in titles:
                if title.get('data-module') == '今日話題食譜':
                    urls.append('https://icook.tw/' + title.get('href'))
            a=random.randrange(1,4)
            contenturl=urls[a-1]
            request = req.Request(contenturl, headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})
            title=[]
            with req.urlopen(request) as response:
                data=response.read().decode("utf-8")
            content=soup(data, "html.parser")
            incontent=content.find_all("p",class_="recipe-step-description-content")
            for i, data in enumerate(content.select('#recipe-name')):
                title.append(data.text)
            ingredient=[]
            for i, data in enumerate(content.select('div.ingredient-name a')):
                ingredient.append(data.text)
            message="食譜推薦:"
            message+=str(title[0])
            message+="食材:"
            message+=str(ingredient)
            for con in incontent:
                message+=str(con.text)
            print(message)
            message=str(message)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='食譜推薦失敗'))        
            
            
    else:
        try:
            
            con=pymysql.connect(host='localhost',user='1073320',password='1073320',db='iot',cursorclass=pymysql.cursors.DictCursor)
            cur=con.cursor()
            cur.execute('select * from drink;')
            r = requests.get('http://192.124.20.184/iot/drink.php')
            r.encoding = 'utf-8'
            crawl = soup(r.text, 'lxml')
            weight = []
            for i, test in enumerate(crawl.select('#nowWeight')):
                weight.append(test.text+' ')
            m=[]
            m=event.message.text
            pos=int(m[0])
            originalweight=str(weight[pos-1])
            pos=str(pos)
            print(pos)
            j=2
            item=''
            while j<len(m):
                item=item+m[j]
                j=j+1
            print(item)
            conbo='UPDATE drink SET originalWeight="'+originalweight+'"WHERE drinkPos='+pos
            final =str(conbo)
            cur.execute(final)
            con.commit()
            conbo='UPDATE drink SET name="'+item+'"WHERE drinkPos ='+pos
            final =str(conbo)
            cur.execute(final)
            con.commit()
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='更新成功'))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='新增失敗'))

if __name__=='__main__':
    app.run()

