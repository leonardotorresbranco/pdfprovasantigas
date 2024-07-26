from flask import Flask, request, jsonify
from pdfreader import SimplePDFViewer
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
        pdf_file = request.files['file']
        pdf_bytes = pdf_file.read()

        viewer = SimplePDFViewer(BytesIO(pdf_bytes))
        last_page_num = len(viewer.pages)
        viewer.navigate(last_page_num)
        
        viewer.render()
        text = "".join(viewer.canvas.strings)

        return jsonify({"text": text})

    except Exception as e:
        logging.error("Error processing PDF: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
