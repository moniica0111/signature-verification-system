import tensorflow as tf

def abs_distance(tensors):
    return tf.abs(tensors[0] - tensors[1])

model = tf.keras.models.load_model(
    "model/siamese_signature_model_final.keras",
    compile=False,
    safe_mode=False,
    custom_objects={"abs_distance": abs_distance}
)

print("✅ Model Loaded Successfully!")
print("Model Name:", model.name)