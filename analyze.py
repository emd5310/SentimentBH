from azure.ai.textanalytics import single_analyze_sentiment
from azure.ai.textanalytics import single_detect_language

# The language code to check for, all others are discarded
lang_code = "en"


# creds : dict - The dictionary containing the endpoint and ACS key to perform analysis
def set_keys(creds):
    global ep; ep = creds["endpoint"]
    global key; key = creds["key"]


# tweets : iterate-able - The list of tweets that will be checked and analyzed
def sent_analysis(tweets):
    # Check the data for the correct language
    concat_tweets = ""  # A long string containing all the tweet text, so that it only takes one call to analyze
    for tweet in tweets:

        concat_tweets += (tweet + " ")

    slicer = int((len(concat_tweets))/2)
    one = concat_tweets[0:slicer]
    two = concat_tweets[slicer:]


    # Performing analysis of all the text through ACS
    resp = single_analyze_sentiment(endpoint=ep, credential=key, input_text=one)
    resp2 = single_analyze_sentiment(endpoint=ep, credential=key, input_text=two)

    # Getting raw scores for the entire population of tweets (double)
    pop_pos = (resp.document_scores.positive + resp2.document_scores.positive) / 2
    pop_neg = (resp.document_scores.negative + resp2.document_scores.negative) / 2
    pop_neu = (resp.document_scores.neutral + resp2.document_scores.neutral) / 2
    pop_overall = resp.sentiment  # The overall sentiment is  a string, positive/neutral/negative
    # Converting the raw score to a percentage
    pop_pos_per = pop_pos*100
    pop_neg_per = pop_neg*100

    sentiments = {"sentiment": pop_overall, "positive": pop_pos, "negative": pop_neg, "neutral": pop_neu}
    return sentiments
