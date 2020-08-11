import pandas as pd
import re
import numpy as np

data = pd.read_csv("../diff_data.csv")
key_words = ["mask", "gown", "ppe", "n95", "facecovering", "face-mask", "face-covering", "face-shield", "facial-covering", "facial-shield", "face-cloth", "facial-cloth", "personal-protective-equipment", "cloth-covering"]
key_phrases = ["face covering", "cloth covering", "personal protective equipment", "face shield", "facial covering", "facial shield", "face cloth", "facial cloth"]
predictions = ["No"] * len(data)
for index, line in enumerate(data['diff_line']):
    lower_line = line.lower()
    words = set(re.findall(r'\w+', lower_line)) # find all words, ignoring punctuation
    singular_words = set()
    for word in words:
        if word[-1] == 's':
            singular_words.add(word[:-1])
    words = words.union(singular_words)
    key_word_found = False
    for key_word in key_words:
        if key_word in words:
            predictions[index] = "Yes"
            key_word_found = True
            break
    if key_word_found:
        continue
    for key_phrase in key_phrases:
        if key_phrase in " ".join(lower_line.split()):
            predictions[index] = "Yes"
            break

data['facemask_prediction'] = predictions
data = data[data['facemask_prediction'] == "Yes"]

#data['success?'] = np.where(data['facemask'] == data['facemask_prediction'], "SUCCESS", "FAIL")
#data = data.sort_values(by='success?')
data.to_csv('mask_result.csv', index=False)
#print(data)


#with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'max_colwidth', 10000):  # more options can be specified also
#    print(data.loc[~(data['facemask'] == data['facemask_prediction'])])
#print(data.groupby(["facemask", "facemask_prediction"]).size()
