from flask import Flask, request, jsonify
from pdfreader import PDFDocument
from io import BytesIO
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/extract-last-page-text', methods=['POST'])
def extract_last_page_text():
    try:
        # Read the PDF file
        pdf_file = request.files['file']
        pdf_bytes = pdf_file.read()

        # Load the PDF document
        with BytesIO(pdf_bytes) as pdf_stream:
            pdf_document = PDFDocument(pdf_stream)
            num_pages = len(pdf_document.pages)
            last_page = pdf_document.pages[num_pages - 1]
            text = last_page.extract_text()

        return jsonify({"text": text})

    except Exception as e:
        logging.error("Error processing PDF: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
