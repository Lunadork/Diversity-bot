#General imports
from distutils.log import ERROR
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

#process the cleaned up sentence into words and convert to numpy array of 1's and 0's based on pattern matching to words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] *len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array(bow))[0]
    #If uncertainty is greater than this percentage, no match
    ERROR_THRESHOLD = 0.25 
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    #Sort our results to be highest probability first
    results.sort(key=lambda x: x[1], reverse = True)
    return_list = []

    for r in results:
        #add most likely match to return list
        return_list.append({'intent':classes[r[0]], 'probability':str(r[1])})

    return return_list

def get_response(intents_list, intents_json):
    #Get the tag and list of intents
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    #find the right intent tag
    for i in list_of_intents:
        if i['tag'] == tag:
            #pick a random response from the options
            result = random.choice(i['responses'])
    #return the response
    return result

print("Hazi should be online")