from flask import Flask, send_file, jsonify, send_from_directory, request
import os
from generate_video import create_promotional_video

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get data from request
        data = request.json or {}
        theme = data.get('theme', 'divine_blue')
        opening_text = data.get('openingText', 'The Night of Cosmic Awakening...')
        closing_text = data.get('closingText', 'Happy Maha Shivaratri')
        output_format = data.get('format', 'mp4')
        resolution = data.get('resolution', '1080p')
        prompt = data.get('prompt', '')

        # Run the generation script with parameters
        output_filename = f"maha_shivaratri_concept.{output_format}"
        create_promotional_video(
            theme=theme, 
            opening_text=opening_text, 
            closing_text=closing_text, 
            output_format=output_format, 
            resolution=resolution,
            prompt=prompt
        )
        
        if os.path.exists(output_filename):
            return jsonify({"status": "success", "file": output_filename})
        else:
            return jsonify({"status": "error", "message": "File not generated"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('.', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
