#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
import csv
import os
import sys
import nltk
import pdfplumber
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from datetime import date, timedelta
from send2trash import send2trash


states = ['Washington', 'North Carolina', 'Louisiana', 'Massachusetts', 'Iowa', 'Michigan', 'Colorado']
for days_ago in range(30, 35): # delete original (non-diff) data from 30-35 days ago
    delete_date = str(date.today() - timedelta(days = days_ago))
    for state in states:
        delete_directory = "../" + state + "/data/" + delete_date
        if os.path.isdir(delete_directory):
            print("deleting", delete_directory)
            send2trash(delete_directory)


# detects new sentences for all counties' txt files from start to end date and writes to diff_file_name

initial_date = str(date.today() - timedelta(days = 3))
end_date = str(date.today() - timedelta(days = 1))

diff_file_name = "data/diff_data_" + initial_date + "_" + end_date + ".csv"



i=1

threshold = 0.3 # for english word percentage from pdf, if less then try ocr
english_words = set(nltk.corpus.words.words())

def ocrReadImage(path):
    return str(pytesseract.image_to_string(Image.open(path)))

'''
Read a PDF using OCR.
Returns text and english success rate.
'''
def ocrReadPDF(path):
    head, tail = os.path.split(path)
    if not os.path.isdir(head + "/img"):
        os.mkdir(head + "/img") # make image directory

    pages = convert_from_path(path, 500)
    image_counter = 1
    for page in pages: # convert each page to jpg
        fileName = head + "/img/" + tail[:-4] + "_page_" + str(image_counter) + ".jpg"
        page.save(fileName, 'JPEG')
        image_counter += 1

    ret_text = ""
    english_count = 0
    total_words = 0
    for i in range(1, image_counter):
        fileName = head + "/img/" + tail[:-4] + "_page_" + str(i) + ".jpg"
        text = ocrReadImage(fileName)
        if text:
            text = text.replace('-\n', '')
            ret_text += text
            words = text.split(' ')
            total_words += len(words)
            for word in words:
                if word in english_words:
                    english_count += 1
    
    if total_words == 0:
        total_words = 1
    success_rate = english_count / total_words
    return ret_text, success_rate

'''
Read a PDF normally.
Returns text and english success rate.
'''
def readPDF(path):
    english_count = 0

    ret_text = ""
    total_words = 0

    with pdfplumber.open(path) as f:
        for page in f.pages:
            text = page.extract_text()
            if text:
                ret_text += text
                words = page.extract_words()
                total_words += len(words)
                for word in words:
                    if word['text'] in english_words:
                        english_count += 1
        
    if total_words == 0:
        total_words = 1
    success_rate = english_count / total_words
    return ret_text, success_rate



def writePDFtext(path, state):
    global i
    try:
        text, rate = readPDF(path)
    except:
        print("failed to read PDF")
    else:
        print("successfully reading PDF")
        if rate < threshold:
            try:
                ocrText, ocrRate = ocrReadPDF(path)
            except:
                print("failed to OCR read PDF")
            else:
                if ocrRate > rate:
                    text = ocrText
                    rate = ocrRate

        head, _ = os.path.split(path)

        _, full_county = os.path.split(head)
        county = full_county[:-4]
        
        text = ' '.join(text.split())
        
        with open(diff_file_name, 'a', newline='') as csvfile:
            fieldnames = ['sentence_num', 'diff_line', 'county', 'state']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for sentence in nltk.tokenize.sent_tokenize(text):
                writer.writerow({'sentence_num' : i, 'diff_line' : sentence, 'county' : county, 'state' : state})
                i += 1
            
'''
Writes the PDF text data (every sentence) for *all new* PDFs for a given county (initial_path and end_path are paths to county-PDF directories)
'''
def writeNewCountyPDFs(initial_path, end_path, state):
    initial_files = os.listdir(initial_path)
    for file_name in os.listdir(end_path):
        if file_name not in initial_files and file_name[-4:] == '.pdf': # new (diff) PDF data
            print("new PDF found", end_path + file_name)
            writePDFtext(end_path + "/" + file_name, state)

def writeImageText(path, state):
    global i
    try:
        text = ocrReadImage(path)
    except:
        print("failed to OCR read image")
    else:
        head, _ = os.path.split(path)
        _, full_county = os.path.split(head)
        county = full_county[:-4]

        text = ' '.join(text.split())

        with open(diff_file_name, 'a', newline='') as csvfile:
            fieldnames = ['sentence_num', 'diff_line', 'county', 'state']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for sentence in nltk.tokenize.sent_tokenize(text):
                writer.writerow({'sentence_num' : i, 'diff_line' : sentence, 'county' : county, 'state' : state})
                i += 1

def writeNewCountyImages(initial_path, end_path, state):
    initial_files = os.listdir(initial_path)
    for file_name in os.listdir(end_path):
        if file_name not in initial_files and file_name[-4:] == '.pdf': # new (diff) PDF data
            print("new image found", file_name)
            writeImageText(end_path + "/" + file_name, state)

def writeCountyDiffText(initial_path, end_path, state):
    global i
    _, full_county = os.path.split(end_path)
    county = full_county[:-4]
    f_sentences = set()
    f_text = ""
    g_text = ""
    with open(initial_path) as f, open(end_path) as g:
        f_text = ' '.join(f.read().split())
        g_text = ' '.join(g.read().split()) # replaces all white space with single space

    for sentence in nltk.tokenize.sent_tokenize(f_text):
        f_sentences.add(sentence)

    with open(diff_file_name, 'a', newline='') as csvfile:
        fieldnames = ['sentence_num', 'diff_line', 'county', 'state']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for sentence in nltk.tokenize.sent_tokenize(g_text):
            if sentence not in f_sentences:
                writer.writerow({'sentence_num' : i, 'diff_line' : sentence, 'county' : county, 'state' : state})
                i += 1
                    
with open(diff_file_name, 'w', newline='') as csvfile: # clear file
    fieldnames = ['sentence_num', 'diff_line', 'county', 'state']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    

for state in states:
    initial_path = "../" + state + "/data/" + initial_date + "/"
    end_path = "../" + state + "/data/" + end_date + "/"
    

    if not os.path.isdir(initial_path):
        print("no path for " + state + " for " + initial_date)
        continue

    if not os.path.isdir(end_path):
        print("no path for " + state + " for " + end_date)
        continue

    for curr_file in os.listdir(initial_path):
        if curr_file[-4:] == '.txt':
            writeCountyDiffText(initial_path + curr_file, end_path + curr_file, state)
        elif curr_file[-4:] == '-PDF':
            writeNewCountyPDFs(initial_path + curr_file, end_path + curr_file, state)
        elif curr_file[-6:] == '-image':
            writeNewCountyImages(initial_path + curr_file, end_path + curr_file, state)

