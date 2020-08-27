# AICHAMP SCREENING TEST

## Submitted by - Sudarshan Paul
## Total Tasks Completed - 4
## Contact - 7908468882
## E-Mail - paulsudarshan98@gmail.com


# TASK-1
### Download 50 public profile PDFs of your connections (randomly) from LinkedIn.

# pip install --user pdfminer
# !pip install --user werkzeug

# Importing the required libraries.

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter # Converting PDF to text
from pdfminer.converter import TextConverter  # utils for pdf conversion
from pdfminer.layout import LAParams  # utils for pdf conversion
from pdfminer.pdfpage import PDFPage  # utils for pdf conversion
from io import StringIO,BytesIO # utils for pdf conversion
import os

from flask import Flask # For FLASK API Development
from flask import Flask, flash, request, redirect, render_template # Utils for API development
from werkzeug.utils import secure_filename # function to secure a filename before storing it directly on the filesystem.
import urllib.request


import spacy  #Required for Profile Text Analysis ex : stop words removal, text cleaning etc
import pandas as pd #Required for structuring the data in the form of a DataFrame
import en_core_web_sm # This is the largest English Library for Spacy
import string #Required for string manipulation
import nltk # Also required for text analysis

# Function to Convert PDF ---> .txt

# Task -2
### # Extract text from the above PDFs and store them in a CSV.

def convertPDFToText(path):
    rsrcmgr = PDFResourceManager() # Create a PDF resource manager object that stores shared resources.
    retstr = StringIO() # Create instance of StringIO
    laparams = LAParams() # Set parameters for analysis.
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb') #Opening the PDF file in the respective path.
    interpreter = PDFPageInterpreter(rsrcmgr, device) #Creating an instance of PDFPageInterpreter
    password = "" #In case PDF is password protected
    maxpages = 0 
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page) 
    fp.close() # Closing the existing open file for security reasons.
    device.close()
    string = retstr.getvalue() #Obtaining all the text values from the PDF after parsing is over
    retstr.close() #Terminating the instance of StringIO
    return string # Returning the string values in plain text format

# convertPDFToText('C://Users//sudar//OneDrive//Desktop//Work Files//AI CHamp//Data//Profile (1).pdf')

# TASK-4 (Part a) and TASK-2 (Put together in single API)
### # The first web API should take a PDF file as input and return the text in it in JSON format.

# Creating the First WEB-API using FLASK.

## What is Flask?
### Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.

## What works will this simple API establish?

### 1. Take the PDF file as input from the user.
### 2. Perform validation checks if the input file is as per mentioned format.
### 3. Save the PDF file in the desired location.
### 4. Call the function convertPDFToText() defined above and convert the PDF data to plain text format.
### 5. Once the data has been converted to plan text (string) then writing the same data to a file.txt ex- Profile_1.txt
### 6. Storing the multiple converted text files as a Pandas DataFrame and exporting the dataframe to CSV format and saving in the desired location.
### 7. Returning the PDF Profiles as .json format as a response from the Web API.

# profile_df=pd.DataFrame() # Empty DataFrame to store the profile texts.

# Setting the FLASK application framework.
app = Flask(__name__)
# Location to save the uploaded files from the user.
UPLOAD_FOLDER = app.root_path+'/Data/uploads'

app.secret_key = "secret key" #value set for the SECRET_KEY configuration key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configuring the app to store the uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #Limiting the size of file that the user upolads.

ALLOWED_EXTENSIONS = set(['pdf']) #Only PDF files are allowed to be as valid input

def allowed_file(filename): # Function to check if the uploaded file is valid or not.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form(): # Returns a simple template, provided to upload the files by the user.
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    global profile_df
    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files: 
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        profile_dict={} # Empty dictionary to store profile details with respective profiles names.
        for file in files: # Looping over multiple files (if multiple files are uploaded by user)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename) 
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # saving the uploaded PDF file to desired location
                
                uploaded_file_path = os.path.join(UPLOAD_FOLDER+ '/'+filename) # Path of stored PDF file
                stringFormat = convertPDFToText(uploaded_file_path) # Passing the path for the PDF file in the function to convert to plain text.
                
                # Writing the plain text values (string) obtained after parsing the pdf to external text files.
                with open(app.root_path+'/Data/uploads/converted/'+filename+'.txt', 'w', encoding='utf-8') as file_txt: 
                    file_txt.write(stringFormat) 
                    file_txt.close()
                
                profile_dict[filename]=stringFormat #storing the profile details as key-value pairs.
                
        # Creating a single DataFrame of all the profiles with their respective Profile Numbers as indexes.        
        # profile_df = pd.DataFrame.from_dict(profile_dict,orient='index',columns=['Profiles'])
        
        # Exporting the created Profiles DataFrame to Excel Format
        # profile_df.to_csv(app.root_path+'/Data/uploads/ProfileCSV/ProfilesCSV.csv')
        
        flash('File(s) successfully uploaded')
        
        # Finally sending the response in .json format to the client (user).
        return profile_dict

if __name__ == "__main__":
    app.run()