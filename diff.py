import csv
import os
import sys
import nltk

# detects new sentences for all counties' txt files from start to end date and writes to diff_data.csv
initial_date = "2020-07-21"
end_date = "2020-08-11"

i=1


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

    with open('diff_data.csv', 'a', newline='') as csvfile:
        fieldnames = ['sentence_num', 'diff_line', 'county', 'state']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for num, sentence in enumerate(nltk.tokenize.sent_tokenize(g_text)):
            if sentence not in f_sentences:
                writer.writerow({'sentence_num' : i, 'diff_line' : sentence, 'county' : county, 'state' : state})
                i += 1
                    
with open('diff_data.csv', 'w', newline='') as csvfile: # clear file
    fieldnames = ['sentence_num', 'diff_line', 'county', 'state']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
states = ['Washington', 'North Carolina', 'Louisiana', 'Massachusetts', 'Iowa', 'Michigan', 'Colorado']

for state in states:
    initial_path = state + "/data/" + initial_date + "/" 
    end_path = state + "/data/" + end_date + "/" 

    if not os.path.isdir(initial_path):
        print("no path for " + state + " for " + initial_date)
        continue

    if not os.path.isdir(end_path):
        print("no path for " + state + " for " + end_date)
        continue

    for curr_file in os.listdir(initial_path):
        if curr_file[-4:] == '.txt':
            writeCountyDiffText(initial_path + curr_file, end_path + curr_file, state)
