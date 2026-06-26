from flask_cors import CORS
from flask import Flask, request, jsonify
import tensorflow as tf
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app)

def abs_distance(tensors):
    return tf.abs(tensors[0] - tensors[1])

model = tf.keras.models.load_model(
    "model/siamese_signature_model_final.keras",
    compile=False,
    safe_mode=False,
    custom_objects={"abs_distance": abs_distance}
)

def preprocess(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (224, 224))
    img = img.astype("float32") / 255.0
    img = img.reshape(1, 224, 224, 1)
    return img

@app.route("/")
def home():
    return "Signature Verification Backend Running!"

@app.route("/verify", methods=["POST"])
def verify():

    image1 = request.files["image1"]
    image2 = request.files["image2"]

    path1 = "temp1.png"
    path2 = "temp2.png"

    image1.save(path1)
    image2.save(path2)

    img1 = preprocess(path1)
    img2 = preprocess(path2)

    prediction = model.predict([img1, img2], verbose=0)

    score = float(prediction[0][0])

    os.remove(path1)
    os.remove(path2)

    if score >= 0.5:
        result = "Genuine Signature"
    else:
        result = "Forgery"

    return jsonify({
        "prediction_score": round(score, 4),
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)