from transformers import MarianMTModel, MarianTokenizer
from PIL import Image, ImageDraw, ImageFont
import pytesseract

# Load MarianMT model and tokenizer
model_name = "Helsinki-NLP/opus-mt-hu-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def ocr_extract_text(image_path):
    """Extract text from an image using Tesseract OCR."""
    return pytesseract.image_to_string(Image.open(image_path), lang="hun")

def translate_text(text):
    """Translate text from Hungarian to English using MarianMT."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import pytesseract

def add_watermark(image_path, translated_text, output_path):
    """Replace Hungarian text with English translation and add a watermark."""
    # Open the original image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Define font (ensure the font file is available)
    font_path = "/Library/Fonts/Arial.ttf"  # Update this path to the correct location
    font = ImageFont.truetype(font_path, size=20)

    # Extract bounding boxes for text regions
    ocr_data = pytesseract.image_to_boxes(Image.open(image_path), lang="hun")
    translated_lines = translated_text.split("\n")

    # Overlay translated text at the corresponding bounding boxes
    for i, line in enumerate(ocr_data.splitlines()):
        if i < len(translated_lines):
            box = line.split()
            x0, y0, x1, y1 = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            
            # Adjust y-coordinates for PIL's coordinate system
            y0 = image.height - y0
            y1 = image.height - y1

            # Ensure y1 is greater than or equal to y0
            if y1 > y0:
                y0, y1 = y1, y0

            # Clear the original text
            draw.rectangle([(x0, y1), (x1, y0)], fill="white")

            # Overlay the translated text
            draw.text((x0, y1), translated_lines[i], fill="black", font=font)

    # Add watermark
    watermark_text = "Translated by MyApp"
    draw.text((image.width - 200, image.height - 50), watermark_text, fill="gray", font=font)

    # Save the output image
    image.save(output_path)