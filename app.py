from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import requests
from PyPDF2 import PdfReader
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from google.cloud import aiplatform
import os
import json
from google.oauth2 import service_account
import logging
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Decode the credentials from environment variable
credentials_base64 = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_BASE64")
if credentials_base64 is None:
    logging.error("Missing GOOGLE_APPLICATION_CREDENTIALS_BASE64 environment variable.")
    raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS_BASE64 environment variable.")

try:
    credentials_json = base64.b64decode(credentials_base64)
    credentials_info = json.loads(credentials_json)
    # Use the credentials to authenticate
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    logging.info("Google Cloud credentials loaded successfully.")
except Exception as e:
    logging.error(f"Error loading Google Cloud credentials: {e}")
    raise

# Initialize Vertex AI
try:
    vertexai.init(
        project="stone-bison-438919-h8",
        location="us-central1",
        credentials=credentials
    )
    logging.info("Vertex AI initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing Vertex AI: {e}")
    raise

app = Flask(__name__)
CORS(app)

@app.route('/extract-last-page-text', methods=['POST'])
def extract_last_page_text():
    try:
        logging.debug("Received request for /extract-last-page-text")
        data = request.json
        if 'file' in data:
            logging.debug("Decoding base64 file data")
            pdf_data = base64.b64decode(data['file'])
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        elif 'url' in data:
            logging.debug(f"Fetching PDF from URL: {data['url']}")
            pdf_url = data['url']
            pdf_data = requests.get(pdf_url).content
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        else:
            logging.error("No file or URL provided in request")
            return jsonify({'error': 'No file or URL provided'}), 400

        num_pages = len(pdf_reader.pages)
        last_page = pdf_reader.pages[num_pages - 1]
        last_page_text = last_page.extract_text()
        
        logging.debug("Extracted text from the last page successfully")
        return jsonify({'text': last_page_text})

    except Exception as e:
        logging.error(f"Error extracting last page text: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/extract-questions-text', methods=['POST'])
def extract_questions_text():
    try:
        logging.debug("Received request for /extract-questions-text")
        data = request.json
        if 'file' in data:
            logging.debug("Decoding base64 file data")
            pdf_data = base64.b64decode(data['file'])
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        elif 'url' in data:
            logging.debug(f"Fetching PDF from URL: {data['url']}")
            pdf_url = data['url']
            pdf_data = requests.get(pdf_url).content
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        else:
            logging.error("No file or URL provided in request")
            return jsonify({'error': 'No file or URL provided'}), 400

        num_pages = len(pdf_reader.pages)
        questions_text = ""
        for page_num in range(num_pages - 1):
            page = pdf_reader.pages[page_num]
            questions_text += page.extract_text() + "\n"
        
        logging.debug("Extracted text from all pages except the last page successfully")
        return jsonify({'text': questions_text.strip()})

    except Exception as e:
        logging.error(f"Error extracting questions text: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/extract-all-text', methods=['POST'])
def extract_all_text():
    try:
        logging.debug("Received request for /extract-all-text")
        data = request.json
        if 'file' in data:
            logging.debug("Decoding base64 file data")
            pdf_data = base64.b64decode(data['file'])
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        elif 'url' in data:
            logging.debug(f"Fetching PDF from URL: {data['url']}")
            pdf_url = data['url']
            pdf_data = requests.get(pdf_url).content
            pdf_reader = PdfReader(io.BytesIO(pdf_data))
        else:
            logging.error("No file or URL provided in request")
            return jsonify({'error': 'No file or URL provided'}), 400

        num_pages = len(pdf_reader.pages)
        questions_text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            questions_text += page.extract_text() + "\n"

        logging.debug("Extracted text from all pages successfully")
        return jsonify({'text': questions_text.strip()})

    except Exception as e:
        logging.error(f"Error extracting all text: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        logging.debug("Received request for /generate")
        
        # Parse request JSON for text1 and image1
        req_data = request.get_json()
        logging.debug(f"Request data: {req_data}")

        text1 = req_data.get("text1", None)
        image1 = req_data.get("image1", None)
        
        if text1 is None or image1 is None:
            logging.error("Missing text1 or image1 in the request")
            return jsonify({"error": "Missing text1 or image1 in the request"}), 400

        # Set generation configuration
        generation_config = {
            "max_output_tokens": 1024,
            "temperature": 1,
            "top_p": 0.95,
        }

        # Load the model using the updated approach
        logging.debug("Loading model for generation")
        model = GenerativeModel("gemini-1.5-flash-002")

        # Generate content using generate_content() method
        logging.debug("Generating content")
        responses = model.generate_content(
            [text1, image1],
            generation_config=generation_config,
            stream=True  # Using streaming responses
        )
        
        # Combine responses from the generator
        output = ""
        for response in responses:
            output += response.text

        logging.debug("Content generated successfully")
        return jsonify({"generated_content": output})

    except Exception as e:
        logging.error(f"Error during generation: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
