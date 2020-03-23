import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model

model1 = load_model('hindi_bot_V2.h5')
model1._make_predict_function()
import json
import random
intents = json.loads(open('hindi_bot_V2.json', encoding="utf8").read())
words = pickle.load(open('hindi_bot_V2_words.pkl','rb'))
classes = pickle.load(open('hindi_bot_V2_classes.pkl','rb'))


def clean_up_sentence(sentence):
	# tokenize the pattern - split words into array
	print(6)
	sentence_words = nltk.word_tokenize(sentence)
	# stem each word - create short form for word
	sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
	print(7)
	return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
	# tokenize the pattern
	print(5)
	sentence_words = clean_up_sentence(sentence)
	# bag of words - matrix of N words, vocabulary matrix
	print(8)
	bag = [0]*len(words)  
	for s in sentence_words:
		for i,w in enumerate(words):
			if w == s: 
				# assign 1 if current word is in the vocabulary position
				bag[i] = 1
				if show_details:
					print ("found in bag: %s" % w)
	print(9)
	return(np.array(bag))

def predict_class(sentence, model1):
	# filter out predictions below a threshold
	print(4)
	p = bow(str(sentence), words,show_details=False)
	print(10)
	res = model1.predict(np.array([p]))[0]
	print(11)
	ERROR_THRESHOLD = 0.25
	results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
	# sort by strength of probability
	results.sort(key=lambda x: x[1], reverse=True)
	return_list = []
	for r in results:
		return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
	return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
	print(1)
	ints = predict_class(str(msg), model1)
	print(2)
	res = getResponse(ints, intents)
	print(3)
	return res
