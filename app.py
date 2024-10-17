from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import requests
from PyPDF2 import PdfReader
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import safety_settings_pb2


app = Flask(__name__)
CORS(app)

@app.route('/extract-last-page-text', methods=['POST'])
def extract_last_page_text():
    try:
        data = request.json
        if 'file' in data:
            pdf_data = base64.b64decode(data['file'])
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        elif 'url' in data:
            pdf_url = data['url']
            pdf_data = requests.get(pdf_url).content
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        else:
            return jsonify({'error': 'No file or URL provided'}), 400

        num_pages = len(pdf_reader.pages)
        last_page = pdf_reader.pages[num_pages - 1]
        last_page_text = last_page.extract_text()
        
        return jsonify({'text': last_page_text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract-questions-text', methods=['POST'])
def extract_questions_text():
    try:
        data = request.json
        if 'file' in data:
            pdf_data = base64.b64decode(data['file'])
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        elif 'url' in data:
            pdf_url = data['url']
            pdf_data = requests.get(pdf_url).content
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        else:
            return jsonify({'error': 'No file or URL provided'}), 400

        num_pages = len(pdf_reader.pages)
        questions_text = ""
        for page_num in range(num_pages - 1):
            page = pdf_reader.pages[page_num]
            questions_text += page.extract_text() + "\n"
        
        return jsonify({'text': questions_text.strip()})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/extract-all-text', methods=['POST'])
def extract_all_text():
    try:
        data = request.json
        if 'file' in data:
            pdf_data = base64.b64decode(data['file'])
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        elif 'url' in data:
            pdf_url = data['url']
            pdf_data = requests.get(pdf_url).content
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        else:
            return jsonify({'error': 'No file or URL provided'}), 400

        num_pages = len(pdf_reader.pages)
        questions_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            questions_text += page.extract_text() + "\n"
        
        return jsonify({'text': questions_text.strip()})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Parse request JSON for text1 and image1
        req_data = request.get_json()
        text1 = req_data.get("text1", None)
        image1 = req_data.get("image1", None)

        if text1 is None or image1 is None:
            return jsonify({"error": "Missing text1 or image1 in the request"}), 400

        # Initialize Vertex AI
        vertexai.init(project="trim-mariner-438916-b6", location="us-central1")
        model = vertexai.language_models.GenerativeModel(
            "gemini-1.5-flash-002",
        )

        # Set generation configuration
        generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }

        # Define safety settings
        safety_settings = [
            safety_settings_pb2.SafetySetting(
                category=safety_settings_pb2.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=safety_settings_pb2.HarmBlockThreshold.BLOCK_THRESHOLD_OFF
            ),
            safety_settings_pb2.SafetySetting(
                category=safety_settings_pb2.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=safety_settings_pb2.HarmBlockThreshold.BLOCK_THRESHOLD_OFF
            ),
            safety_settings_pb2.SafetySetting(
                category=safety_settings_pb2.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=safety_settings_pb2.HarmBlockThreshold.BLOCK_THRESHOLD_OFF
            ),
            safety_settings_pb2.SafetySetting(
                category=safety_settings_pb2.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=safety_settings_pb2.HarmBlockThreshold.BLOCK_THRESHOLD_OFF
            ),
        ]

        # Generate content
        responses = model.generate_content(
            [text1, image1],
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=True,
        )

        # Combine responses and return them
        output = ""
        for response in responses:
            output += response.text

        return jsonify({"generated_content": output})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
