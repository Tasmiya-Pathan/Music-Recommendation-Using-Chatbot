import json
import os
import pickle

import nltk
from nltk.stem import WordNetLemmatizer
import random
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD


lemmatizer = WordNetLemmatizer()
intents_file = open(os.path.join('data/intents.json')).read()
intents = json.loads(intents_file)

words = []
classes = []
documents = []
ignore_letters = ['!', '?', ',', '.']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        # Add documents to the corpus
        documents.append((word, intent['tag']))
        # Add to the classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Create the training data
training = []
# Create empty array for the output
output_empty = [0] * len(classes)

# Training set, bag of words for every sentence
for doc in documents:
    # Initializing bag of words
    bag = [0] * len(words)
    # List of tokenized words for the pattern
    word_patterns = doc[0]
    # Lemmatize each word - create a base word to represent related words
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    # Create the bag of words array with 1 if the word is found in the current pattern
    for word in word_patterns:
        if word in words:
            bag[words.index(word)] = 1
    # Output is '0' for each tag and '1' for the current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

# Shuffle the features
random.shuffle(training)

# Separate into X (patterns) and Y (intents)
train_x = np.array([i[0] for i in training])
train_y = np.array([i[1] for i in training])

print("Training data is created")

# deep neural networds model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
# Compiling model. SGD with Nesterov accelerated gradient gives good results for this model
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#Training and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save(os.path.join('data/chatbot_model.h5'), hist)
print("model is created")

###### Lematization  #############

words = []
classes = []
documents = []
ignore_letters = ['!', '?', ',', '.']
intents_file = open('data/intents.json').read()
intents = json.loads(intents_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word
        word = nltk.word_tokenize(pattern)
        words.extend(word)
        # add documents in the corpus
        documents.append((word, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
print(documents)
# lemmaztize and lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
words = sorted(list(set(words)))
# sort classes
classes = sorted(list(set(classes)))
# documents = combination between patterns and intents
print(len(documents), "documents")
# classes = intents
print(len(classes), "classes", classes)
# words = all words, vocabulary
print(len(words), "unique lemmatized words", words)

pickle.dump(words, open(os.path.join('data/words.pkl'), 'wb'))
pickle.dump(classes, open(os.path.join('data/classes.pkl'), 'wb'))
# create our training data
training = []
# create an empty array for our output
output_empty = [0] * len(classes)
# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])
# shuffle our features and turn into np.array
random.shuffle(training)
# Separate into X (patterns) and Y (intents)
train_x = np.array([i[0] for i in training])
train_y = np.array([i[1] for i in training])
print("2. Training data created")


# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=150, batch_size=5, verbose=1)
model.save(os.path.join('data/chatbot_model.h5'), hist)

print("model created")
