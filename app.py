from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

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
        
        if last_page_text is None:
            return jsonify({'error': 'No text found on the last page'}), 500
        
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
        questions = []
        for page_num in range(num_pages - 1):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                questions.extend(parse_questions(page_text))
        
        return jsonify({'questions': questions})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_questions(text):
    questions = []
    lines = text.split("\n")
    question = None

    for line in lines:
        if line.strip().isdigit():
            if question:
                questions.append(question)
            question = {"number": line.strip(), "text": ""}
        elif question:
            question["text"] += line + " "

    if question:
        questions.append(question)

    return questions

if __name__ == '__main__':
    app.run(debug=True)
