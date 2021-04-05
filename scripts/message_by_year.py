import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from website import settings


def message_by_year_graph():
    path = settings.MEDIA_ROOT
    messages = pd.read_csv(os.path.join(path, "csv/messageboards.csv"))


    messages['creator.created_at'].head()

    messages.info()
    messages["bucket.name"].head()

    messages['creator.created_at'] = pd.to_datetime(messages['creator.created_at'], format='%Y-%m-%d')

    test = pd.DataFrame(
        messages.value_counts(messages['creator.created_at'].dt.year).rename_axis('Year').reset_index(
            name='Message_Count'))

    messagesbyYear = pd.DataFrame(test)

    messagesbyYear.sort_values(by='Year')

    projectmessagebyyear = pd.DataFrame(
        messages.groupby(["bucket.name", messages['creator.created_at'].dt.year]).count())

    projectmessagebyyear = projectmessagebyyear[["id"]].reset_index()

    fig, ax = plt.subplots()
    ax.bar(messagesbyYear.Year, messagesbyYear.Message_Count)
    ax.set_ylabel('Message Count')
    ax.set_xlabel('Year')
    ax.xaxis.set_tick_params(labelsize='small')
    start, end = ax.get_xlim()
    ax.xaxis.set_ticks(np.arange(start + 1, end, 1))
    plt.savefig(os.path.join(path, "graphs/messagesbyYear.png"))
