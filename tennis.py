import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sklearn as sk

import plotly.graph_objects as go
from plotly import graph_objs as go

from streamlit_echarts import st_echarts

from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts

def parse(date):
    return "{}-{}-{}".format(date[:4], date[4:6], date[6:])

def display_winlossratio(num_wins, num_losses):
    option = {
        'title' : {
            'text': 'Win/Loss Ratio',
            #'subtext': '',
            'x':'center'
        },
        'tooltip' : {
            'trigger': 'item',
            'formatter': "{b} ({d}%)"
        },
        'legend': {
            'orient': 'vertical',
            'left': 'left',
            'data': ['Wins', 'Losses']
        },
        'series' : [{
            'name': 'Wins/Losses',
            'type': 'pie',
            'radius' : '55%',
            'center': ['50%', '60%'],
            'data':[
                {'value':num_wins, 'name':str(num_wins) + ' Wins'},
                {'value':num_losses, 'name':str(num_losses) + ' Losses'},
            ],
            'itemStyle': {
                'emphasis': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
                }
            }
        }]
    }
    st_echarts(options=option)


# BoxPlot distribution
def boxplot():
    matches = pd.read_csv('./data/matches.csv', encoding="ISO-8859-1")
    fig = px.box(matches, x = "tourney_name", y = "winner_rank_points")
    fig.update_traces(quartilemethod="exclusive")
    st.plotly_chart(fig)


# Count Plot
def count():
    data = pd.read_csv('./data/matches.csv', encoding="ISO-8859-1")
    fig = go.Figure()
    dataa = data.groupby('tourney_name')
    for name, group in dataa:
        trace = go.Histogram()
        trace.name = name
        trace.x = group['winner_name']
        fig.add_trace(trace)

    fig.update_layout(
        title_text = 'Total counts of Players Winning a match',
        width=900,
        height=500
    )
    st.plotly_chart(fig)


# INDIVIDUAL PLAYER STATS
def indiv_stats(): 
    st.header('Individual Player Stats')

    players = pd.read_csv('./data/players.csv', encoding="ISO-8859-1")
    matches = pd.read_csv('./data/matches.csv', encoding="ISO-8859-1")
    players['full_name'] = players['first_name'] + ' ' + players['last_name']

    #st.header('Select a player')
    player = st.selectbox('Player Name', players['full_name'])
    player_id = players.loc[players['full_name'] == player, 'player_id'].iloc[0]
    hand = players.loc[players['player_id'] == player_id, 'hand'].iloc[0]
    if hand == 'R':
        hand = 'Right'
    elif hand == 'L':
        hand = 'Left'
    else:
        hand = 'Not Specified'
    dob = players.loc[players['player_id'] == player_id, 'birth_date'].iloc[0]
    dob = parse(str(int(dob)))
    country = players.loc[players['player_id'] == player_id, 'country_code'].iloc[0]

    st.header(player)
    st.markdown(f'**Country: ** {country}')
    st.markdown(f'**DOB: ** {dob}')
    st.markdown(f'**Hand: ** {hand}')

    player_matches_losses = matches.loc[matches['loser_id'] == player_id]
    player_matches_wins = matches.loc[matches['winner_id'] == player_id]

    num_wins = len(player_matches_wins)
    num_losses = len(player_matches_losses)

    # st.subheader('Matches Won')
    # st.write(num_wins, ' matches won.')

    # st.subheader('Matches Lost')
    # st.write(num_losses, ' matches lost.')

    display_winlossratio(num_wins, num_losses)

    st.subheader('All Matches')
    player_matches_all = pd.concat([player_matches_losses, player_matches_wins])
    st.write(len(player_matches_all), ' matches total.')

    boxplot()
    count()

    st.subheader('Compare Player')
    player2 = st.header(st.selectbox('Player Name', players['full_name']))
    player_id2 = players.loc[players['full_name'] == player2, 'player_id'].iloc[0]
    player2_matches_losses = matches.loc[matches['loser_id'] == player_id2]
    player2_matches_wins = matches.loc[matches['winner_id'] == player_id2]
    if player_matches_wins/player_matches_all > player2_matches_wins/(player2_matches_losses+player2_matches_wins):
        st.write(player,' wins!')
    else if player_matches_wins/player_matches_all < player2_matches_wins/(player2_matches_losses+player2_matches_wins):
        st.write(player2,' wins!')
    else:
        st.write('There is an equal probability of both winning!')

    # st.table(player_matches_all)

    # st.subheader('Tourneys')
    # player_matches_tourneys = matches.loc[matches['winner_id'] == player_id, 'tourney_name']
    # st.table(player_matches_tourneys)

def overall_stats():
    st.header('Overall Stats')

def home():
    st.header('Home')
    st.text('Welcome to the homepage!')

def main():
    st.sidebar.title("Women's Tennis Association")

    nav = ['Individual', 'Overall', 'Home']
    choice = st.sidebar.selectbox('Navigation', nav)
    
    if choice == 'Individual':
        indiv_stats()
    elif choice == 'Overall':
        overall_stats()
    elif choice == 'Home':
        home()


main() 