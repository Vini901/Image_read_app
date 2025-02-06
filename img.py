import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image
from docx import Document
from io import BytesIO

def extract_text_from_image(image):
    # Convert PIL image to OpenCV format
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    text = pytesseract.image_to_string(gray)  # Extract text
    return text

def save_text_to_word(text):
    doc = Document()
    doc.add_paragraph(text)
    byte_io = BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)
    return byte_io


def main():
    st.title("📷 Image Text Extraction & Word File Converter")
    st.write("Upload an image to extract text and download it as a Word file.")
    
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Extract Text"):
            extracted_text = extract_text_from_image(image)
            st.text_area("Extracted Text", extracted_text, height=200)
            
            if extracted_text.strip():
                word_file = save_text_to_word(extracted_text)
                st.download_button(
                    label="📥 Download Word File",
                    data=word_file,
                    file_name="extracted_text.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            else:
                st.warning("No text detected in the image. Try another image!")

if __name__ == "__main__":
    main()
