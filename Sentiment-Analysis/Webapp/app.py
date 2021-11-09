import os
import tweepy as tw
from flask import Flask,request,url_for,render_template,jsonify
import tweepy as tw
import pandas as pd
import datetime
# from datetime import datetime
import sys
sys.path.append("G:\Major project")
from MainPreprocess import *
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64
import time

consumer_key= 'vWdJyOoVeTu4VEzboZSgSd7NP'
consumer_secret= 'hP9okVJkz0Tt4AVZyHdNfi1VGNqUuWNftaGyz95uQPY7uTg5wQ'
access_token= '1319181878927093760-Qj0Ggbis389Y8378hNQIDp9sGLjqfr'
access_token_secret= '2QI7YvflA639EA4CcHtsnpMEQjoCJCzELaQAMT4LW4qh8'


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
global event_name,date_of_event
counter = pickle.load(open(r"G:\Major project\Models\counter1.sav","rb"))
model = pickle.load(open("G:\Major project\Models\modelnaive1.sav", 'rb'))
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
@app.route('/')
def index():
    return render_template('login.html')



@app.route('/login',methods=['POST','GET'])
def details():
    if request.form['user'] == "qwerty" and request.form['password'] == "12345":
        return render_template("details.html")
    else:
        return "Invalid Credentials. Please try again."

@app.route('/sample_tweets',methods = ['POST','GET'])
def sample():
    global event_name
    event_name = request.form['event_name']
    event_name +=' -filter:retweets'
    # Define the search term and the date_since date as variables
    global date_of_event
    date_of_event = request.form["event_date"]
    search_words = event_name
    date_since = date_of_event
    # date_until = "2021-04-26"
    tweets = tw.Cursor(api.search,
                q=search_words,
                lang="en",
                since=date_since,
                    
                    result_type="recent").items(10)

    tweets_details = [[tweet.text, tweet.user.location] for tweet in tweets]
    tweet_df = pd.DataFrame(data=tweets_details, 
                            columns=['text', "location"])
    # print(type(tweet_df.text))
    # for i in tweet_df.text:
    #     print(i)
    return render_template("display_tweets.html",tweet = tweet_df)

@app.route("/display_final",methods = ["POST","GET"])
def final_page():
    # event_name = request.form['event_name']
    # event_name +=' -filter:retweets'
    # Define the search term and the date_since date as variables
    # date_of_event = request.form["event_date"]
    search_words = event_name
    # print(search_words)
    date_since = date_of_event
    # date_until = "2021-04-26"
    y,m,d = date_since.split("-")
    date_since = y[2:]+"-"+m+"-"+d
    date = date_since+" 00:00:01"

    date_time_obj = datetime.datetime.strptime(date, '%y-%m-%d %H:%M:%S')
    date_until = date_time_obj + datetime.timedelta(days=1)
    date_until = str(date_until)
    date_until = date_until.split()[0]
    print(date_of_event)
    print(search_words)
    tweets_pre = tw.Cursor(api.search,
                q=search_words,
                lang="en",
                since = '2018-01-01',
                until = date_of_event,
                    result_type="recent").items(100)
    # print(tweets_pre)
    # return render_template("display_tweets.html",tweet = tweet_pre_df)
    # print(tweets_pre)
    # for i in tweets_pre:
    #     print(i.text)

    # print(date_since+"s")
    # print(date_until+"u")
    date_since = "20"+date_since
    tweets_curr = tw.Cursor(api.search,
                q=search_words,
                lang="en",
                since = date_since,
                until = date_until,
                    
                    result_type="recent").items(100)

    tweets_post = tw.Cursor(api.search,
                q=search_words,
                lang="en",
                since=date_of_event,
                    result_type="recent").items(100)
    

    tweets_predate = [[tweet.text, tweet.user.location] for tweet in tweets_pre]
    # print(tweets_predate)
    tweet_pre_df = pd.DataFrame(data=tweets_predate, 
                            columns=['text', "location"])

    tweets_currdate = [[tweet.text, tweet.user.location] for tweet in tweets_curr]
    tweet_curr_df = pd.DataFrame(data=tweets_currdate, 
                            columns=['text', "location"])

    tweets_postdate = [[tweet.text, tweet.user.location] for tweet in tweets_post]
    tweet_post_df = pd.DataFrame(data=tweets_postdate, 
                            columns=['text', "location"])
    # print(tweet_pre_df.shape)
    tweet_pre_df =  preprocess(tweet_pre_df)
    tweet_curr_df = preprocess(tweet_curr_df)
    tweet_post_df = preprocess(tweet_post_df)
    
    # print(tweet_pre_df)
    # cv = pickle.load(open(r"G:\Major project\Models\naivevector.pickle","rb"))
    # model = pickle.load(open("G:\Major project\Models\modelwithnaive.sav","rb"))
    # counter = pickle.load(open(r"G:\Major project\Models\counter.sav","rb"))
    # model = pickle.load(open("G:\Major project\Models\modelnaive.sav", 'rb'))
    # print((tweet_curr_df['text'].values))


     # plt.show()
    # Convert plot to PNG image
    # pngImage = io.BytesIO()
    # FigureCanvas(fig).print_png(pngImage)
    #  # Encode PNG image to base64 string
    # pngImageB64String = "data:image/png;base64,"
    # pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    pre_vector = counter.transform(tweet_pre_df['text'].values)
    current_vector = counter.transform(tweet_curr_df['text'].values)
    post_vector = counter.transform(tweet_post_df['text'].values)
    
    # print(pre_vector.shape)
    pre_result = model.predict(pre_vector)
    curr_result = model.predict(current_vector)
    post_result = model.predict(post_vector)
    pre_pos,pre_neg = (pre_result == 1).sum(),(pre_result == 0).sum()
    curr_pos,curr_neg = (curr_result == 1).sum(),(curr_result == 0).sum()
    post_pos,post_neg = (post_result == 1).sum(),(post_result == 0).sum()
    print(pre_pos,pre_neg)
    print(curr_pos,curr_neg)
    print(post_pos,post_neg)
    data = [[pre_pos,curr_pos,post_pos],[pre_neg,curr_neg,post_neg]]
    X = np.arange(3)
    fig = plt.figure()
    
    plt.bar(X + 0.00, data[0], color = '#38C477', width = 0.25,label='positive')
    plt.bar(X + 0.25, data[1], color = '#F2543D', width = 0.25,label = 'negative')
    # Set x-axis name
    plt.xlabel("Sentiment")

    # # Set y-axis name
    plt.ylabel("Frequecy")
    plt.xticks(X,['Pre-Event', 'Current-event', 'Post-Event'])
    plt.yticks(np.arange(0, 100, 10))
    plt.legend()
    plt.rcParams['axes.facecolor'] = '#ffff99'

    plt.savefig(r'static\new_plot0.png')
    plt.close()

    d1 = [pre_pos,pre_neg]
    d2 = [curr_pos,curr_neg]
    d3 = [post_pos,post_neg]

    labels = ['Positive','Negative']
    colors = ['#38C477','#F2543D']
    # create a figure with two subplots
    # fig, (ax1, ax2,ax3) = plt.subplots(1, 3)
    
    # plot each pie chart in a separate subplot
    plt.rcParams['axes.facecolor'] = '#ffff99'
    plt.pie(d1, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Pre Event")
    plt.legend(labels, loc="best")
    plt.axis('equal')
    plt.savefig(r'static\new_plot10.png')
    plt.close()
    plt.rcParams['axes.facecolor'] = '#ffff99'
    plt.pie(d2, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Current Event")
    plt.legend(labels, loc="best")
    plt.axis('equal')
    plt.savefig(r'static\new_plot20.png')
    plt.close()
    plt.rcParams['axes.facecolor'] = '#ffff99'
    plt.pie(d3, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Post Event")
    plt.legend(labels, loc="best")
    plt.axis('equal')
    plt.savefig(r'static\new_plot30.png')
    plt.close()
    # time.sleep(5)

    # ax1.set_title("Pre Event")
    # ax2.set_title("Current Event")
    # ax3.set_title("Post Event")

    # plt.legend(labels, loc="best")
    # plt.axis('equal')
    
    
    # pngImage1 = io.BytesIO()
    # FigureCanvas(fig1).print_png(pngImage1)
    #  # Encode PNG image to base64 string
    # pngImageB64String1 = "data:image/png;base64,"
    # pngImageB64String1 += base64.b64encode(pngImage.getvalue()).decode('utf8')
    # plt.savefig(r'G:\Major project\Webapp\static\new_plot1.png')
    # plt.close()
    return render_template('final.html')
    

    # print("hi")
    # return "Done"
# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == "__main__":
    app.run(debug=True)