import os, sys
import requests
import time, datetime
import asyncio, aiohttp
import base64, json, jwt


from protobuf import *
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf.timestamp_pb2 import Timestamp
from protobuf_decoder.protobuf_decoder import Parser


class VrxxTools:
	def __init__(self):
		pass
	
	
	def fix_hex(self, hex):
		hex = hex.lower().replace(" ", "")
		
		return hex
	
	
	def dec_to_hex(self, decimal):
		decimal = hex(decimal)
		final_result = str(decimal)[2:]
		if len(final_result) == 1:
			final_result = "0" + final_result
			return final_result
		
		else:
			return final_result
	
	
	def encode_varint(self, number):
		if number < 0:
			raise ValueError("Number must be non-negative")
		
		encoded_bytes = []
		
		while True:
			byte = number & 0x7F
			number >>= 7
		
			if number:
				byte |= 0x80
			encoded_bytes.append(byte)
			
			if not number:
				break
		
		return bytes(encoded_bytes)
	
	
	def create_varint_field(self, field_number, value):
		field_header = (field_number << 3) | 0# Varint wire type is 0
		return self.encode_varint(field_header) + self.encode_varint(value)
	
	
	def create_length_delimited_field(self, field_number, value):
		field_header = (field_number << 3) | 2# Length-delimited wire type is 2
		encoded_value = value.encode() if isinstance(value, str) else value
		return self.encode_varint(field_header) + self.encode_varint(len(encoded_value)) + encoded_value
	
	
	def create_protobuf_packet(self, fields):
		packet = bytearray()
		
		for field, value in fields.items():
			if isinstance(value, dict):
				nested_packet = self.create_protobuf_packet(value)
				packet.extend(self.create_length_delimited_field(field, nested_packet))
			
			elif isinstance(value, int):
				packet.extend(self.create_varint_field(field, value))
			
			elif isinstance(value, str) or isinstance(value, bytes):
				packet.extend(self.create_length_delimited_field(field, value))
		
		return packet
	
	
	def parse_my_message(self, serialized_data):
		# Parse the serialized data into a MyMessage object
		my_message = my_message_pb2.MyMessage()
		my_message.ParseFromString(serialized_data)
		
		# Extract the fields
		timestamp = my_message.field21
		key = my_message.field22
		iv = my_message.field23
		
		# Convert timestamp to a single integer
		timestamp_obj = Timestamp()
		timestamp_obj.FromNanoseconds(timestamp)
		timestamp_seconds = timestamp_obj.seconds
		timestamp_nanos = timestamp_obj.nanos
		
		# Combine seconds and nanoseconds into a single integer
		combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
		
		return combined_timestamp, key, iv
	
	
	def parse_results(self, parsed_results):
		result_dict = {}
		
		for result in parsed_results:
			field_data = {}
			field_data["wire_type"] = result.wire_type
			
			if result.wire_type == "varint":
				field_data["data"] = result.data
			
			if result.wire_type == "string":
				field_data["data"] = result.data
			
			if result.wire_type == "bytes":
				field_data["data"] = result.data
			
			elif result.wire_type == "length_delimited":
				field_data["data"] = self.parse_results(result.data.results)
			
			result_dict[result.field] = field_data
		
		return result_dict
	
	
	def parsed_results_to_dict(self, parsed_results):
		result_dict = {}
		for parsed_result in parsed_results.results:
			if hasattr(parsed_result.data, "results"):
				result_dict[parsed_result.field] = self.parsed_results_to_dict(parsed_result.data)
			
			else:
				result_dict[parsed_result.field] = parsed_result.data
	
		return result_dict
	
	
	def Decrypt_API(self, cipher_text):
		key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
		iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
		cipher = AES.new(key, AES.MODE_CBC, iv)
		plain_text = unpad(cipher.decrypt(bytes.fromhex(cipher_text)), AES.block_size)
		
		return plain_text.hex()
	
	
	def Encrypt_API(self, plain_text):
		plain_text = bytes.fromhex(plain_text)
		key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
		iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
		cipher = AES.new(key, AES.MODE_CBC, iv)
		cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
		
		return cipher_text.hex()
	
	
	def Decrypt_Packet(self, packet, key, iv):
		packet = bytes.fromhex(packet)
		key, iv = key, iv
		cipher = AES.new(key, AES.MODE_CBC, iv)
		plain_text = unpad(cipher.decrypt(packet), AES.block_size)
		
		return plain_text.hex()
	
	
	def Encrypt_Packet(self, plain_text, key, iv):
		plain_text = bytes.fromhex(plain_text)
		key, iv = key, iv
		cipher = AES.new(key, AES.MODE_CBC, iv)
		cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
		
		return cipher_text.hex()
	
	
	def Decrypt_ID(self, encoded_bytes):
		encoded_bytes = bytes.fromhex(encoded_bytes)
		number, shift = 0, 0
		
		for byte in encoded_bytes:
			value = byte & 0x7F
			number |= value << shift
			shift += 7
			
			if not byte & 0x80:
				break
			
		return number
	
	
	def Encrypt_ID(self, number):
		number = int(number)
		encoded_bytes = []
		
		while True:
			byte = number & 0x7F
			number >>= 7
			
			if number:
				byte |= 0x80
			encoded_bytes.append(byte)
			
			if not number:
				break
		
		return bytes(encoded_bytes).hex()
	
	
	def MajorLogin(self, access_token, open_id):
		now = datetime.now()
		formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
		fields = {
			3: formatted_time,
			4: "free fire",
			5: 1,
			7: "1.107.12",
			8: "Android OS 10 / API-29 (QP1A.190711.020/1624873154)",
			9: "Handheld",
			10: "Mobifone",
			11: "WIFI",
			12: 1520,
			13: 720,
			14: "288",
			15: "ARM64 FP ASIMD AES | 1989 | 8",
			16: 2731,
			17: "Mali-G72 MP3",
			18: "OpenGL ES 3.2 v1.r20p0-01rel0.6b65289a6438c2775cb93f5486360d04",
			20: "171.236.225.227",
			21: "vn",
			22: str(open_id),
			23: "4",
			24: "Handheld",
			25: "Realme RMX1821",
			29: str(access_token),
			30: 1,
			41: "Mobifone",
			42: "WIFI",
			57: "7428b253defc164018c604a1ebbfebdf",
			60: 21634,
			61: 4711,
			62: 4510,
			63: 107,
			64: 4943,
			65: 21834,
			66: 4711,
			67: 21634,
			73: 1,
			74: "/data/data/com.chaozhuo.gameassistant/virtual/data/app/com.dts.freefireth/lib",
			76: 1,
			77: "1d9dbbc55aa45dd49f131345ba82532b|/data/app/com.dts.freefireth-VEJ_bWErfYR6zhs_4-lqqA==/base.apk",
			78: 3,
			79: 2,
			81: "64",
			83: "2019117718",
			85: 3,
			86: "OpenGLES2",
			87: 16383,
			88: 4,
			89: {8: 86},
			92: 27788,
			93: "android",
			94: "KqsHTwIi2IPBLYk4nYprQP5he++GFTs44lgh14mbHH+qdFmotCEM1r1LBb9otfKIWje+NESNpQ+jElc83NvMFZNrPSnXYfkJ1aZ5VW+O6N6UStSN",
			97: 1,
			98: 1
		}
		
		payload = self.create_protobuf_packet(fields)
		payload = payload.hex()
		payload = self.Encrypt_API(payload)
		
		headers = {
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Connection": "Close",
			"Accept-Encoding": "gzip",
			"Expect": "100-continue",
			"Authorization": "Bearer",
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		
		encrypt_data = bytes.fromhex(payload)
		
		response = requests.post("https://loginbp.ggblueshark.com/MajorLogin", headers=headers, data=encrypt_data)
		
		return response.content
	
	
	def getGuestAccessToken(self, uid, password):
		headers = {
			"Host": "100067.connect.garena.com",
			"User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
			"Content-Type": "application/x-www-form-urlencoded",
			"Accept-Encoding": "gzip, deflate, br",
			"Connection": "close"
		}
		
		data = {
			"uid": str(uid),
			"password": str(password),
			"response_type": "token",
			"client_type": "2",
			"client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
			"client_id": "100067"
		}
		
		response = requests.post("https://100067.connect.garena.com/oauth/guest/token/grant", headers=headers, data=data)
		data = response.json()
		
		access_token = data.get("access_token")
		open_id = data.get("open_id")
		
		return dict(access_token=access_token, open_id=open_id)
	
	
	def getGuestJWTToken(self, access_token, open_id, full=False):
		now = datetime.now()
		formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
		payload = b'\x1a\x13default_datetime"\tfree fire(\x01:\x071.105.8B<Android OS 7.1.2 / API-25 (QKQ1.190825.002/17.0240.2004.9-0)J\x08HandheldR\x06ROGERSZ\x04WIFI`\x80\x0fh\xb8\x08r\x03240z\x1bARMv7 VFPv3 NEON | 2000 | 4\x80\x01\xd7\x1b\x8a\x01\x0fAdreno (TM) 650\x92\x01\rOpenGL ES 3.0\x9a\x01+Google|573feb1f-7b10-4a9a-b23e-b36c0afcb21e\xa2\x01\x0b41.235.8.32\xaa\x01\x02ar\xb2\x01 default_open_id\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x0fasus ASUS_Z01QD\xea\x01@default_access_token\xf0\x01\x01\xca\x02\x06ROGERS\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xfa\xf6\x03\xe8\x03\xdb\xb6\x03\xf0\x03\xfe=\xf8\x03\xb31\x80\x04\xb8\xd0\x03\x88\x04\xfa\xf6\x03\x90\x04\xb8\xd0\x03\x98\x04\xfa\xf6\x03\xc8\x04\x03\xd2\x04&/data/app/com.dts.freefireth-1/lib/arm\xe0\x04\x01\xea\x04H1d9dbbc55aa45dd49f131345ba82532b|/data/app/com.dts.freefireth-1/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019117511\xa8\x05\x03\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xca\x05%K\x04G\x12Y]\x0e\x02\x18T\x0e@\n\x00\x15]C9\\\x03TR\t{[@P1FRSXAj\rS2\xd2\x05\x05Cairo\xda\x05\x01C\xe0\x05\xe8S\xea\x05\x07android\xf2\x05\\KqsHT9B3lQrSQNIV65y9VklbdFPuLruR0lrNnkhdCGY5blTD1XlaY9MzZA8NH+XPx/elY5jIRIYs8/F4zDpUddd/omU=\xf8\x05\xfb\xe4\x06\x82\x06F{"support_mode_count":1,"current_mode_id":1,"current_refreshrate":240}\x88\x06\x01'
		payload = payload.replace(b"default_datetime", formatted_time.encode())
		payload = payload.replace(b"default_open_id", open_id.encode())
		payload = payload.replace(b"default_access_token", access_token.encode())
		payload = self.Encrypt_API(payload.hex())
		payload = bytes.fromhex(payload)
		
		headers = {
			"Expect": "100-continue",
			"Authorization": "Bearer",
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str( len(payload.hex()) ),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "loginbp.ggblueshark.com",
			"Connection": "Keep-Alive",
			"Accept-Encoding": "gzip"
		}
		
		rsp = requests.post("https://loginbp.ggblueshark.com/MajorLogin", headers=headers, data=payload)
		if rsp.status_code == 200:
			if len(rsp.text) < 10:
				return False
			
			if full:
				return rsp.content
			
			token = rsp.text[rsp.text.find("eyJhbGciOiJIUzI1NiIsInN2ciI6I"):-1]
			second_dot_index = token.find(".", token.find(".") + 1)
			token = token[:second_dot_index + 44]
			
			return token
		
		else:
			return False
	

	def GetPayloadByData(self, jwt_token, new_access_token):
		token_payload_base64 = jwt_token.split(".")[1]
		token_payload_base64 += "=" * ((4 - len(token_payload_base64) % 4) % 4)
		decoded_payload = base64.urlsafe_b64decode(token_payload_base64).decode("utf-8")
		decoded_payload = json.loads(decoded_payload)
		
		new_external_id = decoded_payload["external_id"]
		signature_md5 = decoded_payload["signature_md5"]
		now = datetime.now()
		formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
		
		payload = b'\x1a\x132023-12-24 04:21:34"\tfree fire(\x01:\x081.102.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\rEMS - MobinilZ\x04WIFI`\x80\nh\xc0\x07r\x03320z\x1eARM64 FP ASIMD AES VMH | 0 | 6\x80\x01\xbf.\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.0\x9a\x01+Google|6ec2d681-b32f-4b2d-adc2-63b4c643d683\xa2\x01\x0e156.219.174.33\xaa\x01\x02ar\xb2\x01 4666ecda0003f1809655a7a8698573d0\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x0cgoogle G011A\xea\x01@15f5ba1de5234a2e73cc65b6f34ce4b299db1af616dd1dd8a6f31b147230e5b6\xf0\x01\x01\xca\x02\rEMS - Mobinil\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xe6\xdb\x02\xe8\x03\xff\xbb\x02\xf0\x03\xaf\x13\xf8\x03\xfc\x04\x80\x04\xaf\xca\x02\x88\x04\xe6\xdb\x02\x90\x04\xaf\xca\x02\x98\x04\xe6\xdb\x02\xc8\x04\x03\xd2\x04?/data/app/com.dts.freefireth-2kDmep_84HTIG7I7CUiJxw==/lib/arm64\xe0\x04\x01\xea\x04_df3bb3771c4b2d46f751a3e7d0347ba7|/data/app/com.dts.freefireth-2kDmep_84HTIG7I7CUiJxw==/base.apk\xf0\x04\x03\xf8\x04\x02\x8a\x05\x0264\x9a\x05\n2019116797\xa8\x05\x03\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xca\x05 \x11\\\x10F\x07][\x05\x1e\x00XL\x0fXEZ\x149]R[]\x05b\nZ\t\x05`\x0eU5\xd2\x05\x0eShibin al Kawm\xda\x05\x03MNF\xe0\x05\xa6A\xea\x05\x07android\xf2\x05\\KqsHT+kkoTQE5BlBobUYX1gU2WQkP3UxRmOCvqs5/lkAGJsABcsIABFyS2oXUc9QDamooQF50iepFI53iz6yQPfFRAw=\xf8\x05\xac\x02'
		payload = payload.replace(b"2023-12-24 04:21:34", formatted_time.encode("UTF-8"))
		payload = payload.replace(b"15f5ba1de5234a2e73cc65b6f34ce4b299db1af616dd1dd8a6f31b147230e5b6" , new_access_token.encode("UTF-8"))
		payload = payload.replace(b"4666ecda0003f1809655a7a8698573d0", new_external_id.encode("UTF-8"))
		payload = payload.replace(b"7428b253defc164018c604a1ebbfebdf", signature_md5.encode("UTF-8"))
		payload = payload.hex()
		payload = self.Encrypt_API(payload)
		payload = bytes.fromhex(payload)
		
		return payload
	
	
	def getJWTToken(self, payload, full=False):
		payload = bytes.fromhex(payload)
		
		headers = {
			"Expect": "100-continue",
			"Authorization": "Bearer",
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str(len(payload)),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "loginbp.ggblueshark.com",
			"Connection": "Close",
			"Accept-Encoding": "gzip, deflate, br"
		}
		
		rsp = requests.post("https://loginbp.ggblueshark.com/MajorLogin", headers=headers, data=payload)
		if full:
			return rsp.content
		
		token = rsp.text[rsp.text.find("eyJhbGciOiJIUzI1NiIsInN2ciI6I"):-1]
		second_dot_index = token.find(".", token.find(".") + 1)
		token = token[:second_dot_index + 44]
		
		return token
	
	
	def GenerateAuthorizationPacket(self, jwt_token_full):
		try:
			if isinstance(jwt_token_full, str):
				token_full = self.fix_hex(jwt_token_full)
				token_full = bytes.fromhex(token_full)
			
			else:
				token_full = jwt_token_full
		
			token = token_full.decode(errors="ignore")
			token = token[token.find("eyJhbGciOiJIUzI1NiIsInN2ciI6I"):-1]
			second_dot_index = token.find(".", token.find(".") + 1)
			token = token[:second_dot_index + 44]
			
			decoded = jwt.decode(token, options={"verify_signature": False})
			account_id = decoded.get("account_id")
			
			timestamp, key, iv = self.parse_my_message(token_full)
			
			encoded_acc = hex(int(account_id))[2:]
			hex_value = self.dec_to_hex(timestamp)
			time_hex = hex_value
			
			jwt_token_hex = token.encode().hex()
			jwt_token_enc = self.Encrypt_Packet(jwt_token_hex, key, iv)
			
			packet_header = hex( len(jwt_token_enc) // 2)[2:]
			account_enc_length = len(encoded_acc)
			
			zeros = "00000000"
			if account_enc_length == 9:
				zeros = "0000000"
			elif account_enc_length == 8:
				zeros = "00000000"
			elif account_enc_length == 10:
				zeros = "000000"
			elif account_enc_length == 7:
				zeros = "000000000"
			else:
				return dict()
			
			packet_header = f"0115{zeros}{encoded_acc}{time_hex}00000{packet_header}"
			final_token = packet_header + jwt_token_enc
			
			return dict(jwt_token=token, token_packet=final_token, key=key, iv=iv, account_id=account_id)
		
		except:
			return dict()
	
	
	def GetLoginData(self, jwt_token, payload):
		headers = {
			"Expect": "100-continue",
			"Authorization": f"Bearer {jwt_token}",
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str(len(payload)),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "loginbp.ggblueshark.com",
			"Connection": "Close",
			"Accept-Encoding": "gzip, deflate, br"
		}
		
		max_retries, attempt = 3, 0
		while attempt < max_retries:
			try:
				response = requests.post("https://clientbp.ggblueshark.com/GetLoginData", headers=headers, data=payload)
				response.raise_for_status()
				response = response.content.hex()
				try:
					parsed_results = Parser().parse(response)
					parsed_results_dict = self.parse_results(parsed_results)
					json_result = json.dumps(parsed_results_dict)
				
				except Exception as e:
					# print(f"error {e}")
					return None
				
				parsed_data = json.loads(json_result)
				addressMain = parsed_data["14"]["data"]
				addressChat = parsed_data["32"]["data"]
				
				addressMain = dict(ip=addressMain[:len(addressMain) - 6], port=addressMain[len(addressMain) - 5:])
				addressChat = dict(ip=addressChat[:len(addressChat) - 6], port=addressChat[len(addressChat) - 5:])
				return dict(MainServer=addressMain, ChatServer=addressChat)
			
			except requests.RequestException as e:
				# print(f"Request failed: {e}. Attempt {attempt + 1} of {max_retries}. Retrying...")
				attempt += 1
				# time.sleep(2)
		
		# print("Failed to get login data after multiple attempts.")
		return None
	
	
	def GenMsgPacket(self, account_id, account_name, room_id, room_type, message, key, iv, **kwagrs):
		room_type_dict = {"Guild": 1, "Friend": 2, "World": 5}
		room_type = room_type_dict.get(room_type.title())
		alert_icon = kwagrs.get("alert_icon")
		language = kwagrs.get("language", "vn")
		
		account_avatar = kwagrs.get("account_avatar")
		account_banner = kwagrs.get("account_banner")
		account_rank = kwagrs.get("account_rank")
		account_pin = kwagrs.get("account_pin")
		evo_badge = kwagrs.get("evo_badge")
		
		# 1: Headers (Value: 1)
		# 2:
			# 1: Account UID
			# 2: Room ID
			# 3: Room Type (Maybe | 1: Guild, 2: Friend, 5: World)
			# 4: Message
			# 5: Time Sent Message
			# 7: Message Type (2: Alert Icon, 3: Dict Content)
		
		# 9:
			# 1: Account Name
			# 2: Account Avatar
			# 3: Account Banner
			# 4: Account Rank
			# 5: Account Pin
			# 6: Undefined
			# 7: Unknown
			# 8: Guild Name
			# 9: Undefined
			# 10: E Badge
		
		# 10: Message Language | Server
		# 13:
			# 1: Link Account Avatar
			# 2: IDK (Default: 1)
			# 3: IDK (Default: 1)
		
		# 14: IDK (Default: "")
		fields = {
			1: 1,
			2: {
				1: int(account_id),
				2: int(room_id),
				5: int(time.time()),
				7: 3,
				8: '{"content":"abcxyz","isRequest":false,"isAccepted":true,"reason":0,"time":1000,"matchMode":1,"gameMode":43,"mapID":11,"source":0,"groupId":null,"reservationCode":null}',
				9: {
					1: str(account_name)
				},
				10: language,
				13: {
					2: 1,
					3: 1
				},
				14: ""
			}
		}
		
		if room_type:
			fields[2][3] = room_type
		
		if message:
			fields[2][4] = str(message)
		
		if alert_icon:
			fields[2][7] = 2
		
		if account_avatar:
			fields[2][9][2] = account_avatar
		
		if account_banner:
			fields[2][9][3] = account_banner
		
		if account_rank:
			fields[2][9][4] = account_rank
		
		if account_pin:
			fields[2][9][5] = account_pin
		
		if evo_badge:
			fields[2][9][10] = int(evo_badge) if isinstance(evo_badge, int) else 1
		
		sorted_fields = {}
		for k in sorted(fields.keys()):
			if isinstance(fields[k], dict):
				sorted_subdict = {}
				for subkey in sorted(fields[k].keys()):
					if isinstance(fields[k][subkey], dict):
						sorted_subsubdict = {}
						for subsubkey in sorted(fields[k][subkey].keys()):
							sorted_subsubdict[subsubkey] = fields[k][subkey][subsubkey]
						sorted_subdict[subkey] = sorted_subsubdict
					else:
						sorted_subdict[subkey] = fields[k][subkey]
				sorted_fields[k] = sorted_subdict
			else:
				sorted_fields[k] = fields[k]
		
		
		packet = self.create_protobuf_packet(sorted_fields)
		packet = packet.hex()
		packet_enc = self.Encrypt_Packet(packet, key, iv)
		header_length = int(len(packet_enc) // 2)
		header_length = self.dec_to_hex(header_length)
		
		if len(header_length) == 2:
			header = "1215000000"
		
		elif len(header_length) == 3:
			header = "121500000"
		
		elif len(header_length) == 4:
			header = "12150000"
		
		elif len(header_length) == 5:
			header = "1215000"
		
		final_packet = header + header_length + packet_enc
		
		return bytes.fromhex(final_packet)
	
	
	def GetFriendRequestList(self, token):
		payload = self.Encrypt_API("")
		payload = bytes.fromhex(payload)
		
		headers = {
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Connection": "Close",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str(len(payload)),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "clientbp.ggblueshark.com",
			"Accept-Encoding": "gzip"
		}
		
		response = requests.post("https://clientbp.ggblueshark.com/GetFriendRequestList", headers=headers, data=payload)
		
		return response.content
	
	
	def RequestAddingFriend(self, account_id, player_id, token):
		fields = {
			1: int(account_id),
			2: int(player_id),
			3: 3
		}
		
		payload = self.create_protobuf_packet(fields)
		payload = payload.hex()
		payload = self.Encrypt_API(payload)
		payload = bytes.fromhex(payload)
		
		headers = {
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Connection": "Close",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str(len(payload)),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "clientbp.ggblueshark.com",
			"Accept-Encoding": "gzip"
		}
		
		response = requests.post("https://clientbp.ggblueshark.com/RequestAddingFriend", headers=headers, data=payload)
		
		return response.content
	
	
	def ConfirmFriendRequest(self, account_id, friend_id, token):
		fields = {
			1: int(friend_id),
			2: int(account_id)
		}
		
		payload = self.create_protobuf_packet(fields)
		payload = payload.hex()
		payload = self.Encrypt_API(payload)
		payload = bytes.fromhex(payload)
		
		headers = {
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str(len(payload)),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "clientbp.ggblueshark.com",
			"Accept-Encoding": "gzip"
		}
		
		response = requests.post("https://clientbp.ggblueshark.com/ConfirmFriendRequest", headers=headers, data=payload)
		
		return response.content
	
	
	def LikeProfile(self, uid, region, token):
		fields = {
			1: int(uid),
			2: str(region).upper()
		}
		
		payload = self.create_protobuf_packet(fields)
		payload = payload.hex()
		payload = self.Encrypt_API(payload)
		payload = bytes.fromhex(payload)
		
		headers = {
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str(len(payload)),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "clientbp.ggblueshark.com",
			"Accept-Encoding": "gzip"
		}
		
		response = requests.post("https://clientbp.ggblueshark.com/LikeProfile", headers=headers, data=payload)
		
		return response.content
	
	
	def GetPlayerPersonalShow(self, uid, token):
		fields = {
			1: int(uid),
			2: 7,
			3: 1
		}
		
		payload = self.create_protobuf_packet(fields)
		payload = payload.hex()
		payload = self.Encrypt_API(payload)
		payload = bytes.fromhex(payload)
		
		headers = {
			"User-Agent": "Free%20Fire/2019117061 CFNetwork/1399 Darwin/22.1.0",
			"Connection": "Keep-Alive",
			"Accept": "/",
			"Accept-Encoding": "gzip",
			"Content-Type": "application/x-www-form-urlencoded",
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46"
		}
		
		response = requests.post("https://clientbp.ggblueshark.com/GetPlayerPersonalShow", headers=headers, data=payload)
		
		return response.content
	
	
	def UpdateSocialBasicInfo(self, social_bio, token):
		fields = {
			2: 5,
			5: "",
			6: "",
			8: str(social_bio),
			11: "",
			12: ""
		}
		
		payload = self.create_protobuf_packet(fields)
		payload = payload.hex()
		payload = self.Encrypt_API(payload)
		payload = bytes.fromhex(payload)
		
		headers = {
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str(len(payload)),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "clientbp.ggblueshark.com",
			"Accept-Encoding": "gzip"
		}
		
		response = requests.post("https://clientbp.ggblueshark.com/UpdateSocialBasicInfo", headers=headers, data=payload)
		
		return response.content
	
	
	def FuzzySearchAccountByName(self, name):
		fields = {
			1: str(name)
		}
		
		payload = self.create_protobuf_packet(fields)
		payload = payload.hex()
		payload = self.Encrypt_API(payload)
		payload = bytes.fromhex(payload)
		
		headers = {
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str(len(payload)),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "clientbp.ggblueshark.com",
			"Accept-Encoding": "gzip"
		}
		
		response = requests.post("https://clientbp.ggblueshark.com/FuzzySearchAccountByName", headers=headers, data=payload)
		
		return response.content
	
	
	def ChangeWishListItem(self, region, item_id, type, token):
		wishlist = change_wishlist_pb2.Wishlist()
		wishlist.value.item_id = item_id
		wishlist.value.garena_420 = 2265067095
		binary_data = wishlist.SerializeToString()
		hex_data = binary_data.hex()
		
		if str(item_id).startswith(("2030", "2040", "2050", "2110")):
			hex_type = "1"
		else:
			hex_type = "2"
		
		
		if hex_type == "1":
			prefix_to_remove = "0a0b08"
		
		else:
			prefix_to_remove = "0a0c08"
		
		truncate_pattern = "10d7dc88b808"
		
		if hex_data.startswith(prefix_to_remove):
			hex_data = hex_data[len(prefix_to_remove):]
		
		truncate_index = hex_data.find(truncate_pattern)
		
		if truncate_index != -1:
			hex_data = hex_data[:truncate_index]
		
		if mode == "add":
			
			if hex_type == "1":
				payload = f"0a04{hex_data}12001a064d616c6c5632"
			else:
				payload = f"0a05{hex_data}12001a064d616c6c5632"
		
		else:
			
			if hex_type == "1":
				payload = f"0a001204{hex_data}22064d616c6c5632"
			else:
				payload = f"0a001205{hex_data}22064d616c6c5632"
		
		payload = self.Encrypt_API(payload)
		payload = bytes.fromhex(payload)
		
		if region == "IND":
			url = "https://client.ind.freefiremobile.com/ChangeWishListItem"
		
		elif region == "BR":
			url = "https://client.us.freefiremobile.com/ChangeWishListItem"
		
		else:
			url = "https://clientbp.ggblueshark.com/ChangeWishListItem"
		
		headers = {
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Connection": "Close",
			"Accept-Encoding": "gzip",
			"Content-Type": "application/x-www-form-urlencoded",
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46"
		}
		
		response = requests.post(url, headers=headers, data=payload)
		
		return response.content
	
	
	def SendGift(self, player_id, message, token):
		player_id = self.Encrypt_ID(player_id)
		
		fields = {
			1: bytes.fromhex(player_id),
			2: 0,
			3: 1165,
			4: str(message),
			5: 0,
			7: 0,
			9: 0,
			10: 0,
			11: 15
		}
		
		payload = self.create_protobuf_packet(fields)
		payload = payload.hex()
		payload = self.Encrypt_API(payload)
		
		headers = {
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Connection": "Close",
			"Accept-Encoding": "gzip",
			"Content-Type": "application/x-www-form-urlencoded",
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46"
		}
		
		encrypt_data = bytes.fromhex(payload)
		
		response = requests.post("https://clientbp.ggblueshark.com/SendGift", headers=headers, data=encrypt_data)
		
		return response.content
		