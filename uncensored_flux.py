import os
import requests
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/enhanceaiteam/Flux-uncensored"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def generate_image(prompt):
    image_bytes = query({"inputs": prompt})
    image = Image.open(io.BytesIO(image_bytes))
    return image

def save_image(image, prompt):
    folder_path = "generated_images_folder"
    os.makedirs(folder_path, exist_ok=True)
    image_path = os.path.join(folder_path, f"{prompt.replace(' ', '_')}.png")
    image.save(image_path)
    print(f"Image saved to {image_path}")
    return image_path  # Return the file path
