import base64
import datetime
import json
import math
from json import dumps, loads
from random import randint
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from requests import post
import io
from PIL import Image , ImageFont, ImageDraw 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class encryption:
    def __init__(self, auth):
        self.key = bytearray(self.secret(auth), "UTF-8")
        self.iv = bytearray.fromhex('00000000000000000000000000000000')

    def replaceCharAt(self, e, t, i):
        return e[0:t] + i + e[t + len(i):]

    def secret(self, e):
        t = e[0:8]
        i = e[8:16]
        n = e[16:24] + t + e[24:32] + i
        s = 0
        while s < len(n):
            e = n[s]
            if e >= '0' and e <= '9':
                t = chr((ord(e[0]) - ord('0') + 5) % 10 + ord('0'))
                n = self.replaceCharAt(n, s, t)
            else:
                t = chr((ord(e[0]) - ord('a') + 9) % 26 + ord('a'))
                n = self.replaceCharAt(n, s, t)
            s += 1
        return n

    def encrypt(self, text):
        raw = pad(text.encode('UTF-8'), AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        enc = aes.encrypt(raw)
        result = base64.b64encode(enc).decode('UTF-8')
        return result

    def decrypt(self, text):
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        dec = aes.decrypt(base64.urlsafe_b64decode(text.encode('UTF-8')))
        result = unpad(dec, AES.block_size).decode('UTF-8')
        return result

class Bot:
	def __init__(self, auth):
		self.auth = auth
		self.enc = encryption(auth)
		
	def sendMessage(self, chat_id, text, message_id=None):
		if message_id == None:
			t = False
			while t == False:
				try:
					p = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/")
					p = loads(self.enc.decrypt(p.json()["data_enc"]))
					t = True
				except:
					t = False
			return p
		else:
			t = False
			while t == False:
				try:
					p = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/")
					p = loads(self.enc.decrypt(p.json()["data_enc"]))
					t = True
				except:
					t = False
			return p
	
	def deleteMessages(self, chat_id, message_ids):
		return post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"deleteMessages",
			"input":{
				"object_guid":chat_id,
				"message_ids":message_ids,
				"type":"Global"
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c66.iranlms.ir/")

	def requestFile(self, name, size , mime):
		o = ''
		while str(o) != '<Response [200]>':
			o = post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"requestSendFile",
				"input":{
					"file_name":name,
					"size":size,
					"mime":mime
				},
				"client":{
					"app_name":"Main",
					"app_version":"3.2.1",
					"platform":"Web",
					"package":"web.rubika.ir",
					"lang_code":"fa"
				}
			}))},url="https://messengerg2c66.iranlms.ir/")
			try:
				k = loads(self.enc.decrypt(o.json()["data_enc"]))
				if k['status_det'] == 'TOO_REQUESTS':
					return 'many_request'
				elif k['status'] != 'OK' or k['status_det'] != 'OK':
					o = '502'
			except:
				o = '502'
		return k['data']

	def fileUpload(self, bytef ,hash_send ,file_id ,url):		
		if len(bytef) <= 131072:
			h = {
				'auth':self.auth,
				'chunk-size':str(len(bytef)),
				'file-id':str(file_id),
				'access-hash-send':hash_send,
				'total-part':str(1),
				'part-number':str(1)
			}
			t = False
			while t == False:
				try:
					j = post(data=bytef,url=url,headers=h).text
					j = loads(j)['data']['access_hash_rec']
					t = True
				except:
					t = False
			
			return j
		else:
			t = len(bytef) / 131072
			t += 1
			t = math.floor(t)
			for i in range(1,t+1):
				if i != t:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							o = post(data=bytef[k:k + 131072],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(131072),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							o = loads(o)['data']
							t2 = True
						except:
							t2 = False
					j = k + 131072
					j = round(j / 1024)
					j2 = round(len(bytef) / 1024)
					print(str(j) + 'kb / ' + str(j2) + ' kb')                
				else:
					k = i - 1
					k = k * 131072
					t2 = False
					while t2 == False:
						try:
							p = post(data=bytef[k:],url=url,headers={
								'auth':self.auth,
								'chunk-size':str(len(bytef[k:])),
								'file-id':file_id,
								'access-hash-send':hash_send,
								'total-part':str(t),
								'part-number':str(i)
							}).text
							p = loads(p)['data']['access_hash_rec']
							t2 = True
						except:
							t2 = False
					j2 = round(len(bytef) / 1024)
					print(str(j2) + 'kb / ' + str(j2) + ' kb') 
					return p

	def sendFile(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name, size, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"File",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"reply_to_message_id":message_id,
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"File",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p

			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"File",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"File",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc'])) 

	def sendImage(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, thumb_inline , width , height, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"Image",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec,
										'thumb_inline':thumb_inline,
										'width':width,
										'height':height
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))    
			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Image",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'thumb_inline':thumb_inline,
								'width':width,
								'height':height
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc'])) 

	def sendVoice(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name,  size, duration, text=None, message_id=None):
			if text == None:
				if message_id == None:
					t = False
					while t == False:
						try:
							p = loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
								"method":"sendMessage",
								"input":{
									"object_guid":chat_id,
									"rnd":f"{randint(100000,900000)}",
									"file_inline":{
										"dc_id":str(dc_id),
										"file_id":str(file_id),
										"type":"Voice",
										"file_name":file_name,
										"size":size,
										"mime":mime,
										"access_hash_rec":access_hash_rec,
										'time':duration,
									}
								},
								"client":{
									"app_name":"Main",
									"app_version":"3.2.1",
									"platform":"Web",
									"package":"web.rubika.ir",
									"lang_code":"fa"
								}
							}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
							t = True
						except:
							t = False
					return p
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Voice",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'time':duration,
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))    
			else:
				if message_id == None:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Voice",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'time':duration,
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc']))
				else:
					return loads(self.enc.decrypt(loads(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"sendMessage",
						"input":{
							"object_guid":chat_id,
							"rnd":f"{randint(100000,900000)}",
							"text":text,
							"reply_to_message_id":message_id,
							"file_inline":{
								"dc_id":str(dc_id),
								"file_id":str(file_id),
								"type":"Voice",
								"file_name":file_name,
								"size":size,
								"mime":mime,
								"access_hash_rec":access_hash_rec,
								'time':duration,
							}
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c17.iranlms.ir/").text)['data_enc'])) 

	def sendVideo(self, chat_id, file_id , mime , dc_id, access_hash_rec, file_name, size, duration, thumb_inline , width , height, caption=None, message_id=None):
		file_inline = {
			"dc_id": dc_id,
			"file_id": file_id,
			"type":"Video",
			"auto_play":False,
			"file_name": file_name,
			"size": size,
			"mime": mime,
			"access_hash_rec": access_hash_rec,
			"width": width,
			"height": height,
			"thumb_inline": thumb_inline,
			"time":duration
		}
		inData = {	
					"file_inline": file_inline,
					"is_mute":False,
					"object_guid": chat_id,
					"rnd": f"{randint(100000,999999999)}"
				}

		data = {"api_version":"4",
				"auth":self.auth,
				"client": {
						"app_name":"Main",
						"app_version":"2.9.5",
						"lang_code":"fa",
						"package":"ir.resaneh1.iptv",
						"platform":"Android"
					},
				"data_enc":self.enc.encrypt(json.dumps(inData)),
				"method":"sendMessage",
				}
		return loads(self.enc.decrypt(post(json=data,url=Bot._getURL()).json()["data_enc"]))
	
	def block(self, chat_id):
		t = False
		while t == False:
			try:
				p = post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"setBlockUser",
					"input":{
						"action": "Block",
						"user_guid": chat_id
					},
					"client": {
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
				}))},url="https://messengerg2c17.iranlms.ir/")
				p = loads(self.enc.decrypt(p.json()["data_enc"]))
				t = True
			except:
				continue
		return p
	
	def unblock(self, chat_id):
		t = False
		while t == False:
			try:
				p = post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"setBlockUser",
					"input":{
						"action": "Unblock",
						"user_guid": chat_id
					},
					"client": {
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
				}))},url="https://messengerg2c17.iranlms.ir/")
				p = loads(self.enc.decrypt(p.json()["data_enc"]))
				t = True
			except:
				continue
		return p
	
	def getUserInfo(self, chat_id):
		user_info = False
		while user_info == False:
			try:
				p = loads(self.enc.decrypt(post(json={"api_version":"5","auth":self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getUserInfo",
					"input":{
						"user_guid":chat_id
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
				}))},url="https://messengerg2c37.iranlms.ir/").json()["data_enc"]))
				user_info = True
			except:
				continue
		return p

	def getMessages(self, chat_id,min_id):
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesInterval",
			"input":{
				"object_guid":chat_id,
				"middle_message_id":min_id
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data").get("messages")
		
	def getInfoByUsername(self, username):
		t = False
		while t == False:
			try:
				p = post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
						"method":"getObjectByUsername",
						"input":{
							"username":username
						},
						"client":{
							"app_name":"Main",
							"app_version":"3.2.1",
							"platform":"Web",
							"package":"web.rubika.ir",
							"lang_code":"fa"
						}
					}))},url="https://messengerg2c23.iranlms.ir/")
				p = loads(self.enc.decrypt(p.json().get("data_enc")))
				t = True
			except:
				continue
		return p
	def banGroupMember(self, chat_id, user_id):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"banGroupMember",
			"input":{
				"group_guid": chat_id,
				"member_guid": user_id,
				"action":"Set"
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c21.iranlms.ir/")

	def invite(self, chat_id, user_ids):
		return post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"addGroupMembers",
			"input":{
				"group_guid": chat_id,
				"member_guids": user_ids
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c22.iranlms.ir/")
	
	def getGroupAdmins(self, chat_id):
		t = False
		while t == False:
			try:
				p = post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"client":{
						"app_name":"Main",
						"app_version":"2.9.5",
						"lang_code":"fa",
						"package":"ir.resaneh1.iptv",
						"platform":"Android"
					},
					"input":{
						"group_guid":chat_id
					},
					"method":"getGroupAdminMembers"
				}))},url="https://messengerg2c22.iranlms.ir/")
				p = loads(self.enc.decrypt(p.json().get("data_enc")))
				if 'data' in p:
					t = True
			except:
				t = False
		return p

	def getMessagesInfo(self, chat_id, message_ids):
		t = False
		while t == False:
			try:
				p = post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
				"method":"getMessagesByID",
				"input":{
					"object_guid": chat_id,
					"message_ids": message_ids
				},
				"client":{
					"app_name":"Main",
					"app_version":"3.2.1",
					"platform":"Web",
					"package":"web.rubika.ir",
					"lang_code":"fa"
				}
				}))}, url="https://messengerg2c24.iranlms.ir/")
				p = loads(self.enc.decrypt(p.json()["data_enc"])).get("data").get("messages")
				t = True
			except:
				continue
		return p
	def setMembersAccess(self, chat_id, access_list):
		return post(json={
			"api_version": "4",
			"auth": self.auth,
			"client": {
				"app_name": "Main",
				"app_version": "2.9.5",
				"lang_code": "fa",
				"package": "ir.resaneh1.iptv",
				"platform": "Android"
			},
			"data_enc": self.enc.encrypt(dumps({
				"access_list": access_list,
				"group_guid": chat_id
			})),
			"method": "setGroupDefaultAccess"
		}, url="https://messengerg2c24.iranlms.ir/")

	def getGroupInfo(self, chat_id):
		return loads(self.enc.decrypt(post(
			json={
				"api_version":"5",
				"auth": self.auth,
				"data_enc": self.enc.encrypt(dumps({
					"method":"getGroupInfo",
					"input":{
						"group_guid": chat_id,
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
			}))}, url="https://messengerg2c24.iranlms.ir/").json()["data_enc"]))
	
	def get_updates_all_chats(self):
		t = False
		while t == False:
			try:
				time_stamp = str(math.floor(datetime.datetime.now().timestamp()) - 200)
				p = post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
					"method":"getChatsUpdates",
					"input":{
						"state":time_stamp,
					},
					"client":{
						"app_name":"Main",
						"app_version":"3.2.1",
						"platform":"Web",
						"package":"web.rubika.ir",
						"lang_code":"fa"
					}
				}))},url="https://messengerg2c67.iranlms.ir/")
				p = loads(self.enc.decrypt(p.json().get("data_enc"))).get("data").get("chats")
				
				t = True
			except:
				t = False
		return p

	def get_updates_chat(self, chat_id):
		time_stamp = str(math.floor(datetime.datetime.now().timestamp()) - 200)
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMessagesUpdates",
			"input":{
				"object_guid":chat_id,
				"state":time_stamp
			},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data").get("updated_messages")
	
	def my_sticker_set(self):
		time_stamp = str(math.floor(datetime.datetime.now().timestamp()) - 200)
		return loads(self.enc.decrypt(post(json={"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({
			"method":"getMyStickerSets",
			"input":{},
			"client":{
				"app_name":"Main",
				"app_version":"3.2.1",
				"platform":"Web",
				"package":"web.rubika.ir",
				"lang_code":"fa"
			}
		}))},url="https://messengerg2c67.iranlms.ir/").json().get("data_enc"))).get("data")

	def getThumbInline(self,image_bytes:bytes):
		im = Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		if height > width:
			new_height = 40
			new_width  = round(new_height * width / height)
		else:
			new_width  = 40
			new_height = round(new_width * height / width)
		im = im.resize((new_width, new_height), Image.ANTIALIAS)
		changed_image = io.BytesIO()
		im.save(changed_image, format='PNG')
		changed_image = changed_image.getvalue()
		return base64.b64encode(changed_image)

	def getImageSize(self,image_bytes:bytes):
		im = Image.open(io.BytesIO(image_bytes))
		width, height = im.size
		return width , height

	def hex_to_rgb(self,value):
		value = value.lstrip('#')
		lv = len(value)
		return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

	def searchInChannelMembers(self, text, channel_guid):
		try:
			p = loads(self.enc.decrypt(post(json={
				"api_version":"4",
				"auth":self.auth,
				"client":{
					"app_name":"Main",
					"app_version":"2.8.1",
					"platform":"Android",
					"package":"ir.resaneh1.iptv",
					"lang_code":"fa"
				},
				"data_enc":self.enc.encrypt(dumps({
					"channel_guid": channel_guid,
					"search_text": text
				})),
				"method":"getChannelAllMembers"
			},url="https://messengerg2c67.iranlms.ir/").json()["data_enc"]))
			if p['in_chat_members'] != []:
				return p['in_chat_members']
			else:
				return 'no exist'

		except: 
			return 'error'

	def checkJoinChannel(self,member_guid,channel_guid):
		user_data:dict = self.getUserInfo(member_guid)['data']['user']
		del user_data['is_deleted'], user_data['is_verified'], user_data['online_time']
		search_mem = ''
		if 'username' in user_data.keys() and user_data['username'] != '':
			search_mem = user_data['username']
		elif 'last_name' in user_data.keys():
			search_mem = user_data['first_name'] + ' ' + user_data['last_name']
		elif not 'last_name' in user_data.keys() and 'first_name' in user_data.keys():
			search_mem = user_data['first_name']
		else:
			return 'Profile not success'
		
		ppo = False
		while ppo == False:
			response = self.searchInChannelMembers(search_mem, channel_guid)
			if response == 'error':
				continue
			elif response == 'no exist':
				ppo =True
				if not 'username' in user_data.keys():
					return 'need for username'
				else:
					return 'no exist'
			else:
				ppo = True
				ss = [i['member_guid'] for i in response]
				if member_guid in ss:
					return 'is exist'
				elif not member_guid in ss and not 'username' in user_data.keys():
					return 'need for username'
				else:
					return 'no exist'
