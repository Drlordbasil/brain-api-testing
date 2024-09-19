import os
import base64
import requests
from groq import Groq

class ImageAnalyzer:
    def __init__(self, model="llava-v1.5-7b-4096-preview"):
        self.client = Groq()
        self.model = model

    def analyze_image(self, image_source):
        if self._is_url(image_source):
            image_content = self._get_image_from_url(image_source)
        else:
            image_content = self._encode_local_image(image_source)

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_content,
                            },
                        },
                    ],
                }
            ],
            model=self.model,
        )

        return chat_completion.choices[0].message.content

    def _is_url(self, path):
        return path.startswith('http://') or path.startswith('https://')

    def _get_image_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return url
        except requests.RequestException as e:
            raise ValueError(f"Invalid image URL: {e}")

    def _encode_local_image(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Local file {path} not found.")
        
        with open(path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        return f"data:image/jpeg;base64,{base64_image}"

if __name__ == "__main__":
    analyzer = ImageAnalyzer()
    # Test with a local image
    local_image_path = "C:\\Users\\drlor\\OneDrive\\Desktop\\generated_images_folder\\Astronaut_riding_a_horse.png"
    print(analyzer.analyze_image(local_image_path))
    # Test with a URL image
    url_image = "https://politizoom.com/wp-content/uploads/2024/08/Screenshot-2024-08-16-113616.png"
    try:
        print(analyzer.analyze_image(url_image))
    except ValueError as e:
        print(e)