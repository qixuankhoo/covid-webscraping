import pandas as pd
import re
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
import textblob, string
#from keras.preprocessing import text, sequence
#from keras import layers, models, optimizers

def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)
    
    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)
    
    if is_neural_net:
        predictions = predictions.argmax(axis=-1)
    
    return metrics.accuracy_score(predictions, valid_y)

data = pd.read_csv("diff_code_business.csv")

data = data.dropna()

train_x, valid_x, train_y, valid_y = model_selection.train_test_split(data['diff_line'], data['business']) # training is random 75% of data, testing is other 25%

encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(data['diff_line'])

# looking at different feature vectors

# straight word frequencies (count vectors)
xtrain_count = count_vect.transform(train_x) 
xvalid_count = count_vect.transform(valid_x)

# tf-idf 
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(data['diff_line'])
xtrain_tfidf = tfidf_vect.transform(train_x)
xvalid_tfidf = tfidf_vect.transform(valid_x)




accuracy = train_model(linear_model.LogisticRegression(), xtrain_count, train_y, xvalid_count)
print('Accuracy: ', accuracy)