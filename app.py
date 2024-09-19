from flask import Flask, request, jsonify
import groq_vision_only as groq
import groq_text_gen_only as groq_text
import uncensored_flux as flux

app = Flask(__name__)

@app.route('/generate_image', methods=['POST'])
def generate_image():
    prompt = request.json.get('prompt')
    image = flux.generate_image(prompt)
    image_path = flux.save_image(image, prompt)
    return jsonify({"image_path": image_path})

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    image_path = request.json.get('image_path')
    analysis = groq.ImageAnalyzer().analyze_image(image_path)
    return jsonify({"analysis": analysis})

@app.route('/generate_text', methods=['POST'])
def generate_text():
    prompt = request.json.get('prompt')
    history = request.json.get('history', [])
    response, history = groq_text.generate_text(prompt, history)
    return jsonify({"response": response, "history": history})

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)