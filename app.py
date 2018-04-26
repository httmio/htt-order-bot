from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import json
import requests
import random
from linebot.models import *


def shopMeum(shop):
    if shop == '50嵐' and '五十嵐':
        return 'https://i.imgur.com/vmFauOD.png'
    elif shop == '水巷茶弄':
        return 'https://i.imgur.com/6sNomMJ.png'
    elif shop == '茶湯會':
        return 'https://i.imgur.com/AKahSbx.jpg'
    else:
        return shop

app = Flask(__name__)
line_bot_api = LineBotApi('0o5l0pRHo2gX+SpR7BJ4f65rQc6ryImkYZY1Dr0WuWP6uZvGb+Djww4NrBRCd5LOi0/b2LJY+8D6UY5lirRqZZY2I2fqJ0dE/MBCI3a4S9qCptHt8GSS2VZntY4mPFc6/RxviTlG0nwzRcnQn/z2XwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d01e5f80a2981984188e24ee5591587f')
order_list = dict()
group = ""
@app.route('/')
def index():
    return "<p>Hello World!</p>"
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print("-----------------------------\n"+body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    group = event.source.groupId
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='輸入 開團 店名 (例如: 開團 50嵐) 進行開團 \n 訂購者請依照下面格式來訂購 訂 品名 甜度 冰塊 姓名 (例如:訂 紅茶 半糖 少冰 Paul)，如需修改請依照原本格式重新訂購，如需刪除請輸入刪除，如須查詢請輸入查詢'))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('-----------------'+event.reply_token+'----------------------------')
    print('-----------------'+event.message.text+'---------------------------')
    print('-----------------'+event.source.user_id+'---------------------------')
    isCreateOrder = False
    if  hasattr(event.source, 'user_id') == True and hasattr(event.source, 'group_id') == True:
        profile = line_bot_api.get_group_member_profile(event.source.group_id,event.source.user_id)
        print('-----------------'+profile.display_name+'---------------------------')
    elif  hasattr(event.source, 'user_id') == True:
          profile = line_bot_api.get_profile(event.source.user_id)
          print('-----------------'+profile.display_name+'---------------------------')
    if  event.message.text == '雷姆':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='雷姆是一位有著水藍色頭髮、水藍色瞳孔的少女，有著與雙胞胎姊姊拉姆相似的外型，右眼以瀏海掩蓋，只露出左眼，與姐姐拉姆相反；胸部則比拉姆大一點'))
    elif event.message.text.find('開團') != -1:
        if isCreateOrder == False:
            shop = event.message.text.split()
            if shop[0] == '開團' :
                img = shopMeum(shop[1])
                isCreateOrder = True
                line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=img,preview_image_url=img)) 
        else:line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已開團'))
    elif event.message.text.find('訂') != -1:
        if isCreateOrder == True:
            check =  event.message.text.split()
            if len(check) == 5 :
                #飲料名稱 check[1]

                #甜度check[2] 全半少微無
                if check[2].find('糖') == -1:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入甜度"))
                    break
                #冰量check[3]
                if check[3].find('冰') == -1 and check[3].find('熱') == -1 and check[3].find('溫') == -1 :
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請輸入冰量"))
                    break
                #姓名check[4]
            else :    
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="訂購失敗"))
                break
            order = event.message.text.split(" ",1)
            #利用dict KEY值為id
            order_list[event.source.user_id] = order[1]
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(order_list)))
        else : 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="尚未開團"))
    elif event.message.text == '刪除' :
        if isCreateOrder ==True :
            if event.source.user_id in order_list:
                del order_list[event.source.user_id]
            else :
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="你尚未訂購"))
    elif event.message.text == '查詢' :
        if order_list.has_key(event.source.user_id) == True :
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=order_list.get(event.source.user_id)))
        else :           
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="查無訂購資料"))
    elif event.message.text == '結單' :
        isCreateOrder == False
        order_list.clear()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='結單'))

    elif event.message.text == '指令':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="目前可以執行指令\n開團 訂、刪除、查詢、結單"))
    else:
        pass
if __name__ == "__main__":
  #  app.run()
    app.run()

    