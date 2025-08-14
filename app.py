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







from flask import Flask, request, jsonify
import google.generativeai as genai
import json
import os
import imghdr
import requests

app = Flask(__name__)

# 設定 API Key
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# Google API URL
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

@app.route("/", methods=["GET"])
def home():
    return "OCR Server is running"

@app.route("/ocr", methods=["POST"])
def ocr():
    if 'image' not in request.files or 'uid' not in request.form:
        return jsonify({"error": "Missing image or uid"}), 400
    
    image_file = request.files["image"]
    uid = request.form["uid"]
    
    img_bytes = image_file.read()
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
        return jsonify({"error": "Invalid JSON format", "raw": response.text}), 500

    lat, lng = None, None

    # case 1: 店名 + 地址
    if name != "error" and address != "error":
        lat, lng = geocode_address(address)
    
    # case 2: 只有地址
    elif name == "error" and address != "error":
        lat, lng = geocode_address(address)
        if lat and lng:
            found_name = find_place_name_by_address(address)
            if found_name:
                name = found_name
    
    # case 3: 只有店名
    elif name != "error" and address == "error":
        found_address, lat, lng = find_address_by_place_name(name)
        if found_address:
            address = found_address
    
    # case 4: 都沒有
    if name == "error" and address == "error":
        return jsonify({"error": "No valid name or address found"}), 400

    # 整理結果
    result = {
        "name": name,
        "address": address,
        "lat": lat,
        "lng": lng,
        "uid": uid
    }

    # 寫入 Google Sheet
    sheet_url = "https://script.google.com/macros/s/AKfycbzf-llhgSP97vvDuzisINKiWpS2YOBUeNBrefILD8peEhMW1bGwTrNQyT8O29wqBU10/exec"
    params = {
        "name": name,
        "address": address,
        "lat": lat,
        "lng": lng,
        "uid": uid
    }
    try:
        r = requests.get(sheet_url, params=params)
        if r.status_code != 200:
            return jsonify({"error": "Failed to write to sheet", "status_code": r.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result)


# ===== Google API Helper Functions =====

def geocode_address(address):
    params = {"address": address, "key": GOOGLE_API_KEY}
    r = requests.get(GEOCODE_URL, params=params).json()
    if r["status"] == "OK":
        loc = r["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None, None

def find_place_name_by_address(address):
    params = {
        "input": address,
        "inputtype": "textquery",
        "fields": "name",
        "key": GOOGLE_API_KEY
    }
    r = requests.get(PLACES_SEARCH_URL, params=params).json()
    if r["status"] == "OK":
        return r["candidates"][0]["name"]
    return None

def find_address_by_place_name(name):
    params = {
        "input": name,
        "inputtype": "textquery",
        "fields": "formatted_address,geometry",
        "key": GOOGLE_API_KEY
    }
    r = requests.get(PLACES_SEARCH_URL, params=params).json()
    if r["status"] == "OK":
        c = r["candidates"][0]
        address = c.get("formatted_address")
        loc = c["geometry"]["location"]
        return address, loc["lat"], loc["lng"]
    return None, None, None


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
