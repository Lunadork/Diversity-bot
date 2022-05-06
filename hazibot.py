#General imports
import random 
import json
import pickle
import numpy as np

#nltk imports
import nltk
from nltk.stem import WordNetLemmatizer

#tensorflow imports
from tensorflow.keras.models import load_model

#start the lemmatizer, load our intents
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

#load in words and classes, rb = read binaries
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('hazibot_model.model')


#Sentence cleaner, takes a sentence, lemmatizes it into individual words and returns the lemmatized words
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

