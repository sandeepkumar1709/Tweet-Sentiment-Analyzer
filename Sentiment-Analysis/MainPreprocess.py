import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
import html
import string
from nltk.tokenize import TweetTokenizer 
import nltk
from nltk.corpus import stopwords          
from nltk.stem import PorterStemmer
import pickle
from nltk.stem import WordNetLemmatizer
import emoji
from nltk.corpus import wordnet
##declaring few expansions
expansion ={
    "ain't":"is not",
        "amn't":"am not",
        "aren't":"are not",
        "can't":"cannot",
        "'cause":"because",
        "couldn't":"could not",
        "couldn't've":"could not have",
        "could've":"could have",
        "daren't":"dare not",
        "daresn't":"dare not",
        "dasn't":"dare not",
        "didn't":"did not",
        "doesn't":"does not",
        "don't":"do not",
        "e'er":"ever",
        "em":"them",
        "everyone's":"everyone is",
        "finna":"fixing to",
        "gimme":"give me",
        "gonna":"going to",
        "gon't":"go not",
        "gotta":"got to",
        "hadn't":"had not",
        "hasn't":"has not",
        "haven't":"have not",
        "he'd":"he would",
        "he'll":"he will",
        "he's":"he is",
        "he've":"he have",
        "how'd":"how would",
        "how'll":"how will",
        "how're":"how are",
        "how's":"how is",
        "I'd":"I would",
        "I'll":"I will",
        "I'm":"I am",
        "I'm'a":"I am about to",
        "I'm'o":"I am going to",
        "isn't":"is not",
        "it'd":"it would",
        "it'll":"it will",
        "it's":"it is",
        "I've":"I have",
        "kinda":"kind of",
        "let's":"let us",
        "mayn't":"may not",
        "may've":"may have",
        "mightn't":"might not",
        "might've":"might have",
        "mustn't":"must not",
        "mustn't've":"must not have",
        "must've":"must have",
        "needn't":"need not",
        "ne'er":"never",
        "o'":"of",
        "o'er":"over",
        "ol'":"old",
        "oughtn't":"ought not",
        "shalln't":"shall not",
        "shan't":"shall not",
        "she'd":"she would",
        "she'll":"she will",
        "she's":"she is",
        "shouldn't":"should not",
        "shouldn't've":"should not have",
        "should've":"should have",
        "somebody's":"somebody is",
        "someone's":"someone is",
        "something's":"something is",
        "that'd":"that would",
        "that'll":"that will",
        "that're":"that are",
        "that's":"that is",
        "there'd":"there would",
        "there'll":"there will",
        "there're":"there are",
        "there's":"there is",
        "these're":"these are",
        "they'd":"they would",
        "they'll":"they will",
        "they're":"they are",
        "they've":"they have",
        "this's":"this is",
        "those're":"those are",
        "'tis":"it is",
        "'twas":"it was",
        "wanna":"want to",
        "wasn't":"was not",
        "we'd":"we would",
        "we'd've":"we would have",
        "we'll":"we will",
        "we're":"we are",
        "weren't":"were not",
        "we've":"we have",
        "what'd":"what did",
        "what'll":"what will",
        "what're":"what are",
        "what's":"what is",
        "what've":"what have",
        "when's":"when is",
        "where'd":"where did",
        "where're":"where are",
        "where's":"where is",
        "where've":"where have",
        "which's":"which is",
        "who'd":"who would",
        "who'd've":"who would have",
        "who'll":"who will",
        "who're":"who are",
        "who's":"who is",
        "who've":"who have",
        "why'd":"why did",
        "why're":"why are",
        "why's":"why is",
        "won't":"will not",
        "wouldn't":"would not",
        "would've":"would have",
        "y'all":"you all",
        "you'd":"you would",
        "you'll":"you will",
        "you're":"you are",
        "you've":"you have",
        "Whatcha":"What are you",
        "luv":"love",
        "sux":"sucks",
        "y":"why"
}

## all emoticons separating to positive and negative
searched_emoticons = {
        ":O":"sad",
        "=/":"sad",
        "=(" : "sad",
        ":‑)":"smiley",
        ":-]":"smiley",
        ":-3":"smiley",
        ":->":"smiley",
        "8-)":"smiley",
        ":-}":"smiley",
        ":)":"smiley",
        ":]":"smiley",
        ":3":"smiley",
        ":>":"smiley",
        "8)":"smiley",
        ":}":"smiley",
        ":o)":"smiley",
        ":c)":"smiley",
        ":^)":"smiley",
        "=]":"smiley",
        "=)":"smiley",
        ":-))":"smiley",
        ":‑D":"smiley",
        "8‑D":"smiley",
        "x‑D":"smiley",
        "X‑D":"smiley",
        ":D":"smiley",
        "8D":"smiley",
        "xD":"smiley",
        "XD":"smiley",
        ":‑(":"sad",
        ":‑c":"sad",
        ":‑<":"sad",
        ":‑[":"sad",
        ":(":"sad",
        ":c":"sad",
        ":<":"sad",
        ":[":"sad",
        ":-||":"sad",
        ">:[":"sad",
        ":{":"sad",
        ":@":"sad",
        ">:(":"sad",
        ":'‑(":"sad",
        ":'(":"sad",
        ":‑P":"playful",
        "X‑P":"playful",
        "x‑p":"playful",
        ":‑p":"playful",
        ":‑Þ":"playful",
        ":‑þ":"playful",
        ":‑b":"playful",
        ":P":"playful",
        "XP":"playful",
        "xp":"playful",
        ":p":"playful",
        ":Þ":"playful",
        ":þ":"playful",
        ":b":"playful",
        "<3":"love"}



emoticons = pd.read_csv('G:\Major project\Twitter datasets/smileys.csv')
positive_emoticons = emoticons[emoticons.Sentiment == 1]
negative_emoticons = emoticons[emoticons.Sentiment == 0]

## reading all acronyms sort of chat words and so on upto 5000
acronyms = pd.read_csv('G:\Major project\Twitter datasets/acronyms.csv')

## loading few custom stopwords
stops = pd.read_csv('G:\Major project\Twitter datasets/stopwords.csv')
stops.columns = ['Word']

##replacing few negation words like 
negation_words = pd.read_csv('G:\Major project\Twitter datasets/negation.csv')
punctuation = string.punctuation

##loading few positive words and negative words
positive_words = pd.read_csv('G:\Major project\Twitter datasets/positive-words.csv', sep='\t')
positive_words.columns = ['Word', 'Sentiment']
negative_words = pd.read_csv('G:\Major project\Twitter datasets/negative-words.csv', sep='\t',encoding='ISO-8859-1')
negative_words.columns = ['Word', 'Sentiment']

def replace_with_pattern(pattern,replace,df):
    return df.apply(lambda tweet: re.sub(pattern, replace, " " + tweet + " "))

def url(df):
    pattern_url = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''')
    return replace_with_pattern(pattern_url," ",df)




##creating a pattern for emoticons from the dataset 
def make_emoticon_pattern(emoticons):
    pattern = "|".join(map(re.escape, emoticons.Smiley))
    pattern = "(?<=\s)(" + pattern + ")(?=\s)"
    
    return pattern
## replacing with posit and neg
def replace_emoticons(df):
    df = replace_with_pattern(make_emoticon_pattern(positive_emoticons), ' positive ',df)
    df = replace_with_pattern(make_emoticon_pattern(negative_emoticons), ' negative ',df)
    
    return df
def replace_searched(df):
 
    for i in range(len(df)):
        temp = df[i].split()
        for j in range(len(temp)):
            
            if temp[j] in searched_emoticons:
                temp[j] = searched_emoticons[temp[j]]
                chk = j
            elif temp[j] in expansion:
                temp[j] = expansion[temp[j]]
            elif temp[j] in positive_words['Word']:
                temp[j] = "positive"
            elif temp[j] in negative_words['Word']:
                temp[j] = "negative"
        df[i] = " ".join(temp)


    return df


def emojii(df):
    def convert_emojis(text):
       
        text = emoji.demojize(text)
        
        
        return text
    p = ":|_"
    pattern_sep = re.compile(p)
    df = df.apply(lambda tweet: convert_emojis(tweet))
    return replace_with_pattern(pattern_sep," ",df)

def remove_unicode(df):
    
    def reply(string):
        try:
            string = string.encode('ascii','ignore')
            string = string.decode()
    
        except UnicodeDecodeError:
            pass
        return string
#     print(df)
    return df.apply(lambda tweet: reply(tweet))

def decode_html(df):
    return df.apply(lambda tweet: html.unescape(tweet))


def remove_usernames(df):
    pattern_usernames = "@\w{1,}"
    return replace_with_pattern(pattern_usernames," ",df)

#remove punctuations

punch = string.punctuation

def remove_punctuation(df):
    def translate(text):
        return text.translate(str.maketrans('', '', punch))
    df = df.apply(lambda tweet : translate(tweet))
    return df.apply(lambda tweet : str.lower(tweet))

from collections import Counter
def acronym(df):
    # Create a dictionary of acronym which will be used to get translations
    acronym_dictionary = dict(zip(acronyms.Acronym, acronyms.Translation))
    acronyms_counter = Counter()
    def acronym_to_translation(tweet, acronyms_counter):
        words = tweet.split()
        new_words = []
        for i, word in enumerate(words):
            if word in acronym_dictionary:

                acronyms_counter[word] += 1
                new_words.extend(acronym_dictionary[word].split())
            else:
                new_words.append(word)

        return " ".join(new_words)

    return df.apply(lambda tweet: acronym_to_translation(tweet, acronyms_counter))


stopwords_english = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 
                     'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']
def stop_words_removal(df):
    # Remove stopword from tweets
    def remove_stopwords(tweet):
        tweet = tweet.split()
        tweet = [None if word in stopwords_english else word for word in tweet]
        new =  [word for word in tweet if word]
        return " ".join(new)

    return df.apply(lambda tweet: remove_stopwords(tweet))


def stem(df):
    stemmer = PorterStemmer()
    def stemming_words(tweet):
        tweet = tweet.split()
        new = [stemmer.stem(word) for word in tweet]
        
        return " ".join(new)
    return df.apply(lambda tweet: stemming_words(tweet))




def lemmetize(df):
    
    #lemmatizing (because of steming private ==> privat so we retain it back to private)
    lemmatizer = WordNetLemmatizer()
    ctr = 0
    def get_wordnet_pos(word):
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)
    def lemmatize_words(text):
        mod = text.split()

        return " ".join([lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in mod])
    return df.apply(lambda tweet : lemmatize_words(tweet))


def preprocess(df):
    df["text"] = remove_usernames(df["text"])
    #print("user names removed")
    df["text"] = url(df["text"])
    #print("urls removed")
    df["text"] = replace_searched(df["text"])
    #print("normalizing don't to do not,....")
    df["text"] = replace_emoticons(df["text"])
    #print("replacing all emoticons with positive and negative")
    df["text"] = emojii(df["text"])
    #print("replaced all emoji's")
    df["text"] = remove_unicode(df["text"])
    #print("removing all unicodes")
    df["text"] = decode_html(df["text"])
    #print("decoding all html")
    df["text"] = remove_punctuation(df["text"])
    #print("removing all punctuations and making it to lowercase")
    df["text"] = acronym(df["text"])
    #print("replacing all acronyms and chat words")
    df["text"] = stop_words_removal(df["text"])
    #print("removing all stop words")
    df["text"] = stem(df["text"])
    #print("steming all words")
    return df
