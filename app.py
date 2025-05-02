from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from model import ocr_extract_text, translate_text, add_watermark

from flask import send_from_directory
os.environ[ "TESSDATA_PREFIX"] = "/opt/homebrew/share/tessdata"
# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Define upload folder and allowed extensions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure the upload folder exists

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the frontend."""
    return render_template('index.html')
import logging

logging.basicConfig(level=logging.DEBUG)


@app.route('/process', methods=['POST'])
def process_request():
    try:
        logging.debug("Received a request to process an image.")
        if 'image' not in request.files:
            logging.error("No image file provided.")
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']
        if image_file.filename == '' or not allowed_file(image_file.filename):
            logging.error("Invalid or missing image file.")
            return jsonify({"error": "Invalid or missing image file"}), 400

        image_filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image_file.save(image_path)
        logging.debug(f"Image saved to {image_path}.")

        # Step 1: Extract text using OCR
        extracted_text = ocr_extract_text(image_path)
        logging.debug(f"Extracted text: {extracted_text}")

        # Step 2: Translate text
        translated_text = translate_text(extracted_text)
        logging.debug(f"Translated text: {translated_text}")

        # Step 3: Add watermark
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"translated_{image_filename}")
        add_watermark(image_path, translated_text, output_path)
        logging.debug(f"Watermarked image saved to {output_path}.")

        return jsonify({
            "message": "Processing completed successfully",
            "extracted_text": extracted_text,
            "translated_text": translated_text,
            "output_image": f"/uploads/translated_{image_filename}"
        }), 200
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Serve the uploads folder as static content
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)