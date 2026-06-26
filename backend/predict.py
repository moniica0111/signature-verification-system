import cv2
import numpy as np
import tensorflow as tf

def abs_distance(tensors):
    return tf.abs(tensors[0] - tensors[1])

# Load trained model
model = tf.keras.models.load_model(
    "model/siamese_signature_model_final.keras",
    compile=False,
    safe_mode=False,
    custom_objects={"abs_distance": abs_distance}
)

# Test Images
img1_path = "testimages/original_1_1.png"
img2_path = "testimages/forgeries_1_1.png"

# Read grayscale
img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

# Resize
img1 = cv2.resize(img1, (224, 224))
img2 = cv2.resize(img2, (224, 224))

# Normalize
img1 = img1.astype("float32") / 255.0
img2 = img2.astype("float32") / 255.0

# Reshape
img1 = img1.reshape(1, 224, 224, 1)
img2 = img2.reshape(1, 224, 224, 1)

# Predict
prediction = model.predict([img1, img2], verbose=0)

score = float(prediction[0][0])

print("\nPrediction Score:", score)

if score >= 0.5:
    print("✅ Genuine Signature")
    print(f"Confidence: {score*100:.2f}%")
else:
    print("❌ Forgery")
    print(f"Confidence: {(1-score)*100:.2f}%")