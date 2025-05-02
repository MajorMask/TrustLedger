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
def add_watermark(image_path, translated_text, output_path):
    """Reconstruct the document with translated text and add a watermark."""
    # Open the original image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Define font (ensure the font file is available)
    font_path = "/Library/Fonts/Arial.ttf"  # Update this path to the correct location
    font = ImageFont.truetype(font_path, size=20)

    # Overlay translated text
    draw.text((50, 50), translated_text, fill="black", font=font)

    # Add watermark
    watermark_text = "Translated by MyApp"
    draw.text((image.width - 200, image.height - 50), watermark_text, fill="gray", font=font)

    # Save the output image
    image.save(output_path)
# # Example usage
# image_path = "document.jpg"
# output_path = "translated_document.jpg"

# # Step 1: Extract text
# extracted_text = ocr_extract_text(image_path)
# print("Extracted Text:", extracted_text)

# # Step 2: Translate text
# translated_text = translate_text(extracted_text)
# print("Translated Text:", translated_text)

# # Step 3: Reconstruct document with watermark
# add_watermark(image_path, translated_text, output_path)
# print(f"Translated document saved to {output_path}")