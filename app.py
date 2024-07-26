from flask import Flask, request, jsonify
from pdfreader import SimplePDFViewer
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/extract-last-page-text', methods=['POST'])
def extract_last_page_text():
    pdf_file = request.files['file']
    pdf_bytes = pdf_file.read()

    viewer = SimplePDFViewer(BytesIO(pdf_bytes))
    last_page_num = len(viewer.pages)
    viewer.navigate(last_page_num)
    
    viewer.render()
    text = "".join(viewer.canvas.strings)

    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
