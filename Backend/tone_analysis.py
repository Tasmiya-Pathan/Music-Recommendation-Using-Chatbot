import json
import pickle
import random

import keras
import nltk
import numpy as np
from nltk import WordNetLemmatizer
from keras.models import load_model
from textblob import TextBlob
import os

# Load the model
model = keras.models.load_model(os.path.join('Backend/data/chatbot_model.h5'))
msg = list()
text = str()
lemmatizer = WordNetLemmatizer()
intents = json.loads(open(os.path.join('Backend/data/intents.json')).read())
words = pickle.load(open(os.path.join('Backend/data/words.pkl'), 'rb'))
classes = pickle.load(open(os.path.join('Backend/data/classes.pkl'), 'rb'))

api_key = '6d5b1cd5251913147efc4b0e3ce1f1ab'

def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % word)
    return (np.array(bag))

def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

def responsed(msg1):
    msg.append(msg1)
    ints = predict_class(msg1)
    res = getResponse(ints, intents)
    return {"output" : res}

def song_emotion(msg):
    analysis = TextBlob(msg)

    # Get polarity (positive/negative) and subjectivity scores
    polarity = analysis.sentiment.polarity

    # Determine emotion based on polarity
    if polarity > 0.5:
        emotion = "Happy"
    elif polarity < -0.5:
        emotion = "Sad"
    else:
        emotion = "Neutral"
    dic1 = dict()
    dic1['emotion'] = emotion
    import requests

    url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={emotion}&api_key={api_key}&format=json&limit=10"
    response = requests.get(url)
    payload = response.json()
    for i in range(10):
        r = payload['tracks']['track'][i]
        dic1[r['name']] = r['url']
    return dic1

# print("Chatbot : Hey there, Wassup ?")
# # responded function takes text of user and returns chatbot output
# msg1 = ' '
# for i in range(3):
#     m = input("User : ")
#     res = responsed(m)
#     print("Chatbot : "+res)
#     msg1 = msg1 + m
# ans = song_emotion(msg1)
# print("Emotion : "+ans['emotion'])
#
# lst = list(ans.keys())
# print("Song Recommendations : ")
# for i in range(10):
#     print("Song_name : "+lst[i])
#     print("Song_URL : "+ans[lst[i]])


def select_and_run_function(function_name, param1):
    # Function to select and run the specified function
    if function_name == 'responsed':
        return responsed(param1)
    elif function_name == 'song_emotion':
        return song_emotion(param1)
    else:
        pass

if __name__ == "__main__":
    # If the script is run directly, you can add additional logic here
    pass