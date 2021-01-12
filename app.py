#!/usr/bin/env python
# coding: utf-8

# In[2]:


import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from jupyter_dash import JupyterDash
import dash
from dash.dependencies import Input, Output

from datetime import datetime as dt
import plotly.express as px

from jupyter_dash import JupyterDash
import dash
import numpy as np



app = dash.Dash(__name__)
server = app.server


# In[3]:


Spotify = pd.read_csv("Spotify_to_app.csv", sep=";", encoding='utf_8_sig')

key_options          = Spotify["music_key"].astype(str).unique()
language_options     = Spotify["Artist_origin"].astype(str).unique()
decade_options       = Spotify["Song_Decade"].astype(str).unique()

app = dash.Dash()
#app.layout = html.Div(html.H1('Heading', style={'backgroundColor':'blue'})
app.layout = html.Div([
    html.H2("Popularity of songs"),
    html.Div(
        [
            dcc.Dropdown(
                id="music_key",
                options=[{
                    'label': i,
                    'value': i
                } for i in key_options],
                value='All music keys'
            ),
            dcc.Dropdown(
                id="Artist_origin",
                options=[{
                    'label': i,
                    'value': i
                } for i in language_options],
                value='All origins'
             ),
            dcc.Dropdown(
                id="Song_Decade",
                options=[{
                    'label': i,
                    'value': i
                } for i in decade_options],
                value='All Decades'
            ),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
     dcc.Graph(id='funnel-graph'),
    ])

@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('music_key','value'),
    dash.dependencies.Input('Artist_origin','value'),
    dash.dependencies.Input('Song_Decade','value')])
    
def update_graph(music_key,Artist_origin,Song_Decade):
    if ((music_key == "All music keys") & (Artist_origin == "All origins") & (Song_Decade == "All Decades")):
        Spotify_plot = Spotify.copy()
    
    elif ((music_key == "All music keys") & (Song_Decade == "All Decades")):
        Spotify_plot = Spotify[(Spotify['Artist_origin'].astype(str)==Artist_origin)]
        
    elif ((music_key == "All music keys") & (Artist_origin == "All origins")):
        Spotify_plot = Spotify[(Spotify['Song_Decade'].astype(str)==Song_Decade)]
    
    elif ((Song_Decade == "All Decades") & (Artist_origin == "All origins")):
        Spotify_plot = Spotify[(Spotify['music_key']==music_key)]
                             
    elif ((music_key == "All music keys")):
        Spotify_plot = Spotify[(Spotify['Song_Decade'].astype(str)==Song_Decade) & (Spotify['Artist_origin'].astype(str)==Artist_origin)]
    
    elif ((Song_Decade == "All Decades")):
        Spotify_plot = Spotify[(Spotify['music_key']==music_key) & (Spotify['Artist_origin'].astype(str)==Artist_origin)]
                                            
    elif ((Artist_origin == "All origins")):
        Spotify_plot = Spotify[(Spotify['music_key']==music_key) & (Spotify['Song_Decade'].astype(str)==Song_Decade)]
    
    elif ((music_key != "All music keys") & (Song_Decade != "All Decades") & (Artist_origin != "All origins")):
        Spotify_plot = Spotify[(Spotify['music_key']==music_key) & (Spotify['Song_Decade'].astype(str)==Song_Decade) & (Spotify['Artist_origin'].astype(str)==Artist_origin)]
        
    trace1 = go.Bar(x=Spotify_plot['artists'], y=Spotify_plot['Language Specific Popularity'], name='Language Specific Popularity',marker_color='pink')
    trace2 = go.Bar(x=Spotify_plot['artists'], y=Spotify_plot['popularity'], name='Global Popularity',marker_color='black')

    return {
        'data': [trace1, trace2],
        'layout':
        go.Layout(
            title='Artist popularity from {} during {}. Song in {} key'.format(Artist_origin,Song_Decade,music_key),
            barmode ='group',plot_bgcolor='rgb(30, 215, 96)',paper_bgcolor='rgb(30, 215, 96)')
    }


if __name__ == '__main__':
    app.run()


# In[ ]:




