from flask import Flask, request, jsonify
import PyPDF2
from io import BytesIO
from werkzeug.utils import secure_filename
import re
from PIL import Image
import base64

app = Flask(__name__)

def extract_text_and_images(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    
    text = ""
    images = []
    parsed_data = []

    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]
        text += page.extract_text()

        # Extracting images
        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].get_object()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    image = xObject[obj]
                    size = (image['/Width'], image['/Height'])
                    data = image.get_data()
                    
                    if image['/ColorSpace'] == '/DeviceRGB':
                        mode = "RGB"
                    else:
                        mode = "P"
                    
                    img = Image.frombytes(mode, size, data)
                    img_byte_arr = BytesIO()
                    img.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
                    
                    images.append({
                        "page": page_number + 1,
                        "image": img_base64
                    })

    # Split text into questions and parse accordingly
    questions = re.split(r'\d+\)', text)
    for idx, question in enumerate(questions):
        if idx == 0:
            continue  # Skip the first split as it's before the first question
        question_text = re.search(r'([\s\S]+?)(?:\nA\)|\nB\)|\nC\)|\nD\)|\nE\))', question)
        if question_text:
            question_text = question_text.group(0)
        else:
            question_text = question.strip()
        
        parsed_data.append({
            "question_number": idx,
            "question_text": question_text
        })

    return parsed_data, images

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        pdf_file = BytesIO(file.read())

        parsed_data, images = extract_text_and_images(pdf_file)
        return jsonify({"questions": parsed_data, "images": images})

if __name__ == '__main__':
    app.run(debug=True)
