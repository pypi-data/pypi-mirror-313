import os, sys
import requests
import json, jwt
import asyncio, aiohttp
import time, pytz, datetime

from PIL import Image, ImageOps
from io import BytesIO
from vrxx import VrxxTools
from concurrent.futures import ThreadPoolExecutor

vrxx = VrxxTools()
pool = ThreadPoolExecutor()

__all__ = ["GetPlayerPersonalShow", "LikeProfile", "VisitProfile", "CheckBanned", "TokenRetriever", "getRank", "getSkillName", "generateOutfitImg", "formatTime"]

async def _LikeProfile(payload, token, semaphore, session):
	try:
		headers = {
			"Expect": "100-continue",
			"Authorization": "Bearer " + token,
			"X-Unity-Version": "2018.4.11f1",
			"X-GA": "v1 1",
			"ReleaseVersion": "OB46",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": str( len(bytes.fromhex(payload)) ),
			"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; RMX1821 Build/QP1A.190711.020)",
			"Host": "clientbp.ggblueshark.com",
			"Connection": "Close",
			"Accept-Encoding": "gzip"
		}
		
		encrypt_data = bytes.fromhex(payload)
		
		async with semaphore:
			async with session.post("https://clientbp.ggblueshark.com/LikeProfile", headers=headers, data=encrypt_data, ssl=False) as response:
				response = response.status if response.status == 200 else await response.read()
				
				return response
	
	except Exception as e:
		return str(e)


async def LikeProfile(uid, region, tokens):
	success, error = 0, 0
	
	fields = {
		1: int(uid),
		2: str(region).upper()
	}
	
	payload = vrxx.create_protobuf_packet(fields)
	payload = payload.hex()
	payload = vrxx.Encrypt_API(payload)
	
	connect = aiohttp.TCPConnector(limit_per_host=100, limit=0, ttl_dns_cache=300)
	session = aiohttp.ClientSession(connector=connect)
	semaphore = asyncio.Semaphore(100)
	
	tasks = [_LikeProfile(payload, token, semaphore, session) for token in tokens]
	results = await asyncio.gather(*tasks)
	
	for result in results:
		if result == 200:
			success += 1
		
		else:
			error += 1
	
	await session.close()
	connect.close()
	
	return success, error


async def _VisitProfile(payload, token, semaphore, session):
	try:
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
		
		async with semaphore:
			async with session.post("https://clientbp.ggblueshark.com/GetPlayerPersonalShow", headers=headers, data=encrypt_data, ssl=False) as response:
				response = 0 if response.status != 200 else response.status
					
				return response
	
	except:
		return False


async def VisitProfile(uid, token, n):
	success, error = 0, 0
	fields = {
		1: int(uid),
		2: 9,
		3: 1
	}
		
	payload = vrxx.create_protobuf_packet(fields)
	payload = payload.hex()
	payload = vrxx.Encrypt_API(payload)
	
	connect = aiohttp.TCPConnector(limit_per_host=1000, limit=0, ttl_dns_cache=300)
	semaphore = asyncio.Semaphore(1000)
	session = aiohttp.ClientSession(connector=connect)
	
	tasks = [_VisitProfile(payload, token, semaphore, session) for _ in range(n)]
	results = await asyncio.gather(*tasks)
	
	for result in results:
		if result == 200:
			success += 1
		
		else:
			error += 1
	
	await session.close()
	connect.close()
	
	return success, error


def GetPlayerPersonalShow(uid, token):
	try:
		fields = {
			1: int(uid),
			2: 9,
			3: 1
		}
			
		payload = vrxx.create_protobuf_packet(fields)
		payload = payload.hex()
		payload = vrxx.Encrypt_API(payload)
		payload = bytes.fromhex(payload)
	
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
		
		response = requests.Session().post("https://clientbp.ggblueshark.com/GetPlayerPersonalShow", headers=headers, data=payload)
		
		return response.content
	
	except Exception as e:
		print(e)
		return False


def CheckBanned(uid):
	banned_period = {
		1: "Banned within this week.",
		2: "Banned within this month.",
		3: "Banned within the last three months.",
		5: "Banned within the last year.",
		6: "Ban period is unknown."
	}
	
	params = {
		"lang": "vn",
		"uid": str(uid)
	}

	headers = {
		"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
		"Accept": "application/json, text/plain, */*",
		"x-requested-with": "B6FksShzIgjfrYImLpTsadjS86sddhFH",
		"sec-ch-ua-mobile": "?1",
		"sec-ch-ua-platform": "\"Android\"",
		"sec-fetch-site": "same-origin",
		"sec-fetch-mode": "cors",
		"sec-fetch-dest": "empty",
		"referer": "https://ff.garena.com/vn/support",
		"accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
		"Cookie": "_gid=GA1.2.1024919953.1729411733; _ga_57E30E1PMN=GS1.2.1729411733.1.1.1729411813.0.0.0; _ga_KE3SY7MRSD=GS1.1.1729411750.3.1.1729412507.0.0.0; _ga_RF9R6YT614=GS1.1.1729411752.3.1.1729412507.0.0.0; _ga=GA1.1.956013504.1727393790"
	}
	
	try:
		response = requests.Session().get("https://ff.garena.com/api/antihack/check_banned", params=params, headers=headers)
		response = response.json()
		if not response.get("status") or response["status"] != "success":
			return (None, response.get("msg"))
			
		data = response.get("data")
		if not data:
			return (None, response.get("msg", "Banned Account Information Not Found"))
			
		is_banned = data.get("is_banned")
		period = data.get("period", 0)
			
		if not is_banned:
			return (False, None)
			
		return (True, banned_period.get(period))
		
	except Exception as e:
		return (None, str(e))


def GetGuestToken(guest_data):
	try:
		
		if len(guest_data) == 2:
			uid, password = guest_data
		elif len(guest_data) >= 2:
			uid, password, *_ = guest_data
		
		guest_access = vrxx.getGuestAccessToken(uid, password)
		access_token = guest_access["access_token"]
		open_id = guest_access["open_id"]
			
		if not access_token or not open_id:
			return False
			
		token = vrxx.getGuestJWTToken(access_token, open_id)
		
		if not token:
			return None
		
		return (uid, token)
	
	except Exception as e:
		return None


def TokenRetriever(token_list):
	tokens = []
	with ThreadPoolExecutor() as executor:
		results = list(executor.map(GetGuestToken, token_list))
	
	tokens = [result for result in results if result is not None]
	
	return tokens


def getRank(points, rank_type=None):
	if rank_type.upper() == "BR":
		if 1000 <= points < 1100:
			br_rank = "Bronze 1" + f" ({points})"
		elif 1100 <= points < 1200:
			br_rank = "Bronze 2" + f" ({points})"
		elif 1200 <= points < 1300:
			br_rank = "Bronze 3" + f" ({points})"
		elif 1300 <= points < 1400:
			br_rank = "Silver 1" + f" ({points})"
		elif 1400 <= points < 1500:
			br_rank = "Silver 2" + f" ({points})"
		elif 1500 <= points < 1600:
			br_rank = "Silver 3" + f" ({points})"
		elif 1600 <= points < 1725:
			br_rank = "Gold 1" + f" ({points})"
		elif 1725 <= points < 1850:
			br_rank = "Gold 2" + f" ({points})"
		elif 1850 <= points < 1975:
			br_rank = "Gold 3" + f" ({points})"
		elif 1975 <= points < 2100:
			br_rank = "Gold 4" + f" ({points})"
		elif 2100 <= points < 2225:
			br_rank = "Platinum 1" + f" ({points})"
		elif 2225 <= points < 2350:
			br_rank = "Platinum 2" + f" ({points})"
		elif 2350 <= points < 2475:
			br_rank = "Platinum 3" + f" ({points})"
		elif 2475 <= points < 2600:
			br_rank = "Platinum 4" + f" ({points})"
		elif 2600 <= points < 2750:
			br_rank = "Diamond 1" + f" ({points})"
		elif 2750 <= points < 2900:
			br_rank = "Diamond 2" + f" ({points})"
		elif 2900 <= points < 3050:
			br_rank = "Diamond 3" + f" ({points})"
		elif 3050 <= points < 3200:
			br_rank = "Diamond 4" + f" ({points})"
		elif 3200 <= points < 3500:
			br_rank = "Heroic 1★" + f" ({points})"
		elif 3500 <= points < 4000:
			br_rank = "Heroic 2★" + f" ({points})"
		elif 4000 <= points < 4600:
			br_rank = "Elite Heroic 3★" + f" ({points})"
		elif 4600 <= points < 5200:
			br_rank = "Elite Heroic 4★" + f" ({points})"
		elif 5200 <= points < 6000:
			br_rank = "Elite Heroic 5★" + f" ({points})"
		elif 6000 <= points < 6800:
			br_rank = "Master 1★" + f" ({points})"
		elif 6800 <= points < 7700:
			br_rank = "Master 2★" + f" ({points})"
		elif 7700 <= points < 8700:
			br_rank = "Elite Master 3★" + f" ({points})"
		elif 8700 <= points < 9800:
			br_rank = "Elite Master 4★" + f" ({points})"
		elif 9800 <= points:
			br_rank = "Elite Master 5★" + f" ({points})"
		else:
			br_rank = "Undefined"
		
		return br_rank
	
	elif rank_type.upper() == "CS":
		if points == 0:
			cs_rank = "Bronze 1 (0 ★)"
		elif points == 1:
			cs_rank = "Bronze 1 (1 ★)"
		elif points == 2:
			cs_rank = "Bronze 1 (2 ★)"
		elif points == 3:
			cs_rank = "Bronze 1 (3 ★)"
		elif points == 4:
			cs_rank = "Bronze 2 (1 ★)"
		elif points == 5:
			cs_rank = "Bronze 2 (2 ★)"
		elif points == 6:
			cs_rank = "Bronze 2 (3 ★)"
		elif points == 7:
			cs_rank = "Bronze 3 (1 ★)"
		elif points == 8:
			cs_rank = "Bronze 3 (2 ★)"
		elif points == 9:
			cs_rank = "Bronze 3 (3 ★)"
		elif points == 10:
			cs_rank = "Silver 1 (1 ★)"
		elif points == 11:
			cs_rank = "Silver 1 (2 ★)"
		elif points == 12:
			cs_rank = "Silver 1 (3 ★)"
		elif points == 13:
			cs_rank = "Silver 1 (4 ★)"
		elif points == 14:
			cs_rank = "Silver 2 (1 ★)"
		elif points == 15:
			cs_rank = "Silver 2 (2 ★)"
		elif points == 16:
			cs_rank = "Silver 2 (3 ★)"
		elif points == 17:
			cs_rank = "Silver 2 (4 ★)"
		elif points == 18:
			cs_rank = "Silver 3 (1 ★)"
		elif points == 19:
			cs_rank = "Silver 3 (2 ★)"
		elif points == 20:
			cs_rank = "Silver 3 (3 ★)"
		elif points == 21:
			cs_rank = "Silver 3 (4 ★)"
		elif points == 22:
			cs_rank = "Gold 1 (1 ★)"
		elif points == 23:
			cs_rank = "Gold 1 (2 ★)"
		elif points == 24:
			cs_rank = "Gold 1 (3 ★)"
		elif points == 25:
			cs_rank = "Gold 1 (4 ★)"
		elif points == 26:
			cs_rank = "Gold 2 (1 ★)"
		elif points == 27:
			cs_rank = "Gold 2 (2 ★)"
		elif points == 28:
			cs_rank = "Gold 2 (3 ★)"
		elif points == 29:
			cs_rank = "Gold 2 (4 ★)"
		elif points == 30:
			cs_rank = "Gold 3 (1 ★)"
		elif points == 31:
			cs_rank = "Gold 3 (2 ★)"
		elif points == 32:
			cs_rank = "Gold 3 (3 ★)"
		elif points == 33:
			cs_rank = "Gold 3 (4 ★)"
		elif points == 34:
			cs_rank = "Gold 4 (1 ★)"
		elif points == 35:
			cs_rank = "Gold 4 (2 ★)"
		elif points == 36:
			cs_rank = "Gold 4 (3 ★)"
		elif points == 37:
			cs_rank = "Gold 4 (4 ★)"
		elif points == 38:
			cs_rank = "Platinum 1 (1 ★)"
		elif points == 39:
			cs_rank = "Platinum 1 (2 ★)"
		elif points == 40:
			cs_rank = "Platinum 1 (3 ★)"
		elif points == 41:
			cs_rank = "Platinum 1 (4 ★)"
		elif points == 42:
			cs_rank = "Platinum 1 (5 ★)"
		elif points == 43:
			cs_rank = "Platinum 2 (1 ★)"
		elif points == 44:
			cs_rank = "Platinum 2 (2 ★)"
		elif points == 45:
			cs_rank = "Platinum 2 (3 ★)"
		elif points == 46:
			cs_rank = "Platinum 2 (4 ★)"
		elif points == 47:
			cs_rank = "Platinum 2 (5 ★)"
		elif points == 48:
			cs_rank = "Platinum 3 (1 ★)"
		elif points == 49:
			cs_rank = "Platinum 3 (2 ★)"
		elif points == 50:
			cs_rank = "Platinum 3 (3 ★)"
		elif points == 51:
			cs_rank = "Platinum 3 (4 ★)"
		elif points == 52:
			cs_rank = "Platinum 3 (5 ★)"
		elif points == 53:
			cs_rank = "Platinum 4 (1 ★)"
		elif points == 54:
			cs_rank = "Platinum 4 (2 ★)"
		elif points == 55:
			cs_rank = "Platinum 4 (3 ★)"
		elif points == 56:
			cs_rank = "Platinum 4 (4 ★)"
		elif points == 57:
			cs_rank = "Platinum 4 (5 ★)"
		elif points == 58:
			cs_rank = "Diamond 1 (1 ★)"
		elif points == 59:
			cs_rank = "Diamond 1 (2 ★)"
		elif points == 60:
			cs_rank = "Diamond 1 (3 ★)"
		elif points == 61:
			cs_rank = "Diamond 1 (4 ★)"
		elif points == 62:
			cs_rank = "Diamond 1 (5 ★)"
		elif points == 63:
			cs_rank = "Diamond 2 (1 ★)"
		elif points == 64:
			cs_rank = "Diamond 2 (2 ★)"
		elif points == 65:
			cs_rank = "Diamond 2 (3 ★)"
		elif points == 66:
			cs_rank = "Diamond 2 (4 ★)"
		elif points == 67:
			cs_rank = "Diamond 2 (5 ★)"
		elif points == 68:
			cs_rank = "Diamond 3 (1 ★)"
		elif points == 69:
			cs_rank = "Diamond 3 (2 ★)"
		elif points == 70:
			cs_rank = "Diamond 3 (3 ★)"
		elif points == 71:
			cs_rank = "Diamond 3 (4 ★)"
		elif points == 72:
			cs_rank = "Diamond 3 (5 ★)"
		elif points == 73:
			cs_rank = "Diamond 4 (1 ★)"
		elif points == 74:
			cs_rank = "Diamond 4 (2 ★)"
		elif points == 75:
			cs_rank = "Diamond 4 (3 ★)"
		elif points == 76:
			cs_rank = "Diamond 4 (4 ★)"
		elif points == 77:
			cs_rank = "Diamond 4 (5 ★)"
		elif 78 <= points < 127:
			cs_rank = points - 77
			cs_rank = "Heroic (" + str(cs_rank) + " ★)"
		elif 127 <= points < 177:
			cs_rank = points - 77
			cs_rank = "Master (" + str(cs_rank) + " ★)"
		elif 177 <= points:
			cs_rank = points - 77
			cs_rank = "Elite Master (" + str(cs_rank) + " ★)"
		else:
			cs_rank = "Undefined"
		
		return cs_rank


def getSkillName(skill_id):
	skillList = {}
	def add_key_value(keys, value):
		for key in keys:
			skillList[key] = value
	
	skillListData = {
		10: "Olivia (P)",
		20: "Kelly (P)",
		30: "Ford (P)",
		40: "Andrew (P)",
		50: "Nikita (P)",
		60: "Misha (P)",
		70: "Maxim (P)",
		80: "Kla (P)",
		90: "Paloma (P)",
		100: "Miguel (P)",
		110: "Caroline (P)",
		120: "Wukong (A)",
		130: "Antonio (P)",
		140: "Moco (P)",
		150: "Hayato (P)",
		170: "Laura (P)",
		180: "Rafael (P)",
		190: "A124 (A)",
		200: "Joseph (P)",
		210: "Shani (P)",
		220: "Alok (A)",
		230: "Alvaro (P)",
		240: "Notora (P)",
		250: "Kelly \"The Swift\" (P)",
		260: "Steffie (A)",
		270: "Jota (P)",
		280: "Kapella (P)",
		290: "Luqueta (P)",
		300: "Wolfrahh (P)",
		310: "Clu (A)",
		320: "Hayato \"Firebrand\" (P)",
		330: "Jai (P)",
		340: "K (A)",
		350: "Dasha (P)",
		360: "Sverr (A)",
		370: "A-Patroa",
		380: "Chrono (A)",
		390: "Snowelle (P)",
		400: "Skyler (A)",
		410: "Shirou (P)",
		420: "Andrew \"The Fierce\" (P)",
		430: "Maro (P)",
		440: "Xayne (A)",
		450: "D-bee (P)",
		460: "Thiva (P)",
		470: "Dimitri (A)",
		480: "Moco \"Enigma\" (P)",
		490: "Leon (P)",
		500: "Otho (P)",
		510: "Jai's Microchip (P)",
		520: "Nairi (P)",
		530: "Luna (P)",
		540: "Kenta (A)",
		550: "Homer (A)",
		560: "Iris (A)",
		570: "J.Biebs (P)",
		580: "Tatsuya (A)",
		590: "Stunt Double",
		600: "Santino (A)",
		610: "J.Biebs' Microchip (P)",
		620: "Orion (A)",
		630: "Alvaro \"Rageblast\" (P)",
		650: "Sonia (P)",
		660: "Suzy (P)",
		670: "Ignis (A)",
		680: "Ryden (A)",
		690: "Kairos (A)",
		700: "Kassie (A)",
		2201: "Awakened Alok (A)"
	}
	
	for skillId, skillName in skillListData.items():
		skill = [int(f"{skillId}{i+1}") for i in range(6)]
		add_key_value(skill, skillName)
	
	return skillList.get(skill_id)


def load_image_from_url(url):
	try:
		response = requests.get(url)
		image = Image.open(BytesIO(response.content))
		
		return image
	except:
		return False


def generateOutfitImg(outfitList, animationId=None, weaponId=None):
	itemsId = json.load( open("./core/OB46-Item-ID.json") )
	baseUrl = "https://freefiremobile-a.akamaihd.net/common/Local/PK/FF_UI_Icon/"
	
	hairIcon = "Icon_avatar_default_Hair"
	maskIcon = "Icon_avatar_default_Face"
	faceIcon = "Icon_avatar_default_headadditive"
	shirtIcon = "Icon_avatar_cos_top_default"
	pantsIcon = "Icon_avatar_cos_bottom_default"
	shoesIcon = "Icon_avatar_cos_shoe_default"
	bundleIcon = None
	
	outfitForm = Image.open("./assets/Images/OutfitForm.png")
	for outfit in outfitList:
		outfit, outfitId = next(((item["Icon_Name"], item["Item_ID"]) for item in itemsId if item["Item_ID"] == str(outfit)), ("", ""))
		print(outfit)
		if "_hair_" in outfit.lower():
			hairIcon = outfit
		elif "_accessory_" in outfit.lower():
			maskIcon = outfit
		elif "_headadditive_" in outfit.lower():
			faceIcon = outfit
		elif next(item not in outfit.lower() for item in ["_top", "_top_cos", "_shirt_cos", "_tshirt", "_shirt"]) and "_cos_" in outfit.lower() and outfitId.startswith("203"):
			bundleIcon = outfit
		elif any(item in outfit.lower() for item in ["_top", "_top_cos", "_shirt_cos", "_tshirt", "_shirt"]) and outfitId.startswith("203") or outfitId.startswith("203"):
			shirtIcon = outfit
		elif outfitId.startswith("204"):
			pantsIcon = outfit
		elif outfitId.startswith("205"):
			shoesIcon = outfit
	
	
	hairIcon = load_image_from_url(baseUrl + hairIcon + ".png")
	if not hairIcon:
		hairIcon = load_image_from_url(baseUrl + "Icon_avatar_default_Hair.png")
	
	hairIcon = ImageOps.mirror(hairIcon)
	outfitForm.paste(hairIcon, (252, 90), hairIcon)
	
	
	maskIcon = load_image_from_url(baseUrl + maskIcon + ".png")
	if not maskIcon:
		maskIcon = load_image_from_url(baseUrl + "Icon_avatar_default_Face.png")
	
	maskIcon = ImageOps.mirror(maskIcon)
	outfitForm.paste(maskIcon, (97, 230), maskIcon)
	
	
	faceIcon = load_image_from_url(baseUrl + faceIcon + ".png")
	if not faceIcon:
		faceIcon = load_image_from_url(baseUrl + "Icon_avatar_default_headadditive.png")
	
	faceIcon = ImageOps.mirror(faceIcon)
	outfitForm.paste(faceIcon, (97, 430), faceIcon)
	
	
	shirtIcon = load_image_from_url(baseUrl + shirtIcon + ".png")
	if not shirtIcon:
		shirtIcon = load_image_from_url(baseUrl + "Icon_avatar_cos_top_default.png")
	
	shirtIcon = ImageOps.mirror(shirtIcon)
	shirtIcon = shirtIcon.resize((102, 102))
	outfitForm.paste(shirtIcon, (918, 94), shirtIcon)
	
	pantsIcon = load_image_from_url(baseUrl + pantsIcon + ".png")
	if not pantsIcon:
		pantsIcon = load_image_from_url(baseUrl + "Icon_avatar_cos_bottom_default.png")
	
	pantsIcon = ImageOps.mirror(pantsIcon)
	pantsIcon = pantsIcon.resize((102, 102))
	outfitForm.paste(pantsIcon, (1075, 232), pantsIcon)
	
	shoesIcon = load_image_from_url(baseUrl + shoesIcon + ".png")
	if not shoesIcon:
		shoesIcon = load_image_from_url(baseUrl + "Icon_avatar_cos_shoe_default.png")
	
	shoesIcon = ImageOps.mirror(shoesIcon)
	shoesIcon = shoesIcon.resize((102, 102))
	outfitForm.paste(shoesIcon, (1074, 432), shoesIcon)
	
	if not weaponId:
		weaponIcon = Image.open("./assets/Images/FF_icon_gun_default.png")
		weaponIcon = ImageOps.mirror(weaponIcon)
		weaponIcon = weaponIcon.resize((74, 74))
		weaponIcon = weaponIcon.rotate(20, expand=True)
		outfitForm.paste(weaponIcon, (252, 583), weaponIcon)
	
	else:
		weaponIcon = next((item["Icon_Name"] for item in itemsId if item["Item_ID"] == str(weaponId)), "Undefined")
		weaponIcon = load_image_from_url(baseUrl + weaponIcon + ".png")
		if not weaponIcon:
			weaponIcon = Image.open("./assets/Images/FF_icon_gun_default.png")
			weaponIcon = ImageOps.mirror(weaponIcon)
			weaponIcon = weaponIcon.resize((74, 74))
			weaponIcon = weaponIcon.rotate(20, expand=True)
			outfitForm.paste(weaponIcon, (252, 583), weaponIcon)
		
		else:
			weaponIcon = ImageOps.mirror(weaponIcon)
			w, h = weaponIcon.size
			
			if str(weaponId).startswith("90719"):
				weaponIcon = weaponIcon.resize((w - 128, h - 34))
				weaponIcon = weaponIcon.rotate(34, expand=True)
				outfitForm.paste(weaponIcon, (218, 550), weaponIcon)
			
			else:
				weaponIcon = weaponIcon.resize((w - 160, h - 44))
				weaponIcon = weaponIcon.rotate(29, expand=True)
				outfitForm.paste(weaponIcon, (234, 580), weaponIcon)
	
	
	if not animationId:
		animationIcon = load_image_from_url(baseUrl + "FF_UI_Emote_Collection_BAN.png")
		animationIcon = animationIcon.resize((68, 68))
		outfitForm.paste(animationIcon, (934, 596), animationIcon)
	
	else:
		animationIcon = next((item["Icon_Name"] for item in itemsId if item["Item_ID"] == str(animationId)), "Undefined")
		animationIcon = load_image_from_url(baseUrl + animationIcon + ".png")
		if not animationIcon:
			animationIcon = load_image_from_url(baseUrl + "FF_UI_Emote_Collection_BAN.png")
			animationIcon = animationIcon.resize((68, 68))
			outfitForm.paste(animationIcon, (934, 596), animationIcon)
		
		else:
			animationIcon = animationIcon.resize((92, 92))
			animationIcon = ImageOps.mirror(animationIcon)
			outfitForm.paste(animationIcon, (924, 592), animationIcon)
	
	
	if bundleIcon:
		bundleIcon = load_image_from_url(baseUrl + bundleIcon + ".png")
		if bundleIcon:
			bundleIcon = ImageOps.mirror(bundleIcon)
			bundleIcon = bundleIcon.resize((102, 102))
			outfitForm.paste(bundleIcon, (1074, 583), bundleIcon)
	
	
	return outfitForm


def formatTime(timestamp):
	try:
		timestamp = int(timestamp)
	except:
		timestamp = 0
	
	if not timestamp:
		return "Undefined"
	
	utc_time = datetime.datetime.utcfromtimestamp(timestamp)
	vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
	vietnam_time = utc_time.astimezone(vietnam_tz)
	formatted_time = vietnam_time.strftime("%d/%m/%Y %H:%M")
	
	return formatted_time
