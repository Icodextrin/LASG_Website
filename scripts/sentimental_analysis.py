import pandas as pd
from django.conf import settings
import os
import spacy
from spacy import displacy
import numpy as np
from wordcloud import WordCloud, STOPWORDS
from spacy.lang.en.examples import sentences
import nltk
# from nltk.tokenize import sent_tokenize
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
import string
import ssl
import matplotlib.pyplot as plt


def make_graphs():
    # nlp = spacy.load("en_core_web_sm")
    path = settings.MEDIA_ROOT
    mentions = pd.read_csv(os.path.join(path, "csv/comments_and_mentions.csv"), encoding="utf8")
    mentions.head()
    text = mentions['content.text'].unique()
    text = np.array2string(text)

    nltk.download('punkt')
    nltk.download('vader_lexicon')
    nltk.download('stopwords')


    words = nltk.tokenize.word_tokenize(text)
    wordList = []

    sentences = nltk.tokenize.sent_tokenize(text)

    stop_words = nltk.corpus.stopwords.words('english')

    punctuations = list(string.punctuation)
    # print(punctuations)
    for i in range(len(words)):
        words[i] = words[i].lower()

    for word in words:  # iterate over word_list
        if word in nltk.corpus.stopwords.words('english'):
            try:
                while True:
                    words.remove(word)
            except ValueError:
                pass
            wordList.append(word)

    for punctuation in punctuations:
        if punctuation in words:
            try:
                while True:
                    words.remove(punctuation)
            except ValueError:
                pass
            wordList.append(punctuation)

    # nlp = spacy.load("en_core_web_sm")

    clean_text = []

    for i in text:
        doc = nlp(i)

        for token in doc:
            if token.is_alpha and not token.is_stop:
                clean = {
                    'text': token.text,
                    'lemma': token.lemma_,
                    'part_of_speech': token.pos_,
                    'pos_tag': token.tag_}
                clean_text.append(clean)

    df = pd.DataFrame(clean_text)

    # saving the dataframe
    df.to_csv(os.path.join(path, '/csv/nlu-text.csv'))

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()

    text_df = pd.DataFrame(data=text, columns=['text'])

    text_df['scores'] = text_df['text'].apply(lambda comment: sid.polarity_scores(comment))

    text_df['scores'].head()

    text_df['compound'] = text_df['scores'].apply(lambda score_dict: score_dict['compound'])

    text_df.head()

    text_df['comp_score'] = text_df['compound'].apply(lambda c: 'pos' if c >= 0 else 'neg')

    text_df.head()

    neg_text = text_df.where(text_df['comp_score'] == 'neg').dropna()
    neg_text.head()

    pos_text = text_df.where(text_df['comp_score'] == 'pos').dropna()
    pos_text.head()

    text_df.to_csv(os.path.join(path, 'csv/sentiment-text.csv'), encoding='utf8')

    stopwords = set(STOPWORDS)
    stopwords.add("Philip")

    # Generate a word cloud image
    wordcloud = WordCloud(background_color="white", stopwords=stopwords).generate(df['text'].to_string())

    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title("All Conversation Words")
    plt.axis("off")
    plt.savefig(os.path.join(path, "/graphs/sent_analysis_all_words.png"))

    # lower max_font_size
    wordcloud = WordCloud(background_color="white", max_font_size=40, stopwords=stopwords, max_words=50).generate(
        df['text'].to_string())
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title("All Conversation Words (Smaller Font)")
    plt.axis("off")
    plt.savefig(os.path.join(path, "/graphs/sent_analysis_all_words_small.png"))

    wordcloud = WordCloud(background_color="white", max_words=50).generate(
        df.where(df['part_of_speech'] == 'PROPN').dropna()['text'].to_string())
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title("Pronouns Used")
    plt.axis("off")
    plt.savefig(os.path.join(path, "/graphs/sent_analysis_pronouns.png"))

    clean_neg_text = []

    for i in text:
        doc = nlp(i)

        for token in doc:
            if token.is_alpha and not token.is_stop:
                clean = {
                    'text': token.text,
                    'lemma': token.lemma_,
                    'part_of_speech': token.pos_,
                    'pos_tag': token.tag_}
                clean_neg_text.append(clean)

    neg_text = pd.DataFrame(clean_neg_text)
    neg_text.to_csv('neg_text_nlp.csv', encoding='utf8')
    wordcloud = WordCloud(background_color="white", stopwords=stopwords, max_words=50).generate(
        neg_text['text'].to_string())
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title("Negative Words Used")
    plt.axis("off")
    plt.savefig(os.path.join(path, "/graphs/sent_analysis_neg.png"))

    clean_pos_text = []

    for i in text:
        doc = nlp(i)

        for token in doc:
            if token.is_alpha and not token.is_stop:
                clean = {
                    'text': token.text,
                    'lemma': token.lemma_,
                    'part_of_speech': token.pos_,
                    'pos_tag': token.tag_}
                clean_pos_text.append(clean)

    pos_text = pd.DataFrame(clean_pos_text)
    pos_text.to_csv('pos_text_nlp.csv', encoding='utf8')
    wordcloud = WordCloud(background_color="white", stopwords=stopwords, max_words=50).generate(
        pos_text['text'].to_string())
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title("Positive Words Used")
    plt.axis("off")
    plt.savefig(os.path.join(path, "/graphs/sent_analysis_pos.png"))

