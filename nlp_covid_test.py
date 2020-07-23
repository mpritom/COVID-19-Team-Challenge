# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 19:01:46 2020

@author: sanugroho
"""

#STEP 1
#Import tweets from excel

import xlrd

wb1 = xlrd.open_workbook(r'C:\Users\sanugroho\.spyder-py3\positive_dataset.xlsx')
sheets_name1 = wb1.sheet_names();
ws1 = wb1.sheet_by_index(0)
positive_tweets = ws1.col_values(0)

wb2 = xlrd.open_workbook(r'C:\Users\sanugroho\.spyder-py3\negative_dataset.xlsx')
sheets_name2 = wb1.sheet_names();
ws2 = wb2.sheet_by_index(0)
negative_tweets = ws2.col_values(0)

#%%

#STEP 2
#Tokenizing the data

import nltk

positive_tweet_tokens = []
for i in range(len(positive_tweets)):
    temp_split = nltk.word_tokenize(positive_tweets[i])
    positive_tweet_tokens.append(temp_split)
    
negative_tweet_tokens = []
for i in range(len(negative_tweets)):
    temp_split = nltk.word_tokenize(negative_tweets[i])
    negative_tweet_tokens.append(temp_split)

#%%

#STEP 3
#Normalizing the data


from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

#Test
print(lemmatize_sentence(positive_tweet_tokens[100]))
print(lemmatize_sentence(negative_tweet_tokens[100]))

#%%

#STEP 4
#Removing noise from the data


import re, string

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#:/]|[!*\(\),]|..."😷RT'\
                       'http(?:%[0-9a-fA-F][0-9a-fA-F]))+"..."😷RT','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

#Test
print(lemmatize_sentence(positive_tweet_tokens[100]))
print(lemmatize_sentence(negative_tweet_tokens[100]))

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

sebastian_stop_words = ['i',
 'me',
 'my',
 'myself',
 'we',
 'our',
 'ours',
 'ourselves',
 'you',
 "you're",
 "you've",
 "you'll",
 "you'd",
 'your',
 'yours',
 'yourself',
 'yourselves',
 'he',
 'him',
 'his',
 'himself',
 'she',
 "she's",
 'her',
 'hers',
 'herself',
 'it',
 "it's",
 'its',
 'itself',
 'they',
 'them',
 'their',
 'theirs',
 'themselves',
 'what',
 'which',
 'who',
 'whom',
 'this',
 'that',
 "that'll",
 'these',
 'those',
 'am',
 'is',
 'are',
 'was',
 'were',
 'be',
 'been',
 'being',
 'have',
 'has',
 'had',
 'having',
 'do',
 'does',
 'did',
 'doing',
 'a',
 'an',
 'the',
 'and',
 'but',
 'if',
 'or',
 'because',
 'as',
 'until',
 'while',
 'of',
 'at',
 'by',
 'for',
 'with',
 'about',
 'against',
 'between',
 'into',
 'through',
 'during',
 'before',
 'after',
 'above',
 'below',
 'to',
 'from',
 'up',
 'down',
 'in',
 'out',
 'on',
 'off',
 'over',
 'under',
 'again',
 'further',
 'then',
 'once',
 'here',
 'there',
 'when',
 'where',
 'why',
 'how',
 'all',
 'any',
 'both',
 'each',
 'few',
 'more',
 'most',
 'other',
 'some',
 'such',
 'only',
 'own',
 'same',
 'so',
 'than',
 'too',
 'very',
 's',
 't',
 'can',
 'will',
 'just',
 'should',
 "should've",
 'now',
 'd',
 'll',
 'm',
 'o',
 're',
 've',
 'y',
 'ma']

#print(remove_noise(tweet_tokens[0], stop_words))

positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

for tokens in positive_tweet_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, sebastian_stop_words))

for tokens in negative_tweet_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, sebastian_stop_words))
    
#print(positive_tweet_tokens[500])
#print(positive_cleaned_tokens_list[500])

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

all_pos_words = get_all_words(positive_cleaned_tokens_list)
all_neg_words = get_all_words(negative_cleaned_tokens_list)


from nltk import FreqDist

freq_dist_pos = FreqDist(all_pos_words)
print(freq_dist_pos.most_common(20))
freq_dist_neg = FreqDist(all_neg_words)
print(freq_dist_neg.most_common(20))

#Step 6

...
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

import random

positive_dataset = [(tweet_dict, "Positive")
                     for tweet_dict in positive_tokens_for_model]

negative_dataset = [(tweet_dict, "Negative")
                     for tweet_dict in negative_tokens_for_model]

dataset = positive_dataset + negative_dataset

random.shuffle(dataset)

train_data = dataset[:250]
test_data = dataset[251:]

train_data2 = dataset

#Step 7
#%%
...
from nltk import classify
from nltk import NaiveBayesClassifier
classifier = NaiveBayesClassifier.train(train_data)

#classifier2 = nltk.classify.svm.SvmClassifier.train(train_data)

print("Accuracy Naive Bayes is:", classify.accuracy(classifier, test_data)*100)

print(classifier.show_most_informative_features(10))

#print("Accuracy SVM is:", classify.accuracy(classifier, test_data))

#print(classifier2.show_most_informative_features(10))

...
from nltk.tokenize import word_tokenize
#%%
# classifier2 = NaiveBayesClassifier.train(train_data2)

classifier2 = classifier

#print(classifier2.show_most_informative_features(10))

custom_tweet1 = "Hydroxychloroquine is the vaccine for covid19"

custom_tokens1 = remove_noise(word_tokenize(custom_tweet1))

print(classifier2.classify(dict([token, True] for token in custom_tokens1)))

custom_tweet2 = "I will not wear mask!"

custom_tokens2 = remove_noise(word_tokenize(custom_tweet2))

print(classifier2.classify(dict([token, True] for token in custom_tokens2)))

custom_tweet3 = "Put on your face mask and you're helping people"

custom_tokens3 = remove_noise(word_tokenize(custom_tweet3))

print(classifier2.classify(dict([token, True] for token in custom_tokens3)))

custom_tweet4 = "vitamin D can cure Covid19"

custom_tokens4 = remove_noise(word_tokenize(custom_tweet4))

print(classifier2.classify(dict([token, True] for token in custom_tokens4)))

custom_tweet5 = "Gargle hydrogen peroxide + salt to cure Covid19"

custom_tokens5 = remove_noise(word_tokenize(custom_tweet5))

print(classifier2.classify(dict([token, True] for token in custom_tokens5)))

custom_tweet6 = "Wear face mask if you're going to meet people"

custom_tokens6 = remove_noise(word_tokenize(custom_tweet6))

print(classifier2.classify(dict([token, True] for token in custom_tokens6)))

custom_tweet7 = "Wash your hands regularly"

custom_tokens7 = remove_noise(word_tokenize(custom_tweet7))

print(classifier2.classify(dict([token, True] for token in custom_tokens7)))

custom_tweet8 = "Azithromycin cures Covid19 in 100% patients"

custom_tokens8 = remove_noise(word_tokenize(custom_tweet8))

print(classifier2.classify(dict([token, True] for token in custom_tokens8)))

custom_tweet9 = "Wearing mask is advised by CDC and WHO"

custom_tokens9 = remove_noise(word_tokenize(custom_tweet9))

print(classifier2.classify(dict([token, True] for token in custom_tokens9)))

custom_tweet10 = "Vaccine for Covid19 is alredy available"

custom_tokens10 = remove_noise(word_tokenize(custom_tweet10))

print(classifier2.classify(dict([token, True] for token in custom_tokens10)))

#Step-8
#%%
#DecisionTreeClassifier

# ...
# from nltk import MaxentClassifier
# classifier2 = MaxentClassifier.train(train_data)


# print("Accuracy Decision Tree is:", classify.accuracy(classifier2, test_data)*100)

# print(classifier2.show_most_informative_features(100))


#%%
# custom_tweet = " hydroxychloroquine is the vaccine"

# custom_tokens = remove_noise(word_tokenize(custom_tweet))

# print(classifier2.classify(dict([token, True] for token in custom_tokens)))

# custom_tweet = "I am not wearing mask"

# custom_tokens = remove_noise(word_tokenize(custom_tweet))

# print(classifier2.classify(dict([token, True] for token in custom_tokens)))
