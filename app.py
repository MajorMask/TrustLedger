from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from model import ocr_extract_text, translate_text, add_watermark, create_translated_image
from pdf2image import convert_from_path

from flask import send_from_directory
os.environ[ "TESSDATA_PREFIX"] = "/opt/homebrew/share/tessdata"
# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Define upload folder and allowed extensions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
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
        logging.debug("Received a request to process an image or PDF.")
        if 'image' not in request.files:
            logging.error("No file provided.")
            return jsonify({"error": "No file provided"}), 400

        file = request.files['image']
        if file.filename == '' or not allowed_file(file.filename):
            logging.error("Invalid or missing file.")
            return jsonify({"error": "Invalid or missing file"}), 400

        file_filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_filename)
        file.save(file_path)
        logging.debug(f"File saved to {file_path}.")

        # Check if the file is a PDF
        if file_filename.lower().endswith('.pdf'):
            logging.debug("Processing PDF file.")
            # Convert PDF pages to images
            pages = convert_from_path(file_path)
            extracted_text = ""
            for i, page in enumerate(pages):
                page_path = os.path.join(app.config['UPLOAD_FOLDER'], f"page_{i + 1}.jpg")
                page.save(page_path, 'JPEG')
                logging.debug(f"Page {i + 1} saved as image: {page_path}")
                extracted_text += ocr_extract_text(page_path) + "\n"
        else:
            # Process image file
            extracted_text = ocr_extract_text(file_path)

        logging.debug(f"Extracted text: {extracted_text}")

        # Step 2: Translate text
        translated_text = translate_text(extracted_text)
        logging.debug(f"Translated text: {translated_text}")

        # Step 3: Add watermark (if it's an image)
        if not file_filename.lower().endswith('.pdf'):
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"translated_{file_filename}")
            add_watermark(file_path, translated_text, output_path)
            logging.debug(f"Watermarked image saved to {output_path}.")
            output_image_url = f"/uploads/translated_{file_filename}"
        else:
            output_image_url = None

        # Step 4: Create a new image with the translated text
        output_text_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"text_only_{file_filename}.jpg")
        create_translated_image(translated_text, output_text_image_path)
        logging.debug(f"Translated text image saved to {output_text_image_path}.")

        return jsonify({
            "message": "Processing completed successfully",
            "extracted_text": extracted_text,
            "translated_text": translated_text,
            "output_image": output_image_url,
            "text_image": f"/uploads/text_only_{file_filename}.jpg"
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