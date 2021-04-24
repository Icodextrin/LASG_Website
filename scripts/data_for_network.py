# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 03:48:19 2021

@author: Bin Tang
"""

import pandas as pd
import networkx as nx

def main():
    # loop for all files:
 
    # file_arr = glob.glob("*_interactions.csv")  
    # for f in file_arr:
    #     df = pd.read_csv(f)
        
    file_path = "a_interactions.xlsx" 
    #from here, if the file is excel, no need to change
    df = pd.read_excel(file_path, index_col = 0)
    
    G_weighted = nx.Graph()
    for index, row in df.iterrows():
        G_weighted.add_edge(row["commentor.name"],\
                            row["mention.name"],\
                            weight = row["count"])
    # color of nodes
    color_map = [] #'blue'
    for node in G_weighted:
        if node < "20":
            color_map.append('blue')
        else:
            color_map.append('green')
    nx.draw_networkx(G_weighted, node_size = 250, node_color = color_map, with_labels=True)  
    
main()
