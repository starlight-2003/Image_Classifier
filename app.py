import os
import numpy as np
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image


# Khởi tạo Flask app
app = Flask(__name__)

# Load model chỉ một lần khi khởi động
model = MobileNetV2(weights='imagenet')


# Hàm dự đoán
def model_predict(img):
    img = img.resize((224, 224))
    x = np.expand_dims(image.img_to_array(img), axis=0)
    x = preprocess_input(x)  # Chỉnh đầu vào theo chuẩn của MobileNetV2

    preds = model.predict(x)
    return decode_predictions(preds, top=1)[0][0]  # Lấy dự đoán cao nhất


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Lấy ảnh từ request
        img_data = request.json
        img = Image.open(img_data)

        # Dự đoán kết quả
        pred_class, _, pred_proba = model_predict(img)

        return jsonify({
            "result": pred_class.replace('_', ' ').capitalize(),
            "probability": "{:.3f}".format(pred_proba)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()