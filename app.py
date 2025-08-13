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


from flask import Flask, request, jsonify
import google.generativeai as genai
import json
import os
import imghdr
import requests

app = Flask(__name__)

# 設定你的 Google API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

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
        name = json_data.get("店名", "error")
        address = json_data.get("地址", "error")
    except:
        return jsonify({"error": "Invalid JSON format", "raw": response.text}), 500
    
    # 把中文鍵轉成英文方便寫入DB或Sheet
    mapped_data = {
        "name": name,
        "address": address,
        "uid": uid
    }
    
    # 直接把結果寫入 Google Sheet (用 Google Apps Script Web App URL)
    sheet_url = "https://script.google.com/macros/s/AKfycbzf-llhgSP97vvDuzisINKiWpS2YOBUeNBrefILD8peEhMW1bGwTrNQyT8O29wqBU10/exec"
    params = {
        "name": mapped_data["name"],
        "address": mapped_data["address"],
        "uid": mapped_data["uid"]
    }
    
    try:
        r = requests.get(sheet_url, params=params)
        if r.status_code == 200:
            return jsonify({"status": "success", "name": name, "address": address})
        else:
            return jsonify({"error": "Failed to write to sheet", "status_code": r.status_code}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)