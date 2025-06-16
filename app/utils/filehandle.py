import os
from datetime import datetime

def save_image(image_data):
    image_dir = '/openfabric/app/outputs/images'
    os.makedirs(image_dir, exist_ok=True)
    path = f"{image_dir}/image_{int(datetime.utcnow().timestamp())}.png"
    with open(path, "wb") as f:
        f.write(image_data)
    return path

def save_model(model_data):
    model_dir = '/openfabric/app/outputs/models'
    os.makedirs(model_dir, exist_ok=True)
    path = f"{model_dir}/model_{int(datetime.utcnow().timestamp())}.glb"
    with open(path, "wb") as f:
        f.write(model_data)
    return path
