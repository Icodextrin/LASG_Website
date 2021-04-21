import pandas as pd
import numpy as np
import holoviews as hv
import plotly.graph_objects as go
from website import settings


def sankey_graph():
    path = settings.MEDIA_ROOT

    hv.extension('bokeh')
    file_path = path + '/csv/proj_interactions/' + "15541798_interactions.csv"
    df = pd.read_csv(file_path, index_col=0)
    #df = pd.read_csv(file_path)

    label_1 = df["commentor.name"].unique()
    label_2 = df["mention.name"].unique()
    label = np.append(label_1, label_2) #not unique

    source_1 = df["commentor.name"].tolist()
    target_1 = df["mention.name"].tolist()
    value_1 = df["count"].tolist()
    n = len(source_1)

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

    fig.update_layout(title_text= "Project " + file_path + ", " + str(n)+" patterns of communication Sankey Diagram", font_size=10)
    fig.write_image(path + '/graphs/' + 'sankey.png')
