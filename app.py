import io
import base64
from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBox, LTImage
import re

app = Flask(__name__)

def extract_images_from_page(page):
    images = []
    if '/Resources' in page:
        resources = page['/Resources']
        if '/XObject' in resources:
            xObject = resources['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    image_data = xObject[obj]._data
                    images.append(base64.b64encode(image_data).decode('utf-8'))
    return images

@app.route('/extract', methods=['POST'])
def extract():
    try:
        file = request.json.get('file')
        file_data = base64.b64decode(file)
        pdf_reader = PdfReader(io.BytesIO(file_data))
        num_pages = len(pdf_reader.pages)
        
        # Extract last page text
        last_page = pdf_reader.pages[-1]
        last_page_text = extract_text(io.BytesIO(file_data), page_numbers=[num_pages - 1])
        
        # Extract questions text from all pages except the last one
        questions_text = extract_text(io.BytesIO(file_data), page_numbers=list(range(num_pages - 1)))
        
        # Extract images from all pages
        images = []
        for i in range(num_pages):
            page = pdf_reader.pages[i]
            page_images = extract_images_from_page(page)
            for img in page_images:
                images.append({'page': i + 1, 'image': img})
        
        return jsonify({
            'last_page_text': last_page_text,
            'questions_text': questions_text,
            'images': images
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
