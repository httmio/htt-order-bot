from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
isCreateOrder = False
line_bot_api = LineBotApi('0o5l0pRHo2gX+SpR7BJ4f65rQc6ryImkYZY1Dr0WuWP6uZvGb+Djww4NrBRCd5LOi0/b2LJY+8D6UY5lirRqZZY2I2fqJ0dE/MBCI3a4S9qCptHt8GSS2VZntY4mPFc6/RxviTlG0nwzRcnQn/z2XwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d01e5f80a2981984188e24ee5591587f')
order_list = dict()

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print('-----------------'+event.reply_token+'----------------------------')
    print('-----------------'+event.message.text+'---------------------------')
    print('-----------------'+event.source.user_id+'---------------------------')
    
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
        shop = event.message.text.split()
        if shop[0] == '開團' :
            img = shopMeum(shop[1])
            isCreateOrder = True
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=img,preview_image_url=img)) 
    elif event.message.text.find('訂') != -1:
        order = event.message.text.split(" ",1)
        #利用dict KEY值為id 
        order_list[profile.display_name] = order[1]
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='order_list'))
         #飲料名稱 order[0]
         
         #甜度order[1]
         
         #冰量order[2]
         
         #姓名order[3]
    elif event.message.text == '指令':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="目前可以執行指令\n抽籤、吃什麼、抽早安圖、雷姆"))
    else:
        pass
if __name__ == "__main__":
  #  app.run()
    app.run()

    