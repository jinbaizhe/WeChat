import sqlite3,re
import os,threading
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage, ShortVideoMessage)
import Crawler

conf = WechatConf(
    token='parker',
    appid='wx2fb280445fa5d7d3',
    appsecret='6ef28e9c05653e17ae5a822bfaef110f',
    encrypt_mode='normal',
    encoding_aes_key='nRP1YWs5bhUP0XjsaWLwwlpdzCYKrMEJhGnHQbn0hXN'
)

@csrf_exempt
def WeChat(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    wechat_instance = WechatBasic(conf=conf)
    if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return HttpResponseBadRequest('Verify Failed')
    else:
        if request.method == 'GET':
           response = request.GET.get('echostr', 'error')
        else:
            try:
                wechat_instance.parse_data(request.body)
                message = wechat_instance.get_message()
                if isinstance(message, TextMessage):
                    db_path = 'info.db'
                    keywords=message.content
                    openid=message.source
                    reply_text = ''
                    if not os.path.isfile(db_path):
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        cursor.execute('create table user(openid varchar(30) primary key,account varchar(20),passwd varchar(20),card text,update_time varchar(20),is_valid varchar(10))')
                        cursor.execute('create table grade(account varchar(20) ,course varchar(30),credit varchar(10),gpa varchar(10),score varchar(10))')
                        cursor.execute('create table library(account varchar(20) ,book_name text,borrow_time varchar(20),return_time varchar(20),renew_count varchar(10),situation varchar(10))')
                        cursor.close()
                        conn.commit()
                        conn.close()		    
                    match = re.search(r'绑定\s+(\d+)\s+(.*)',keywords)
                    if match:
                        account=match.group(1)
                        passwd=match.group(2)
                        status=Crawler.verify(account, passwd)
                        if status == True:
                            conn=sqlite3.connect(db_path)
                            cursor=conn.cursor()
                            cursor.execute('select account,passwd from user where openid=?',(openid,))
                            value=cursor.fetchall()
                            if value:
                                cursor.execute('update user set account=?,passwd=? where openid=?',(account,passwd,openid))
                                reply_text ='身份验证通过，数据库大约将在1小时之后更新完成'
                            else:
                                t = threading.Thread(target=Crawler.invoke, args=(openid, account, passwd))
                                t.start()
                                reply_text = '身份验证通过，数据库大约将在1分钟之后更新完成'
                            cursor.close()
                            conn.commit()
                            conn.close()
                        else:
                            reply_text = '身份验证未通过，错误信息：'+str(status)
                    else:
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        cursor.execute('select * from user where openid=?', (openid,))
                        value = cursor.fetchall()
                        if value and (value[0][5]=='True'):
                            account = value[0][1]
                            update_time=value[0][4]
                            if keywords in ['成绩','grade','Grade']:
                                cursor.execute('select course,credit,gpa,score from grade where account=?', (account,))
                                value = cursor.fetchall()
                                for course in value:
                                    reply_text += '  '.join(course)+'\r\n'
                                reply_text +='更新时间：'+update_time
                            elif keywords in ['图书馆','library','Library']:
                                cursor.execute('select book_name,return_time,renew_count,situation from library where account=?', (account,))
                                value = cursor.fetchall()
                                for book in value:
                                    reply_text += '  '.join(book) + '\r\n'
                                reply_text += '更新时间：' + update_time
                            elif keywords in ['一卡通','card','Card']:
                                reply_text = value[0][3]+ '\r\n'
                                reply_text += '更新时间：' + update_time
                            else:
                                reply_text='指令无效'
                        else:
                            reply_text = '账号未绑定或账号信息已过期\r\n回复 绑定 学号 统一身份认证密码（各部分用空格隔开）完成账号绑定'
                        cursor.close()
                        conn.commit()
                        conn.close()
                elif isinstance(message, VoiceMessage):
                    reply_text = 'voice'
                elif isinstance(message, ImageMessage):
                    reply_text = 'image'
                elif isinstance(message, LinkMessage):
                    reply_text = 'link'
                elif isinstance(message, LocationMessage):
                    reply_text = 'location'
                elif isinstance(message, VideoMessage):
                    reply_text = 'video'
                elif isinstance(message, ShortVideoMessage):
                    reply_text = 'shortvideo'
                else:
                    reply_text = 'other'
                response = wechat_instance.response_text(content=reply_text)
            except ParseError:
                return HttpResponseBadRequest('Invalid XML Data')
        return HttpResponse(response, content_type="application/xml")