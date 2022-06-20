
#外部的函式庫
from flask import Flask, request, abort
from flask_cors import CORS

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#python內建的函式庫
import tempfile, os
import string
import random

app = Flask(__name__)
CORS(app)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
#line Channel Access Token
line_bot_api = LineBotApi('your channel access token')
#line Channel Secret
handler = WebhookHandler('your channel secret')


#監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)

    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent)
def handle_message(event):
    #print(event.message)
    
    if event.message.type =='text':
        #msg=event.message.text
        msg='目前尚未提供文字回覆功能'
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message) #回複文字訊息

    elif event.message.type=='image':      

        img_name=''.join(random.choice(string.ascii_letters+string.digits)for x in range(4)) #建立隨機名稱
        img_content=line_bot_api.get_message_content(event.message.id) 
        img_name=img_name.upper()+'.png' #建立副檔名       
        print(img_content)
        path='./static/'+img_name
        with open(path,'wb') as fd: #寫入static資料夾-可透過ngrok網址/static/圖片名 看圖
            for chunk in img_content.iter_content():
                fd.write(chunk)

        msg='圖片已上傳'
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message) #回複文字訊息



@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event): #新成員
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
