import pandas as pd
import numpy as np
import holoviews as hv
import plotly.graph_objects as go
import sys, glob, json,csv, os
from website import settings


def sankey_graph():
    path = settings.MEDIA_ROOT
    hv.extension('bokeh')
    # list all of the json files of that type
    file_arr = glob.glob(path + "/csv/proj_interactions/" + "*_interactions.csv")
    # loop through all of the files
    for f in file_arr:
        df = pd.read_csv(f)
        label_1 = df["commentor.name"]
        label_2 = df["mention.name"]
        label = label_1.append(label_2,ignore_index=True).unique()
        source_1 = df["commentor.name"].tolist()
        target_1 = df["mention.name"].tolist()
        value_1 = df["count"].tolist()
        source_index = []
        for ele in source_1:
            a = np.where(label == ele)
            source_index.append(a[0][0])

        target_index = []
        for ele in target_1:
            a = np.where(label == ele)
            target_index.append(a[0][0])

        #generate sankey

        fig = go.Figure(data=[go.Sankey(
            node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = label,
            color = "light blue"
            ),
            link = dict(
            source = source_index,
            target = target_index,
            value = value_1
        ))])
        fig.update_layout(title_text="", font_size=10)
        #file_name = f.split("/")[-1].split(".")[0]
        file_name = os.path.split(f.split(".")[0])
        print(file_name)
        #fig.write_html(file_name+".html")
        fig.write_image(path + '/graphs/sankey/' + file_name[1] + ".png")
