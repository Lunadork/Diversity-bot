#General imports
import os
import random 
import json
import pickle
import numpy as np
import dbqueries as db
import asyncio

#nltk imports
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
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

context = ["Start"]


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
    ERROR_THRESHOLD = 0.50 
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    #Sort our results to be highest probability first
    results.sort(key=lambda x: x[1], reverse = True)
    return_list = []

    for r in results:
        #add most likely match to return list
        return_list.append({'intent':classes[r[0]], 'probability':str(r[1])})

    print(return_list)

    return return_list



def get_response(predicted_intent, intents_json, context, username,task = 'not_set'):

    #if predicted_intent is a string we've overrode AI interpretation due to conversation context flow, tag = predicted_intent
    if isinstance(predicted_intent, str):
        tag = predicted_intent
      

    #If we found no matches on predicted intent, tag = no match, add no_match to context
    elif len(predicted_intent) == 0:
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
            choice = random.choice(i['responses'])

            if bool(task) == False:
                task = 'nothing'

            if db.check_if_new(username) == False:
                username = db.get_preferred_name(username)
                message = choice.replace("[username]",username+"").replace("[task]",task+"")
                result = { "message" : message, "context" :  context, "expression" : 1 } 
                #return the response
                return result
            elif db.check_if_new(username) == True:
                result = { "message" : message, "context" :  context, "expression" : 1 }
                return result

            message = choice.replace("[username]",username+"").replace("[task]",task+"")
            result = { "message" : message, "context" :  context, "expression" : 1 }
            return result



async def hazibot_generate_response(input):

    predicted_intent = predict_class(input['message'].lower())

    username = ""

    is_new = await db.check_if_new(input['username'])
    if is_new == False:
        print("isn'tnew")
        username = await db.get_preferred_name(input['username'])
    elif is_new == True:
        print("isnew")
        username = input['username']

    #If last entry in context is "Start", it's a new convo, do the startup procedure
    if input['context'][ len(input['context'])-1 ] == "Start":
        #Check if the user is new
        is_new = await db.check_if_new(input['username'])
        #if is new start the new user procedure
        if is_new == True:
            
            ##user is new, get their preferred name and add to db.
            predicted_intent = "get_user_preferred_name"
            res = get_response(predicted_intent,intents,input['context'],username)
            return res

        else:         
            #Check if if task exists
            task = await db.check_if_has_task(input['username'])
            print("tsk")
            print(task)
            #if task isn't false, there's a task, ask if user done task
            if task != False:
                predicted_intent = "start_check_task"
                res = get_response(predicted_intent,intents,input['context'],username,task)
                return res
            #No task, resume normal flow
            else:
                res = get_response(predicted_intent,intents,input['context'],username,task)
                return res

    #last context was "get_user_preferred_name" > "Start" -> user has been asked for their preferred name.        
    elif input['context'][ len(input['context'])-1 ] == "get_user_preferred_name" and input['context'][ len(input['context'])-2 ] == "Start":
        name = input['message']
        await db.add_user(input['username'],name)
        predicted_intent = "got_user_preferred_name"
        res = get_response(predicted_intent,intents,input['context'],username)
        return res
    
    #If last entry in context is "check_task" the user has been asked to, get predicted intent - if it's agree - user did it.  if disagree - user did not
    elif input['context'][ len(input['context'])-1 ] == "check_task": #or input['context'][ len(input['context'])-1 ] == "start_check_task":
        predicted_intent = predict_class(input['message'])

        ##if user did the task
        if predicted_intent[0]['intent'] == "agree":
            predicted_intent = "task_done"
            res=get_response(predicted_intent, intents,input['context'], username)
            await db.set_task_done(username)
            return res

        #if user didn't do the task
        if predicted_intent[0]['intent'] == "disagree":
            predicted_intent = "task_not_done"
            res=get_response(predicted_intent,intents,input['context'],username)
            return res


    #If user wants to change the task - last context agree, previous context disagree, context before check_task
    elif input['context'][ len(input['context'])-1 ] == "agree" or input['context'][ len(input['context'])-1 ] == "user_agree" and input['context'][ len(input['context'])-2 ] == "disagree" and input['context'][ len(input['context'])-3 ] == "check_task":
        predicted_intent = "stop_task"
        await db.stop_task(username)
        res = get_response(predicted_intent,intents,input['context'],username)
        return res

    #if last context was agree and context before that was agree, then before that depression resources, user agreed to hear about task
    elif input['context'][ len(input['context'])-1 ] == "agree" and input['context'][ len(input['context'])-2 ] == "agree" and input['context'][ len(input['context'])-3 ] == "depression_resources":
        predicted_intent = "cbt_info"
        res = get_response(predicted_intent,intents,input['context'],username)
        return res

    #if last context was agree or agree_cbt > agree > agree > depression resources, user agreed to cbt task
    elif input['context'][ len(input['context'])-1 ] == "agree" or input['context'][ len(input['context'])-1 ] == "agree_cbt"  and input['context'][ len(input['context'])-2 ] == "agree" and input['context'][ len(input['context'])-3 ] == "agree" and input['context'][ len(input['context'])-4 ] == "depression_resources":
        predicted_intent = "cbt_set_task"
        res = get_response(predicted_intent,intents,input['context'],username)
        await db.set_cbt_task(username)
        return res
    

    else:
        predicted_intent = predict_class(input['message'])
        res = get_response(predicted_intent,intents,input['context'],input['username'])
        return res



    predicted_intent = predict_class(input['message'])
    res = get_response(predicted_intent,intents,input['context'],input['username'])
    return res

def setup():
    print("Hazi online")






# while True:

#     message = input("")

#     data = {"message" : message, "context" : context, "username" : "Zeia"}

#     response = hazibot_generate_response(data)

#     print("Hazi: "+response['message'])