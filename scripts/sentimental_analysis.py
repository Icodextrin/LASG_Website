import pandas as pd
from django.conf import settings
import os
import spacy
from spacy import displacy
import numpy as np
from wordcloud import WordCloud, STOPWORDS


def read_data():
    path = os.path.join(settings.MEDIA_ROOT, "/csv")
    mentions = pd.read_csv(path, encoding="utf8")
    mentions.head()
    text = mentions['content.text'].unique()