import os
from flask import Flask, render_template, request
import openai
import glob
import pytesseract
from googleapiclient.http import MediaFileUpload
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from google.oauth2 import service_account
from googleapiclient.discovery import build

CLASSES = ['מילואים', 'אישור מחלה', 'קורות חיים']
API_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
UPLOAD_FOLDER = 'uploaded_files'
SCOPES = ['https://www.googleapis.com/auth/drive']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load Google Drive credentials
credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    # Get the uploaded file from the request
    file = request.files['file']

    # Save the file to the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.pdf')
    file.save(file_path)

    # Classify the file
    predicted_class = classify_file(file_path)
    classification = predicted_class.split("Classification:")[-1].strip()
    file_name = predicted_class.split("Sender:")[-1].split("Recipient:")[0].strip()

    # Create a folder in Google Drive with the predicted class name

    # Upload the file to Google Drive
    upload_file_to_drive(file_path, classification, file_name)

    # Remove the temporary file
    os.remove(file_path)

    return render_template('result1.html', predicted_class=predicted_class)

def extract_text_from_pdf(file_path, password='0545951589'):
    try:
        # Attempt to extract text using the first method
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            if pdf_reader.is_encrypted:
                pdf_reader.decrypt(password)  # Provide the password
            first_page = pdf_reader.pages[0]  # Access the first page of the PDF
            text = first_page.extract_text()

        # If no text is extracted, try the second method
        if not text or len(text) < 100:
            # Convert the first page of the image-based PDF to a PIL Image object
            images = convert_from_path(file_path, first_page=1, last_page=2)
            first_image = images[0]  # Access the first image/page

            # Extract text from the first image/page using pytesseract
            text = pytesseract.image_to_string(first_image, lang='heb')

        return text

    except Exception as e:
        # If no text is extracted, try the second method

        # Convert the first page of the image-based PDF to a PIL Image object
        images = convert_from_path(file_path, first_page=1, last_page=2)
        first_image = images[0]  # Access the first image/page

        # Extract text from the first image/page using pytesseract
        text = pytesseract.image_to_string(first_image, lang='heb')

        return text

def classify_text(text):
    openai.api_key = "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"
    prompt = f'''
        Please write the year in which the text below was written,
        the name of the company that sent the file,
        the recipient of the file,
        and classify the text into one of the following categories:
        University, Job, Car Insurance, Health Insurance, Medical Topic,
        Salary, Wedding, Electricity Bill,
        Military Service, CV.

        Text: {text}

        Year:

        Sender:

        Recipient:

        Classification:
    '''

    # Send the prompt to the ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a user."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the classification from the ChatGPT response
    predicted_class = response.choices[0].message.content
    return predicted_class

def classify_file(file_path):
    text = extract_text_from_pdf(file_path)
    predicted_class = classify_text(text)
    return predicted_class

def create_folder_in_drive(folder_name):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': ['1gMJob3Y2Bwh5FW2hPdllTt_QHChndvs_']
    }
    drive_service.files().create(body=folder_metadata).execute()

def upload_file_to_drive(file_path, folder_name, file_name):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': ['1gMJob3Y2Bwh5FW2hPdllTt_QHChndvs_']
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()

    file_metadata = {
        'name': file_name,
        'parents': [folder.get('id')]
    }
    media = MediaFileUpload(file_path)
    drive_service.files().create(body=file_metadata, media_body=media).execute()


def get_folder_id_by_name(folder_name):
    response = drive_service.files().list(q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='files(id)',
                                          pageToken=None).execute()
    folders = response.get('files', [])
    if len(folders) == 1:
        return folders[0]['id']
    return None

if __name__ == '__main__':
    app.run(debug=True)
