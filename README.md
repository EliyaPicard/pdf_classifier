# File Classification and Google Drive Upload

This script provides a web application built with Flask that allows users to upload PDF files, classify them into predefined categories, and upload them to Google Drive. The classification is performed using OpenAI's ChatGPT API, and text extraction from PDFs is done using the PyPDF2 and pdf2image libraries. The uploaded files are saved in a local directory (uploaded_files) before being processed and uploaded to Google Drive.

Prerequisites
Python 3.x
Flask
pytesseract library
google-auth, google-auth-oauthlib, google-auth-httplib2, and google-api-python-client libraries
Installation
Clone the repository or copy the script into your local project directory.
Install the required libraries by running the following command:
Copy code
pip install flask pytesseract google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pdf2image PyPDF2
Configuration
Obtain OpenAI API credentials by signing up on the OpenAI website.
Replace the openai.api_key with your OpenAI API key.
Create a Google Cloud project and enable the Google Drive API. Follow the instructions in the Google Drive API Python Quickstart guide to create the required credentials file (credentials.json).
Replace the credentials.json file path with the path to your own credentials file.
Set up the SCOPES variable according to your needs.
Modify the CLASSES list to match your desired classification categories.
Adjust the UPLOAD_FOLDER variable to specify the folder where uploaded files should be saved.
Usage
Run the script using the following command:
Copy code
python script_name.py
Access the web application by opening your browser and navigating to http://localhost:5000.
Upload a PDF file using the provided form.
The file will be classified into one of the predefined categories using the ChatGPT API.
A folder with the predicted class name will be created in your Google Drive.
The classified file will be uploaded to the corresponding Google Drive folder.
The temporary file will be removed from the local directory.
The result page will display the predicted class.
Additional Notes
This script assumes that the uploaded PDF files are in Hebrew.
If the text extraction from the PDF fails, the script uses OCR (Optical Character Recognition) to extract text from the first page of the PDF.
The classification prompt can be customized by modifying the classify_text function.
The Google Drive folder where the files will be uploaded is specified by the folder ID in the parents field. Modify the create_folder_in_drive and upload_file_to_drive functions to adjust this behavior.
The web application runs in debug mode (debug=True) to provide detailed error messages. Change this value to False for production deployment.
License
This script is released under the MIT License. Feel free to modify and distribute it as needed.
