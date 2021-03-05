import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly import graph_objs as go
from pillow import Image 
 
def parseDate(date):
   date = str(int(date))
   return "{}-{}-{}".format(date[:4], date[4:6], date[6:])
 
# INDIVIDUAL PLAYER STATS
def indiv_stats():
   st.write('# Individual Player Stats')
 
   players = pd.read_csv('./data/players.csv', encoding="ISO-8859-1")
   matches = pd.read_csv('./data/matches.csv', encoding="ISO-8859-1")
   matches.drop(['Unnamed: 32'], axis=1, inplace=True)
   players['full_name'] = players['first_name'] + ' ' + players['last_name']
 
   #st.header('Select a player')
   player = st.selectbox('Select a player', players['full_name'])
   player_id = players.loc[players['full_name'] == player, 'player_id'].iloc[0]
   hand = players.loc[players['player_id'] == player_id, 'hand'].iloc[0]
   if hand == 'R':
       hand = 'Right'
   elif hand == 'L':
       hand = 'Left'
   else:
       hand = 'Not Specified'
   dob = players.loc[players['player_id'] == player_id, 'birth_date'].iloc[0]
   dob = parseDate(dob)
   country = players.loc[players['player_id'] == player_id, 'country_code'].iloc[0]
 
   matches_won = matches.loc[matches['winner_id'] == player_id]
   matches_lost = matches.loc[matches['loser_id'] == player_id]
   num_wins = len(matches_won)
   num_losses = len(matches_lost)
 
   st.markdown(f'## **{player}**')
   st.subheader('Overview')
 
   col1, col2 = st.beta_columns(2)
 
   col1.markdown(f'**Country**: {country}')
   col1.markdown(f'**DOB**: {dob}')
   col1.markdown(f'**Hand**: {hand}')
   col1.markdown(f'')
   col1.markdown(f'**{num_wins}** matches won')
   col1.markdown(f'**{num_losses}** matches lost')
 
   labels = 'Wins', 'Losses'
   sizes = [num_wins, num_losses]
   colors = ['lightgreen', 'lightcoral']
   explode = (0.1, 0)  # explode 1st slice
 
   plt.pie(sizes, explode=explode, labels=labels, colors=colors,
       autopct='%1.1f%%', shadow=True, startangle=140)
 
   plt.axis('equal')
   plt.savefig('./images/pie.png')
   col2.image('./images/pie.png')
 
   st.subheader('Matches')
   matches_all = pd.concat([matches_lost, matches_won])
   st.markdown(f'**{len(matches_all)}** matches total')
 
   clean_matches_all = pd.DataFrame()
 
   clean_matches_all['Date'] = matches_all['tourney_date'].apply(parseDate)
   clean_matches_all['Date'] = pd.to_datetime(clean_matches_all['Date'])
 
   clean_matches_all['Tourney'] = matches_all['tourney_name']
   clean_matches_all['Level'] = matches_all['tourney_level']
 
   clean_matches_all['Winner'] = matches_all['winner_name']
   clean_matches_all['Winner Country'] = matches_all['winner_ioc']
   clean_matches_all['Winner Rank'] = matches_all['winner_rank']
   clean_matches_all['Loser'] = matches_all['loser_name']
   clean_matches_all['Loser Country'] = matches_all['loser_ioc']
   clean_matches_all['Loser Rank'] = matches_all['loser_rank']
 
   clean_matches_all['Score'] = matches_all['score']
   clean_matches_all['Match Num'] = matches_all['match_num']
   clean_matches_all['Round'] = matches_all['round']
   clean_matches_all['Surface'] = matches_all['surface']
 
   # sort by tourney date
   clean_matches_all = clean_matches_all.sort_values(by='Date')
  
   # reset index
   clean_matches_all = clean_matches_all.reset_index(drop=True)
 
   if st.checkbox("Display all matches"):
       st.markdown(f'**Won** matches are highlighted in green!')
        # highlight rows where selected player won
       clean_matches_all = clean_matches_all.style.apply(lambda x: ["background: lightgreen" if x.Winner == player else "" for i in x], axis = 1)
       st.dataframe(clean_matches_all)
   else:
       # get the list of columns
       columns = clean_matches_all.columns.tolist()
       # st.write("Select the columns to display:")
       selected_cols = st.multiselect("Select the columns to display", columns)
       if len(selected_cols) > 0:
           selected_df = clean_matches_all[selected_cols]
           # selected_df = selected_df.style.apply(lambda x: ["background: lightgreen" if x.Winner == player else "" for i in x], axis = 1)
           st.dataframe(selected_df)
     
   st.subheader('Correlation Heat Map')
   st.write("Displays the correlation between any two features from the dataset of the player's matches.")
   corr = matches_all.corr()
   mask = np.zeros_like(corr)
   with sns.axes_style("white"):
       f, ax = plt.subplots(figsize=(15, 10))
       ax = sns.heatmap(corr, mask=mask, vmax=1, square=True,  annot=True)
       st.write(f)
      
   st.subheader('Tourneys')
   # box plot
   st.write('#### Winning rank points from winning tourney matches')
   st.write('Displays a box plot, which shows mins, maxes, medians, and quartiles.')
   fig = px.box(matches_won, x = "tourney_name", y = "winner_rank_points",
       labels={
           "tourney_name": "tourney",
           "winner_rank_points": "rank points",
       })
   fig.update_traces(quartilemethod="exclusive")
   st.plotly_chart(fig)
 
   # histogram
   st.write('#### Number of wins and losses at each tourney')
   st.write("Displays a histogram, which simultaneously shows both the player's number of wins and losses.")
   matches_all['result'] = np.where(matches_all['winner_name'] == player, 'Win', 'Loss')
   fig = px.histogram(matches_all, x="tourney_name", color="result",
       color_discrete_map={
           "Win": "lightgreen",
           "Loss": "lightcoral",
       },
       labels={
           "tourney_name": "tourney",
           "count": "number of wins/losses",
           "result": "match result"
       })
   # fig.update_layout(
   #     width=900,
   #     height=500
   # )
   st.plotly_chart(fig)
 
def about():
   st.write('# About Queens of Tennis')
   st.write("This is a web app that displays a collection of Women's Tennis players' data visually. It aims to help ease an audience into consuming the information, rather than having them look purely at a wall of numbers.")
   st.write("The sports industry is still largely male-dominated. Information that is available for women’s sports is currently still very limited and is often only available in a format that is not user-friendly. This discourages prospective fans from learning more about the game. Sexism in statistics is hurting women's sports.")
   st.write("In honor of Pearl Hacks' mission of celebrating and uplifting women, this project aims to better serve and empower women, specifically those in the sports industry.")
   st.subheader('What this app does')
   st.write("Collects available WTA data and displays it in a visual manner to make it less daunting to consume.")
   st.subheader('Created by')
   st.write('Sonali Joshi, Lacey Umamoto, Rakshaa Viswanathan, Nadia Yonata')
   img = Image.open("./images/tennis.png") 
   st.image(img) 
 
def compare_players():
   st.write('# Calculate Winning Probability')
   st.write('This shows who has a greater chance of winning between any two players.')
 
   players = pd.read_csv('./data/players.csv', encoding="ISO-8859-1")
   matches = pd.read_csv('./data/matches.csv', encoding="ISO-8859-1")
  
   players['full_name'] = players['first_name'] + ' ' + players['last_name']
  
   player1 = st.selectbox('Player Name 1', players['full_name'])
   st.write('**VS**')
   player2 = st.selectbox('Player Name 2', players['full_name'])
  
   player_id = players.loc[players['full_name'] == player1, 'player_id'].iloc[0]
   player_id2 = players.loc[players['full_name'] == player2, 'player_id'].iloc[0]
  
   player_matches_losses = matches.loc[matches['loser_id'] == player_id]
   player_matches_wins = matches.loc[matches['winner_id'] == player_id]

   player_matches_all = pd.concat([player_matches_losses, player_matches_wins])
 
   player2_matches_losses = matches.loc[matches['loser_id'] == player_id2]
   player2_matches_wins = matches.loc[matches['winner_id'] == player_id2]

   player1ratio = len(player_matches_wins) / ( len(player_matches_losses) + len(player_matches_wins) )
   player2ratio = len(player2_matches_wins) / ( len(player2_matches_losses) + len(player2_matches_wins) )

   if player1ratio > player2ratio:
       st.write(player1,' wins!')
   elif player1ratio < player2ratio:
       st.write(player2,' wins!')
   else:
       st.write('There is an equal probability of either player winning!')
 
def main():
   img = Image.open("./images/logo.png") 
   st.sidebar.image(img) 

   st.sidebar.title("Queens of Tennis 👑")
 
   nav = ['About', 'Individual Player Stats', 'Calculate Winning Probability']
   choice = st.sidebar.selectbox('Navigation', nav)
  
   if choice == 'Individual Player Stats':
       indiv_stats()
   elif choice == 'Calculate Winning Probability':
       compare_players()
   elif choice == 'About':
       about()
 
 
main()