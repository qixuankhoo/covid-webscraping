import csv
import os
import pdfplumber
import nltk
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 

nltk.download('words')
english_words = set(nltk.corpus.words.words())

#threshold = 0.9 # percent of words we want to be actual english


f_map = {}
g_map = {}

WRITE = False


#with open("Louisiana/data/2020-6-20/st_tammany.txt") as f, open("Louisiana/data/2020-07-14/st_tammany.txt") as g:
#with open("test/thing1.txt") as f, open("test/thing2.txt") as g:
#with open("test/black_hawk_06_23.txt") as f, open("test/black_hawk_07_14.txt") as g:
#with open("test/test1.txt") as f, open("test/test2.txt") as g:

STATE = 'Michigan'
COUNTY = 'kalamazoo'
start_date = "2020-06-28"
end_date = "2020-07-15"

start_path = STATE + "/data/" + start_date + "/" + COUNTY + "-PDF/"
end_path = STATE + "/data/" + end_date + "/" + COUNTY + "-PDF/"
'''
start_files = os.listdir(start_path)
for file_name in os.listdir(end_path):
    if file_name not in start_files:
        with pdfplumber.open(end_path + file_name) as f:
            for page in f.pages:
                print(page.extract_text())
'''

with pdfplumber.open("Iowa/data/2020-07-14/woodbury-PDF/050820_Memo_to_Day_Cares.pdf") as f:
    print("hi")

'''

english_count = 0

with pdfplumber.open("Iowa/data/2020-07-14/woodbury-PDF/050820_Memo_to_Day_Cares.pdf") as f:
    for page in f.pages:
        text = page.extract_text()
        words = page.extract_words()
        for word in words:
            if word['text'] in english_words:
                print(word['text'])
                english_count += 1
    print(english_count / len(words))

    print("\n\n")


with open(STATE + "/data/" + start_date + "/" +COUNTY + ".txt") as f, open(STATE + "/data/" + end_date + "/" + COUNTY + ".txt") as g:
    flines = f.readlines()
    glines = g.readlines()

    for i, line in enumerate(flines):
        stripped_line = line.lstrip().rstrip()
        if len(stripped_line) > 4:
            f_map[stripped_line] = 1
    for i, line in enumerate(glines):
        stripped_line = line.lstrip().rstrip()
        if len(stripped_line) > 4:
            g_map[stripped_line] = 1
    
    with open("test/out1.txt", "w") as fout, open("test/out2.txt", "w") as gout:
        fout.write(str(f_map))
        gout.write(str(g_map))
    
    with open('diff_data.csv', 'a', newline='') as csvfile:
        fieldnames = ['category', 'diff_line', 'county']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for line in g_map.keys():
            if line not in f_map:
                print("\n\n" + line)
                if WRITE:
                    writer.writerow({'diff_line' : line, 'county' : COUNTY})
                    
    print("\n\n")
'''