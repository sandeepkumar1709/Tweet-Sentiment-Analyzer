# Tweet Sentiment Analyzer
The Tweet Sentiment Analyzer is a web application designed to analyze sentiments expressed in tweets related to specific events. Leveraging machine learning (ML) algorithms, it categorizes tweets into three distinct sentiments: pre-event, current, and post-event. This classification provides users with valuable insights into the overall sentiment surrounding an event.

## Key Components:
Data Cleaning and Processing Challenges:
We encountered significant challenges related to data quality during development:
Noise Reduction: Removing irrelevant or spammy tweets.
Text Preprocessing: Tokenization, stemming, and special character removal.
Handling Emojis and Slang: Dealing with non-standard language expressions.
Imbalanced Classes: Ensuring balanced training data.
## Machine Learning Algorithms:
The heart of the system lies in ML algorithms:
Naive Bayes: Probabilistic classification based on word frequencies.
Support Vector Machines (SVM): Decision boundaries for sentiment classes.
These algorithms process tweet content, considering features like keywords, sentiment-bearing phrases, and context.
## Sentiment Classification:
Pre-Event Sentiment: Analyzes tweets leading up to the event. Are people excited, anxious, or indifferent?
Current Sentiment: Focuses on real-time tweets during the event. Is the sentiment positive, negative, or neutral?
Post-Event Sentiment: Examines tweets after the event. Did it leave a positive or negative impact?
## Graphical Visualization:
To enhance user understanding, we present sentiment results in graph format as shown below.
![image](https://github.com/sandeepkumar1709/Sentiment-Analysis/assets/68548056/da84215f-44a9-48d3-85a4-40456eb80df8)


![image](https://github.com/sandeepkumar1709/Sentiment-Analysis/assets/68548056/3c7417fe-5ec5-44e3-b1a0-6945ded7f3b8)
Users can visualize sentiment trends over time, providing a more intuitive representation of tweet sentiments.
## Web Application Stack:
Flask: A lightweight Python web framework for routing and views.
HTML, CSS, and Bootstrap: Create the user interface (UI) and styling.
Direct Model Integration:
Instead of microservices, we’ve embedded the trained sentiment analysis model directly within the Flask application.
When a user submits a tweet, Flask invokes the model for sentiment prediction.
## Workflow:
A user accesses the web application via a browser.
The front-end interacts with the Flask back-end.
Flask routes requests to the sentiment analysis model.
Results are presented to the user in an intuitive UI.
Th


In summary, the Tweet Sentiment Analyzer combines data cleaning expertise, direct model integration, and a user-friendly Flask web interface. We’re committed to refining our approach based on real-world challenges and feedback!



Please refer to the project publication here: https://www.ijrar.org/papers/IJRAR23C1279.pdf
