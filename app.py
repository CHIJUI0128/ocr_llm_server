# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from PIL import Image
# import io
# import google.generativeai as genai
# import easyocr
# import os
# import numpy as np
# import json
# app = Flask(__name__)
# CORS(app)  # 允許跨域

# # ✅ 設定 API 金鑰
# # 改為讀取環境變數（安全）
# import os
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# reader = easyocr.Reader(['ch_tra', 'en'], gpu=False)

# @app.route('/ocr', methods=['POST'])
# def ocr():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image provided'}), 400
#     img = Image.open(request.files['image'].stream)
#     # text = pytesseract.image_to_string(img, lang='eng+chi_tra')

#     # name = "Wannaeat 好想吃甜點工作室"
#     # address = "110台北市信義區永吉路30巷158弄23號"
    

#     # ✅ 用 EasyOCR 讀取圖片
#     # ocr_result = reader.readtext(r"D:\my_foodmap_app\test.jpg", detail=0)
#     # img = Image.open(request.files['image'].stream).convert("RGB")
#     ocr_result = reader.readtext(np.array(img), detail=0)
#     text_input = "\n".join(ocr_result)

#     # ✅ 使用 Gemini 解析
#     model = genai.GenerativeModel('gemini-1.5-pro')

#     prompt = f"""
#     這是一段從圖片中 OCR 擷取出來的文字：

#     {text_input}

#     請你從中推斷出：
#     1. 店家名稱（如果有的話）
#     2. 店家地址（如果有的話）

#     輸出格式請用 JSON（不要解釋、不加註解）：
#     {{"name": "xxx", "address": "xxx"}}
#     """

#     response = model.generate_content(prompt)
#     print("Gemini 回覆：\n", response.text)
#     try:
#         # 假設 response 是你原始回傳的結果
#         text_output = response.candidates[0].content.parts[0].text

#         # 移除 markdown 的 ```json 與 ```
#         cleaned_text = text_output.strip().strip("```json").strip("```").strip()

#         # 轉換成 Python 字典
#         result = json.loads(cleaned_text)

#         # 取出 name 和 address
#         name = result.get("name", "未知")
#         address = result.get("address", "未知")

#         print("店名：", name)
#         print("地址：", address)

#     except json.JSONDecodeError:
#         name = '未知店名'
#         address = '未知地址'
#     print(name,address)
    
    
#     return jsonify({'name': name,'address': address})


# if __name__ == '__main__':
#     # app.run(host='0.0.0.0', port=5000)

#     port = int(os.environ.get("PORT", 5000))
#     app.run(debug=False, host='0.0.0.0', port=port)






















# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# from PIL import Image
# import json
# import os

# app = Flask(__name__)
# CORS(app)

# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
# model = genai.GenerativeModel("gemini-1.5-pro")

# @app.route("/ocr", methods=["POST"])
# def ocr():
#     if 'image' not in request.files:
#         return jsonify({"error": "No image uploaded"}), 400

#     image_file = request.files["image"]
#     img_bytes = image_file.read()

#     prompt = "請從圖片中擷取出店名與地址，格式為 JSON：{'店名': '...', '地址': '...'}"

#     response = model.generate_content([
#         prompt,
#         {
#             "inline_data": {
#                 "mime_type": "image/jpeg",
#                 "data": img_bytes
#             }
#         }
#     ])

#     try:
#         extracted = response.text
#         data = extracted.strip().replace("'", '"')
#         return jsonify(json.loads(data))
#     except:
#         return jsonify({"raw": response.text})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)











# import google.generativeai as genai
# import PIL.Image
# import os

# # 設定你的 API 金鑰
# GOOGLE_API_KEY = "AIzaSyBgG0Js0PwIYTRae2-mkPpV1MnDwG_ubE8"
# genai.configure(api_key=GOOGLE_API_KEY)

# # 載入模型 (使用 Gemini 1.5 Pro)
# model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# # 載入圖片
# image_path = r"D:\my_foodmap_app\test3.jpg"  # 替換為你的圖片路徑
# image = PIL.Image.open(image_path)

# # 固定 prompt：要求模型輸出格式化結果
# prompt = """
# 請從這張圖片中擷取「店名」與「地址」，並僅回傳 JSON 格式如下：
# {
#   "店名": "...",
#   "地址": "..."
# }
# 如果圖片中無法辨識出完整的店名或地址，請將欄位留空字串。
# """

# # 執行辨識
# response = model.generate_content([prompt, image])

# # 顯示結果
# print("辨識結果：")
# print(response.text)















from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image
import json
import os
import imghdr

app = Flask(__name__)
CORS(app)

# 初始化 Gemini 模型
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

@app.route("/ocr", methods=["POST"])
def ocr():
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    img_bytes = image_file.read()

    # 嘗試判斷 MIME 類型（jpg / png）
    image_type = imghdr.what(None, h=img_bytes)
    mime_type = f"image/{image_type}" if image_type else "image/jpeg"

    # 更嚴格的 prompt，要求只輸出 JSON，無其他說明
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
    print("Gemini raw response:")
    print(response)
    print("辨識結果：")
    print(response.text)

    # 嘗試解析模型輸出為 JSON
    try:
        extracted = response.text.strip()
        json_data = json.loads(extracted.replace("'", '"'))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({
            "error": "Invalid JSON format",
            "raw": response.text
        })
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)