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


# TASK-3
### # For every profile data (text), find out the most frequent words and essential words used. It shouldn’t contain stop words (like is, the, an, etc.).

# Function : text_preprocessing()

## What does this function do?
### 1. Take in each word from various Profiles texts as input.
### 2. Perform checks if the particular word or character is a punctuation or unwanted symbols and removing them from the corpus. Since they carry very little or Nil information during text analytics.
### 3. Changing the case of all letters in a word to lowerCase this is done to avoid case sensitive issues which should be avoided during text analysis. For ex : boy , BoY, BOy, boY carry same meaning.
### 4. Removing stop-words from the corpus, which means those words which occur very frequently in a text corpus and removing them would not alter the inherent meaning of the text. This is done to achieve better performace from NLP models or easing the computational cost during pre-processing.
### 5. Performing Lemmatization of the words in order to reduce the different forms of the same word to the root word so as to return the base or dictionary form of a word, which is known as the lemma .

nlp = en_core_web_sm.load() # Loading the spacy English Language Model.

def text_preprocessing(word):
    try:
        rem_char = string.punctuation + string.digits # ALl the characters which must be omitted from the word corpus.

        mod_word = '' #Empty string to concatenate with the resultant strings.
        
        for char in word:
            if (char not in rem_char):
                mod_word += char.lower() # Lower Case all the letters of the word.

        docx = nlp(str(mod_word)) # Creating a Doc Object by tokenizing the text.

        if (len(mod_word) == 0 or docx[0].is_stop): # Removing the stopwords (if any)
            return None
        else:
            return docx[0].lemma_ # Perform Lemmatization of the words to reduce down to the root word or dictionary form.
    except:
        print('error') # to handle the odd case of characters like 'x02', etc.


# Function to clean the text-corpus and return the clean text

def clean_profile(profile_desc):    
    prc_description = ''
    for word in profile_desc.split():
        mod_word = text_preprocessing(word)
        if (mod_word is not None): 
            prc_description += (mod_word + ' ')
    return prc_description

# Function : pos_tag(s)
### - This function performs Parts of Speech Tagging of each words in a sentence.
### - This POS tagging is useful when we want to determine the most essential words in a corpus based on their use in the sentence.
### - This function returns the tag of a particular word based on which we can determine the relevancy of tha word in the corpus.

# Function : adj_Noun_words()
### 1. This function is used to determine the most relevant words in a text corpus which in case of a person's professional profile will be the Nouns (Name, Place, Object) and Adjectives. This helps to create a good impression in the recruiter's mind, use of good adjectives is really common for professional profiles like LinkedIN.

def pos_tag(s):
    return nltk.pos_tag(s) # Using nltks's pos_tag module to identify pos of each word in the corpus.

def adj_Noun_words(profile_desc):
    essential_list={}
    token = profile_desc.split()
    pos_token = pos_tag(token) # Obtaining the pos of the particular word.
    for i,tag in pos_token:
        # Checking if the word is of type : Noun or and Adjective.
        if tag in ["JJ","JJR","JJS","N"]:  # JJ, JJR, JJS , N denote Adjectives and Noun
            if i in essential_list: 
                essential_list[i]+=1
            else:
                essential_list[i] = 1
    return list(essential_list.keys()) # Returning the Essential Words


# Function : freq_words()
### - This function finds the most frequently occuring words in the text corpus for each profile. 
### - This helps us to analyse the individual's professional domain, linguistic behavior, professionalism and even past working experiences as well as job preferences.

def freq_words(profile_desc):
    corpus = list(profile_desc.split())
    word_count=dict()
    for word in corpus:
        if word not in word_count.keys():
            word_count[word] = corpus.count(word)
    sorted_word_count = sorted(word_count.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    top_10_words = list() #List to contain top 10 most frequently occuring words in the corpus.
    for kv in sorted_word_count :
        top_10_words.append(kv)
        if len(top_10_words)==10:
            break
    return top_10_words


# TASK-4 (Part-b)
### # The second web API should take text data as input and return the most frequent words and important words (as mentioned in 3) in JSON format.

# Creating the Second WEB-API using FLASK.

## What work will this API establish?

### 1. Read the plain text input file of respective LinkedIn profiles which we converted previously using our very first WEB API.

### 2. Perform the cleaning or text-preprocessing of the each profile text corpus uploaded by the user.

### 3. Determine the Most-Essential words from each of the profile text corpus uploaded by the user and store them.

### 4. Find out the most frequently occuring words from the profile text corpus and store them.

### 5. As a final step, club all the results from multiple input files (or only single) and send as response to the client (user) in the form of .json format.



# Setting the FLASK application framework.
app = Flask(__name__)

# Location to save the uploaded files from the user.
UPLOAD_FOLDER = app.root_path+'/Data/uploads'

app.secret_key = "secret key" #value set for the SECRET_KEY configuration key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #configuring the app to store the uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #Limiting the size of file that the user upolads.


ALLOWED_EXTENSIONS = set(['txt']) #Only PDF files are allowed to be as valid input

def allowed_file(filename): # Function to check if the uploaded file is valid or not.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():# Returns a simple template, provided to upload the files by the user.
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
        NUM=0
        for file in files: # Looping over multiple files (if multiple files are uploaded by user)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # saving the uploaded PDF file to desired location
                
                uploaded_file_path = os.path.join(UPLOAD_FOLDER+ '/'+filename) # Path of stored .txt file
                with open(uploaded_file_path, 'r',encoding='ascii',errors='ignore') as file: # Reading the plain text input file
                    profile_txt = file.read()
                
                profile_txt = clean_profile(profile_txt) # Performing Text-Preprocessing of the profile text corpus
                Essential_Words = adj_Noun_words(profile_txt) # Returns the Most Essential WOrds
                Top_10_words = freq_words(profile_txt) # Returns the most frequently occuring words.
                print(profile_txt)
                print('!!!!!!',Essential_Words)
                NUM+=1
                profile_dict['PROFILE '+str(NUM)+' ESSENTIAL WORDS']= Essential_Words #Storing the results in a dict()
                profile_dict['PROFILE '+str(NUM)+' MOST FREQUENT WORDS']= Top_10_words #Storing frequent words in a dict()
        
        
        return profile_dict # Returning the response a .json
            

if __name__ == "__main__":
    app.run()