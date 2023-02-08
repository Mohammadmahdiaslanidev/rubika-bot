import math
from api_rubika import Bot
import datetime
from requests import get,post
from json import loads
math 
bot=Bot("فقطauth")
list_message_seened = []
time_reset = round(datetime.datetime.today().timestamp()) + 350
guid_of_channel = ""
caption = ""
while(2 > 1):
    try:
        chats_list:list = bot.get_updates_all_chats()
        if chats_list != []:
            for chat in chats_list:
                access = chat['access']
                admins = open('admins.txt','r').read().split('\n')
                m_id = chat['object_guid'] + chat['last_message']['message_id']
                if not m_id in list_message_seened and chat['object_guid'] in admins:
                    msg_data = bot.getMessagesInfo(chat['object_guid'],[chat['last_message']['message_id']])[0]
                    text:str = chat['last_message']['text']
                    if text == "شروع" :
                        bot.sendMessage(chat['object_guid'],'ایدی کانال مورد نظر را وارد کنید')
                    elif text.startswith("@"):
                        id = text.split("@")[1]
                        guid_of_channel = bot.getInfoByUsername(id)['data']['channel']['channel_guid']
                        bot.sendMessage(chat['object_guid'],'کپشن را وارد کنید')
                    elif text.startswith("cp ["):
                        caption = id = text.split("[")[1][:-1]
                        bot.sendMessage(chat['object_guid'],'فرمت فایل را وارد کنید')
                    elif text.startswith("-"):
                        new_name = f" {text}"
                        bot.sendMessage(chat['object_guid'],'پست مورد نظر را فوروارد کنید')
                    elif chat['abs_object']['type'] == 'User' and 'SendMessages' in access and (msg_data['type'] == 'FileInline' or msg_data['type'] == 'FileInlineCaption'):
                        bot.sendMessage(chat['object_guid'],'آپلود شروع شد')
                        start_time = datetime.datetime.now().timestamp()
                        fileID = msg_data['file_inline']['file_id']
                        accessHashRec = msg_data['file_inline']['access_hash_rec']
                        dc_id = msg_data['file_inline']['dc_id']
                        size = msg_data['file_inline']['size']
                        
                        
                        file_upload_data = bot.requestFile(new_name,size,msg_data['file_inline']['mime'])
                        header = {
                            'auth':bot.auth,
                            'file-id':str(fileID),
                            'access-hash-rec':accessHashRec
                        }
                        server = "https://messenger"+str(dc_id)+".iranlms.ir/GetFile.ashx"
                        if size <= 131072:
                            header["start-index"], header["last-index"] = "0",str(size)
                            while True:
                                try:
                                    part_data = get(url=server,headers=header).content
                                    h = {
                                        'auth':bot.auth,
                                        'chunk-size':str(len(part_data)),
                                        'file-id':str(file_upload_data['id']),
                                        'access-hash-send':file_upload_data['access_hash_send'],
                                        'total-part':str(1),
                                        'part-number':str(1)
                                    }
                                    j = post(data=part_data,url=file_upload_data['upload_url'],headers=h).text
                                    j = loads(j)['data']['access_hash_rec']
                                    break
                                except Exception as e:
                                    print (e)
                                    continue
                        else:
                            a = 1
                            is_tweny_five = False
                            is_fifty = False
                            is_seventy_five = False
                            for i in range(0,size,131072):
                                while True:
                                    try:
                                        header["start-index"], header["last-index"] =str(i) if i == 0 else str(i+1), str(i+131072 if i+131072 <= size else size)
                                        part_data = get(url=server,headers=header).content
                                        total = size / 131072
                                        total += 1
                                        total = math.floor(total)
                                        h = {
                                            'auth':bot.auth,
                                            'chunk-size':str(len(part_data)),
                                            'file-id':str(file_upload_data['id']),
                                            'access-hash-send':file_upload_data['access_hash_send'],
                                            'total-part':str(total),
                                            'part-number':str(a)
                                        }
                                        a +=1

                                        j = post(data=part_data,url=file_upload_data['upload_url'],headers=h).text
                                        if loads(j)['data'] != None and 'access_hash_rec' in loads(j)['data']:
                                            j = loads(j)['data']['access_hash_rec']                                        
                                        tweny_five = round(total / 4)
                                        fifty = round(total / 2 )
                                        seventy_five = round(total * .75)
                                        if a > tweny_five and is_tweny_five == False:
                                            bot.sendMessage(chat['object_guid'],'25 درصد کار انجام شده')
                                            is_tweny_five = True
                                        elif a > fifty and is_fifty == False:
                                            bot.sendMessage(chat['object_guid'],'50 درصد کار انجام شده')
                                            is_fifty = True
                                        elif a > seventy_five and is_seventy_five == False:
                                            bot.sendMessage(chat['object_guid'],'75 درصد کار انجام شده')
                                            is_seventy_five = True
                                        break
                                    except Exception as e:
                                        continue
                        if j != None and type(j) == str:
                            bot.sendFile(guid_of_channel,file_upload_data['id'],msg_data['file_inline']['mime'],file_upload_data['dc_id'],j,new_name,size,text=caption)
                            bot.sendMessage(chat['object_guid'],'آپلود موفقیت آمیز بود \nزمان : '+ str(datetime.datetime.now().timestamp() - start_time) + ' (s)')
                        else:
                            bot.sendMessage(chat['object_guid'],'آپلود نشد')
                    list_message_seened.append(m_id)
    except Exception as e:
        print(e)
    time_reset2 = round(datetime.datetime.today().timestamp())
    if list_message_seened != [] and time_reset2 > time_reset:
        list_message_seened = []
        time_reset = round(datetime.datetime.today().timestamp()) + 350