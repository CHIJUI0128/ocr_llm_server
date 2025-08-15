#from flask import Flask, request, jsonify
#from flask_cors import CORS
#import google.generativeai as genai
#from PIL import Image
#import json
#import os
#import imghdr
#
#app = Flask(__name__)
#CORS(app)
#
## 初始化 Gemini 模型
#genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
#model = genai.GenerativeModel("gemini-1.5-pro")
#
#@app.route("/ocr", methods=["POST"])
#def ocr():
#    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", flush=True)
#    if 'image' not in request.files:
#        return jsonify({"error": "No image uploaded"}), 400
#
#    image_file = request.files["image"]
#    img_bytes = image_file.read()
#
#    # 嘗試判斷 MIME 類型（jpg / png）
#    image_type = imghdr.what(None, h=img_bytes)
#    mime_type = f"image/{image_type}" if image_type else "image/jpeg"
#
#    # 更嚴格的 prompt，要求只輸出 JSON，無其他說明
#    prompt = """
#            請從這張圖片中擷取「店名」與「地址」，只回傳 JSON 格式如下：
#            {
#            "店名": "xxx",
#            "地址": "xxx"
#            }
#            不要多加任何註解、說明或文字。
#            若無法擷取，請輸出"error"，例如：
#            {
#            "店名": "error",
#            "地址": "error"
#            }
#            """
#
#    response = model.generate_content([
#        prompt,
#        {
#            "inline_data": {
#                "mime_type": mime_type,
#                "data": img_bytes
#            }
#        }
#    ])
#    print("Gemini raw response:", flush=True)
#    print(response, flush=True)
#    print("辨識結果：", flush=True)
#    print(response.text, flush=True)
#
#    # 嘗試解析模型輸出為 JSON
#    try:
#        extracted = response.text.strip()
#
#        # 移除 ```json 開頭與 ``` 結尾
#        if extracted.startswith("```json"):
#            extracted = extracted[7:]  # 去掉 ```json
#        if extracted.endswith("```"):
#            extracted = extracted[:-3]  # 去掉 ```
#
#        extracted = extracted.strip()
#
#        # 解析 JSON
#        json_data = json.loads(extracted)
#
#        # 👉 將中文鍵轉成英文鍵
#        mapped_data = {
#            "name": json_data.get("店名", "error"),
#            "address": json_data.get("地址", "error")
#        }
#
#        return jsonify(mapped_data)
#
#    except Exception as e:
#        return jsonify({
#            "error": "Invalid JSON format",
#            "raw": response.text
#        })
#
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000)


# from flask import Flask, request, jsonify
# import google.generativeai as genai
# import json
# import os
# import imghdr
# import requests

# app = Flask(__name__)

# # 設定你的 Google API key
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# model = genai.GenerativeModel("gemini-1.5-pro")

# @app.route("/", methods=["GET"])
# def home():
#     return "OCR Server is running"

# @app.route("/ocr", methods=["POST"])
# def ocr():
#     if 'image' not in request.files or 'uid' not in request.form:
#         return jsonify({"error": "Missing image or uid"}), 400
    
#     image_file = request.files["image"]
#     uid = request.form["uid"]
    
#     img_bytes = image_file.read()
#     image_type = imghdr.what(None, h=img_bytes)
#     mime_type = f"image/{image_type}" if image_type else "image/jpeg"
    
#     prompt = """
#     請從這張圖片中擷取「店名」與「地址」，只回傳 JSON 格式如下：
#     {
#     "店名": "xxx",
#     "地址": "xxx"
#     }
#     不要多加任何註解、說明或文字。
#     若無法擷取，請輸出"error"，例如：
#     {
#     "店名": "error",
#     "地址": "error"
#     }
#     """
    
#     response = model.generate_content([
#         prompt,
#         {
#             "inline_data": {
#                 "mime_type": mime_type,
#                 "data": img_bytes
#             }
#         }
#     ])
    
#     extracted = response.text.strip()
#     if extracted.startswith("```json"):
#         extracted = extracted[7:]
#     if extracted.endswith("```"):
#         extracted = extracted[:-3]
#     extracted = extracted.strip()
    
#     try:
#         json_data = json.loads(extracted)
#         name = json_data.get("店名", "error")
#         address = json_data.get("地址", "error")
#     except:
#         return jsonify({"error": "Invalid JSON format", "raw": response.text}), 500
    
#     # 把中文鍵轉成英文方便寫入DB或Sheet
#     mapped_data = {
#         "name": name,
#         "address": address,
#         "uid": uid
#     }
    
#     # 直接把結果寫入 Google Sheet (用 Google Apps Script Web App URL)
#     sheet_url = "https://script.google.com/macros/s/AKfycbzf-llhgSP97vvDuzisINKiWpS2YOBUeNBrefILD8peEhMW1bGwTrNQyT8O29wqBU10/exec"
#     params = {
#         "name": mapped_data["name"],
#         "address": mapped_data["address"],
#         "uid": mapped_data["uid"]
#     }
    
#     try:
#         r = requests.get(sheet_url, params=params)
#         if r.status_code == 200:
#             return jsonify({"status": "success", "name": name, "address": address})
#         else:
#             return jsonify({"error": "Failed to write to sheet", "status_code": r.status_code}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # if __name__ == "__main__":
# #     app.run(host="0.0.0.0", port=5000)

# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 8080))
#     app.run(host="0.0.0.0", port=port)



import google.generativeai as genai
import json
import os
import imghdr
import requests
from datetime import datetime

# ===== 設定 =====
GOOGLE_API_KEY =os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

# Google API URL
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

# Google Apps Script Web App URL (需要替換成你的URL)
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbzyiO8YXVGA75ZDPNWl0-ASh6Wt19TyYD59IWQswM0jU0-ehdzSB3GutEOd-MGJsNiQ/exec"

# ===== Google API Helper Functions =====
def geocode_address(address):
    """將地址轉換為經緯度"""
    params = {"address": address, "key": GOOGLE_API_KEY}
    r = requests.get(GEOCODE_URL, params=params).json()
    if r["status"] == "OK":
        loc = r["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None, None

def find_place_name_by_address(address):
    """根據地址查找店名"""
    params = {
        "input": address,
        "inputtype": "textquery",
        "fields": "name",
        "key": GOOGLE_API_KEY
    }
    r = requests.get(PLACES_SEARCH_URL, params=params).json()
    if r["status"] == "OK" and r["candidates"]:
        return r["candidates"][0]["name"]
    return None

def find_address_by_place_name(name):
    """根據店名查找地址和經緯度"""
    params = {
        "input": name,
        "inputtype": "textquery",
        "fields": "formatted_address,geometry",
        "key": GOOGLE_API_KEY
    }
    r = requests.get(PLACES_SEARCH_URL, params=params).json()
    if r["status"] == "OK" and r["candidates"]:
        c = r["candidates"][0]
        address = c.get("formatted_address")
        loc = c["geometry"]["location"]
        return address, loc["lat"], loc["lng"]
    return None, None, None

def save_to_google_sheet(data):
    """將資料存入Google Sheet"""
    payload = {
        "uid": data["uid"],
        "name": data["name"],
        "address": data["address"],
        "time": data["time"],
        "latitude": data["latitude"],
        "longitude": data["longitude"]
    }
    
    try:
        response = requests.post(GOOGLE_SHEET_URL, json=payload)
        if response.status_code == 200:
            print("✅ 資料已存入Google Sheet")
            return True
        else:
            print(f"❌ Google Sheet寫入失敗：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Google Sheet寫入錯誤：{e}")
        return False

# ===== 本地測試 OCR 流程 =====
def process_image(image_path, uid="test_uid"):
    """處理圖片：OCR → 地理編碼 → 存入Google Sheet"""
    
    # 讀取圖片
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    image_type = imghdr.what(None, h=img_bytes)
    mime_type = f"image/{image_type}" if image_type else "image/jpeg"

    prompt = """
    請從這張圖片中擷取「店名」與「地址」，只回傳 JSON 格式如下：
    {
    "店名": "xxx",
    "地址": "xxx"
    }
    不要多加任何註解、說明或文字。
    若無法擷取，請輸出"error"，例如：
    {
    "店名": "error",
    "地址": "error"
    }
    """

    # 呼叫 Gemini OCR
    response = model.generate_content([
        prompt,
        {
            "inline_data": {
                "mime_type": mime_type,
                "data": img_bytes
            }
        }
    ])

    extracted = response.text.strip()
    if extracted.startswith("```json"):
        extracted = extracted[7:]
    if extracted.endswith("```"):
        extracted = extracted[:-3]
    extracted = extracted.strip()

    try:
        json_data = json.loads(extracted)
        name = json_data.get("店名", "error").strip()
        address = json_data.get("地址", "error").strip()
    except:
        raise ValueError(f"Invalid JSON format: {response.text}")

    lat, lng = None, None

    # case 1: 店名 + 地址都有
    if name != "error" and address != "error":
        print(f"🔍 Case 1: 店名+地址 - {name}, {address}")
        lat, lng = geocode_address(address)

    # case 2: 只有地址
    elif name == "error" and address != "error":
        print(f"🔍 Case 2: 只有地址 - {address}")
        lat, lng = geocode_address(address)
        if lat and lng:
            found_name = find_place_name_by_address(address)
            if found_name:
                name = found_name
                print(f"✅ 根據地址找到店名：{name}")

    # case 3: 只有店名
    elif name != "error" and address == "error":
        print(f"🔍 Case 3: 只有店名 - {name}")
        found_address, lat, lng = find_address_by_place_name(name)
        if found_address:
            address = found_address
            print(f"✅ 根據店名找到地址：{address}")

    # case 4: 都沒有
    else:
        raise ValueError("無法從圖片中提取有效的店名或地址")

    # 驗證是否成功獲得經緯度
    if lat is None or lng is None:
        raise ValueError(f"無法獲得有效的經緯度：name={name}, address={address}")

    # 準備要存入Google Sheet的資料
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = {
        "uid": uid,
        "name": name,
        "address": address,
        "time": current_time,
        "latitude": lat,
        "longitude": lng
    }

    # 存入Google Sheet
    if save_to_google_sheet(result):
        print("✅ 處理完成並存入資料庫")
    else:
        print("⚠️ 處理完成但資料庫寫入失敗")

    return result

# ===== Flask Web API 版本 =====
def create_flask_app():
    """建立Flask API服務"""
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route('/ocr', methods=['POST'])
    def ocr_endpoint():
        """OCR API端點"""
        try:
            # 檢查是否有圖片檔案
            if 'image' not in request.files:
                return jsonify({"error": "No image file"}), 400
            
            image_file = request.files['image']
            uid = request.form.get('uid', 'unknown')
            
            if image_file.filename == '':
                return jsonify({"error": "No image selected"}), 400
            
            # 讀取圖片資料
            img_bytes = image_file.read()
            
            # 處理圖片（修改為使用bytes而不是檔案路徑）
            result = process_image_bytes(img_bytes, uid)
            
            return jsonify(result)
            
        except Exception as e:
            print(f"❌ API錯誤：{e}")
            return jsonify({"error": str(e)}), 500
    
    return app

def process_image_bytes(img_bytes, uid="unknown"):
    """處理圖片bytes資料"""
    
    image_type = imghdr.what(None, h=img_bytes)
    mime_type = f"image/{image_type}" if image_type else "image/jpeg"

    prompt = """
    請從這張圖片中擷取「店名」與「地址」，只回傳 JSON 格式如下：
    {
    "店名": "xxx",
    "地址": "xxx"
    }
    不要多加任何註解、說明或文字。
    若無法擷取，請輸出"error"，例如：
    {
    "店名": "error",
    "地址": "error"
    }
    """

    # 呼叫 Gemini OCR
    response = model.generate_content([
        prompt,
        {
            "inline_data": {
                "mime_type": mime_type,
                "data": img_bytes
            }
        }
    ])

    extracted = response.text.strip()
    if extracted.startswith("```json"):
        extracted = extracted[7:]
    if extracted.endswith("```"):
        extracted = extracted[:-3]
    extracted = extracted.strip()

    try:
        json_data = json.loads(extracted)
        name = json_data.get("店名", "error").strip()
        address = json_data.get("地址", "error").strip()
    except:
        raise ValueError(f"Invalid JSON format: {response.text}")

    lat, lng = None, None

    # 地理編碼邏輯（同process_image）
    if name != "error" and address != "error":
        print(f"🔍 Case 1: 店名+地址 - {name}, {address}")
        lat, lng = geocode_address(address)
    elif name == "error" and address != "error":
        print(f"🔍 Case 2: 只有地址 - {address}")
        lat, lng = geocode_address(address)
        if lat and lng:
            found_name = find_place_name_by_address(address)
            if found_name:
                name = found_name
    elif name != "error" and address == "error":
        print(f"🔍 Case 3: 只有店名 - {name}")
        found_address, lat, lng = find_address_by_place_name(name)
        if found_address:
            address = found_address
    else:
        raise ValueError("無法從圖片中提取有效的店名或地址")

    if lat is None or lng is None:
        raise ValueError(f"無法獲得有效的經緯度：name={name}, address={address}")

    # 準備資料並存入Google Sheet
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = {
        "uid": uid,
        "name": name,
        "address": address,
        "time": current_time,
        "latitude": lat,
        "longitude": lng
    }

    # 存入Google Sheet
    save_to_google_sheet(result)

    return result

# ===== 測試執行 =====
if __name__ == "__main__":
    # 本地測試
    # image_path = r"C:\Users\吳基瑞\Desktop\123.png"  # 換成你本地的圖片路徑
    # try:
    #     result = process_image(image_path)
    #     print("\n=== 處理結果 ===")
    #     print(json.dumps(result, ensure_ascii=False, indent=2))
    # except Exception as e:
    #     print(f"❌ 處理失敗：{e}")
    
    # 啟動Flask API服務（注釋掉本地測試時使用）
    app = create_flask_app()
    app.run(host='0.0.0.0', port=8080, debug=True)

