import requests
from PIL import Image
import io

BASE_URL = "http://127.0.0.1:5000"

def test_generate_image(prompt):
    url = f"{BASE_URL}/generate_image"
    payload = {"prompt": prompt}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Image generated successfully.")
        image_path = response.json()["image_path"]
        return image_path
    else:
        print("Failed to generate image.")
        print(response.text)
        return None

def open_image(image_path):
    try:
        image = Image.open(image_path)
        image.show()
        print(f"Image opened: {image_path}")
    except Exception as e:
        print(f"Failed to open image: {e}")

def main():
    prompt = "A beautiful landscape with a river and mountains"
    
    # Test image generation
    image_path = test_generate_image(prompt)
    if not image_path:
        return
    
    # Open the generated image
    open_image(image_path)

if __name__ == "__main__":
    main()