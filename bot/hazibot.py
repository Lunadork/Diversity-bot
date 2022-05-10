#General imports
import os
import random 
import json
import pickle
import numpy as np

#nltk imports
import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

#tensorflow imports
from tensorflow.keras.models import load_model
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#start the lemmatizer, load our intents
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('./bot/intents.json').read())

#load in words and classes, rb = read binaries
words = pickle.load(open('./bot/words.pkl','rb'))
classes = pickle.load(open('./bot/classes.pkl', 'rb'))
model = load_model('./bot/hazibot_model.h5')

context = []


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
    res = model.predict(np.array([bow]))[0]
    #If uncertainty is greater than this percentage, no match
    ERROR_THRESHOLD = 0.80 
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    #Sort our results to be highest probability first
    results.sort(key=lambda x: x[1], reverse = True)
    return_list = []

    for r in results:
        #add most likely match to return list
        return_list.append({'intent':classes[r[0]], 'probability':str(r[1])})

    print(return_list)

    return return_list



def get_response(predicted_intent, intents_json, context):
    #Get the tag and list of intents


    #If we found no matches on predicted intent, tag = no match, add no_match to context
    if len(predicted_intent) == 0:
        tag = "no_match"
        context.append("no_match")


    #If match was reset_context, set context to empty array
    elif predicted_intent[0]['intent'] == "reset_context":
        tag = "reset_context"
        context = []


    #Anything else, continue as normal, tag is our most likely predicted intent.  populate context
    else:
        tag = predicted_intent[0]['intent']


    list_of_intents = intents_json['intents']
   
   
    #find the right intent tag in our intents.json
    for i in list_of_intents:
        if i['tag'] == tag:
            #pick a random response from the options for that tag
            context.append(i['context'])
            result = { "message" : random.choice(i['responses']), "context" :  context, "expression" : 1 }

            
    #return the response
    return result



def hazibot_generate_response(input):
    predicted_intent = predict_class(input['message'])
    res = get_response(predicted_intent,intents,input['context'])

    # print (res)

    return res

def setup():
    print("Hazi online")

# while True:

#     message = input("")

#     data = {"message" : message, "context" : context}

#     response = hazibot_generate_response(data)

#     print("Hazi: "+response['message'])