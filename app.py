import io
import base64
from flask import Flask, request, jsonify
from pdfminer.high_level import extract_text


app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract():
    try:
        file = request.json.get('file')
        file_data = base64.b64decode(file)
        num_pages = len(pdf_reader.pages)
        
        # Extract last page text
        last_page_text = extract_text(io.BytesIO(file_data), page_numbers=[num_pages - 1])
        
        # Extract questions text from all pages except the last one
        questions_text = extract_text(io.BytesIO(file_data), page_numbers=list(range(num_pages - 1)))
        
        return jsonify({
            'last_page_text': last_page_text,
            'questions_text': questions_text,
            
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
