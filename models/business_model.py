import pandas as pd
import re
import numpy as np

data = pd.read_csv("diff_code_business.csv")
key_words = ["business", "businesses", "occupation", "occupational", "occupancy", "worker", "employer", "employee", "sba", "labor", "farmer", "farm", "customer", "market", "markets", "workplace"]
key_phrases = ["public space"]
predictions = [0] * 800
for index, line in enumerate(data['diff_line']):
    #print("line", line)
    lower_line = str(line).lower()
    words = set(re.findall(r'\w+', lower_line)) # find all words, ignoring punctuation
    singular_words = set()
    for word in words:
        if word[-1] == 's':
            singular_words.add(word[:-1])
    words = words.union(singular_words)
    key_word_found = False
    for key_word in key_words:
        if key_word in words:
            predictions[index] = 1
            key_word_found = True
            break
    if key_word_found:
        continue
    for key_phrase in key_phrases:
        if key_phrase in " ".join(lower_line.split()):
            predictions[index] = 1
            break

data['business_prediction'] = predictions

data['success?'] = np.where(data['business'] == data['business_prediction'], "SUCCESS", "FAIL")
data = data.sort_values(by='success?')
data.to_csv('business_result.csv', index=False)
#print(data)

#with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'max_colwidth', 10000):  # more options can be specified also
#    print(data.loc[~(data['business'] == data['business_prediction'])])
print(data.groupby(["business", "business_prediction"]).size())