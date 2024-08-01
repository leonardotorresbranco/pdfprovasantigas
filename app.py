from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import requests
from PyPDF2 import PdfReader

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

@app.route('/upload-to-blob', methods=['POST'])
def upload_to_blob():
    try:
        data = request.json
        if 'file' not in data:
            return jsonify({'error': 'No file provided'}), 400

        pdf_data = base64.b64decode(data['file'])
        file_name = data.get('filename', 'uploaded_file.pdf')

        blob_url = upload_to_vercel_blob_storage(pdf_data, file_name)
        return jsonify({'url': blob_url})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def upload_to_vercel_blob_storage(file_data, file_name):
    # Implement the actual upload logic here.
    # Placeholder implementation:
    # This function should return the URL of the uploaded file in Vercel Blob Storage
    return f'https://your-vercel-deployment.vercel.app/blob/{file_name}'

if __name__ == '__main__':
    app.run(debug=True)
