from bs4 import BeautifulSoup
import requests

#Ectracting text from url or website
def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lst = [p.text for p in soup.find_all('h2')]
    return ' '.join(lst)

import pdfplumber
from PIL import Image

#Ectracting text from pdf file
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

#extracting text from image file
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" # OCR ENGINE 

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text
