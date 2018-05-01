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
import model
import requests
import random
from linebot.exceptions import LineBotApiError
from linebot.models import *


app = Flask(__name__)
line_bot_api = LineBotApi('0o5l0pRHo2gX+SpR7BJ4f65rQc6ryImkYZY1Dr0WuWP6uZvGb+Djww4NrBRCd5LOi0/b2LJY+8D6UY5lirRqZZY2I2fqJ0dE/MBCI3a4S9qCptHt8GSS2VZntY4mPFc6/RxviTlG0nwzRcnQn/z2XwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d01e5f80a2981984188e24ee5591587f')
order_list = dict()
global groupId
groupId = ""
global isCreateOrder
isCreateOrder = False
@app.route('/')
def index():
    return "<p>Hello World!</p>"
@app.route("/callback", methods=['POST'])
def callback():
   
    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    if  hasattr(event.source, 'group_id') == True:
        global groupId
        if groupId == "":
            groupId = event.source.group_id
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='輸入 開團 店名 (例如: 開團 50嵐) 進行開團\n訂購者請依照下面格式來訂購\n訂 品名 甜度 冰塊 姓名 (例如:訂 紅茶 半糖 少冰 Paul)，如需修改請依照原本格式重新訂購，如需刪除請輸入刪除，如須查詢請輸入查詢'))
        else:
            line_bot_api.leave_group(event.source.group_id)

   

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global isCreateOrder
    global groupId
    replyToken = event.reply_token
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
        replyToken,
        TextSendMessage(text='雷姆是一位有著水藍色頭髮、水藍色瞳孔的少女，有著與雙胞胎姊姊拉姆相似的外型，右眼以瀏海掩蓋，只露出左眼，與姐姐拉姆相反；胸部則比拉姆大一點'))
        if hasattr(event.source, 'group_id') == True:
            line_bot_api.push_message(event.source.group_id,TextSendMessage(text='雷姆大好!!'))
    elif  hasattr(event.source, 'group_id') == True:
        groupId = event.source.group_id
        if event.message.text.find('開團') != -1:
            if isCreateOrder == False:
                shop = event.message.text.split()
                if len(shop) == 2:
                    if shop[0] == '開團' :
                        img = model.shopMeum(shop[1])
                        isCreateOrder = True
                        line_bot_api.reply_message(replyToken,ImageSendMessage(original_content_url=img,preview_image_url=img))
                        line_bot_api.push_message(groupId,TextSendMessage(text='開團囉! 快來訂飲料'))
            else:
                line_bot_api.reply_message(replyToken,TextSendMessage(text='已開團'))
        elif event.message.text.find('訂') != -1:
            if isCreateOrder == True:
                check = event.message.text.split()
                if len(check) == 5 :
                    #飲料名稱 check[1]
                    #甜度check[2] 全半少微無
                    if check[2].find('糖') == -1:
                        line_bot_api.reply_message(replyToken,TextSendMessage(text="請輸入甜度"))
                    #冰量check[3]
                    elif check[3].find('冰') == -1 and check[3].find('熱') == -1 and check[3].find('溫') == -1 :
                        line_bot_api.reply_message(replyToken,TextSendMessage(text="請輸入冰量"))
                        #姓名check[4]
                    else :   
                        order = event.message.text.split(" ",1)
                        #利用dict KEY值為id
                        order_list[event.source.user_id] = order[1]
                        line_bot_api.reply_message(replyToken,TextSendMessage(text='訂購成功'))
                else :    
                    line_bot_api.reply_message(replyToken,TextSendMessage(text="訂購失敗"))
            
            else : 
                line_bot_api.reply_message(replyToken,TextSendMessage(text="尚未開團"))
        elif event.message.text == '刪除' :
            if isCreateOrder ==True :
                if event.source.user_id in order_list:
                    del order_list[event.source.user_id]
                else :
                    line_bot_api.reply_message(replyToken,TextSendMessage(text="你尚未訂購"))
        elif event.message.text == '查詢' :
            if event.source.user_id in order_list:
                line_bot_api.reply_message(replyToken,TextSendMessage(text=order_list.get(event.source.user_id)))
            else :           
                line_bot_api.reply_message(replyToken,TextSendMessage(text="查無訂購資料"))
        elif event.message.text == '結單' :
            if isCreateOrder == True:
                isCreateOrder = False
                result = order_list.values()
                if len(result)> 0:
                    line_bot_api.reply_message(replyToken,TextSendMessage(text=result))
                    order_list.clear()
                else:
                   line_bot_api.reply_message(replyToken,TextSendMessage(text="無人訂購"))

                try:
                    line_bot_api.leave_group(groupId)
                    groupId = ""
                except LineBotApiError as e:
                    print(e)
            else :     
                line_bot_api.reply_message(replyToken,TextSendMessage(text="尚未開團"))

        elif event.message.text == '指令':
            line_bot_api.reply_message(
            replyToken,
            TextSendMessage(text="目前可以執行指令\n開團 訂、刪除、查詢、結單"))
        else:
            pass
    else:
        line_bot_api.reply_message(
        replyToken,
        TextSendMessage(text="請在群組訂餐"))
if __name__ == "__main__":
  #  app.run()
    app.run()

    