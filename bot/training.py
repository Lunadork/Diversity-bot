#GENERAL IMPORTS
import random
import json
import pickle
import numpy as np

#NTLK IMPORTS
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

#TENSORFLOW IMPORTS
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

#Read in base intents, save as intents variable
intents = json.loads(open('intents.json').read())

#BOT SETUP 
words = []
classes = []
documents = []
ignore_letters = ['?','!','.',',']

#Iterate through intents and put into bot
for intent in intents['intents']:
    for pattern in intent['patterns']:
        #This splits patterns up into its individual words
        word_list = nltk.word_tokenize(pattern)

        #add the word list to the words array
        words.extend(word_list)

        #Add word list and its associated tag to documents
        documents.append((word_list,intent['tag']))

        #if the tag isn't stored as a class, add it too
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#Lemmatize words stored in words array, if not set to ignore in ignore_letters
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
#Change to list, remove duplicates
words = sorted(set(words))
#Do the same to our classes
classes = sorted(set(classes))

##dump it all into pickle - write as binaries (wb)
pickle.dump(words, open('words.pkl','wb'))
pickle.dump(classes, open('classes.pkl','wb'))


#Setup training
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]

    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1

    training.append([bag, output_row])

#Shuffle it about
random.shuffle(training)
#Create a numpy array based on the training array
training = np.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])

print("tr")
print(train_x)
print(train_y)
 
##NEURAL NETWORK MODEL SETUP - Dense sets up neurons.  I've no idea how this all works in reality.  I didn't do compsci xD
model = Sequential()
#Create 128 neurons, tie shape to length of words to train
model.add(Dense(128, input_shape=(len(train_x[0]),), activation = 'relu'))
model.add(Dropout(0.5))
#Create another layer of neurons
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
#Create another layer, to the length of our classes to train on.  Activation is scaling settings
model.add(Dense(len(train_y[0]), activation = 'softmax'))

# Idk what any of this means but it's needed for the model optimizer.  
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

model.compile(loss='categorical_crossentropy', optimizer = sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose = 1 )
model.save('hazibot_model.h5', hist)
print("done")
