from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/extract-last-page-text', methods=['POST'])
def extract_last_page_text():
    try:
        data = request.json
        if 'file' not in data:
            return jsonify({'error': 'No file provided'}), 400

        pdf_data = base64.b64decode(data['file'])
        
        pdf_reader = PdfReader(io.BytesIO(pdf_data))
        num_pages = len(pdf_reader.pages)

        # Extract text from the last page
        last_page = pdf_reader.pages[num_pages - 1]
        last_page_text = last_page.extract_text()
        
        return jsonify({'text': last_page_text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract-questions-text', methods=['POST'])
def extract_questions_text():
    try:
        data = request.json
        if 'file' not in data:
            return jsonify({'error': 'No file provided'}), 400

        pdf_data = base64.b64decode(data['file'])
        
        pdf_reader = PdfReader(io.BytesIO(pdf_data))
        num_pages = len(pdf_reader.pages)

        # Extract text from all pages except the last one
        questions_text = ""
        for page_num in range(num_pages - 1):
            page = pdf_reader.pages[page_num]
            questions_text += page.extract_text() + "\n"
        
        return jsonify({'text': questions_text.strip()})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
