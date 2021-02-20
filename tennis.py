import pandas as pd 
import streamlit as st 

def parse(date):
    return "{}-{}-{}".format(date[:4], date[4:6], date[6:])

st.title("Women's Tennis Association") 
st.info("Displays a chosen player's matches and number of wins and losses.")

players = pd.read_csv('./data/players.csv', encoding="ISO-8859-1")
matches = pd.read_csv('./data/matches.csv', encoding="ISO-8859-1")

players['full_name'] = players['first_name'] + ' ' + players['last_name']

st.header('Select a player')
player = st.selectbox('Player Name', players['full_name'])
player_id = players.loc[players['full_name'] == player, 'player_id'].iloc[0]
hand = players.loc[players['player_id'] == player_id, 'hand'].iloc[0]
dob = players.loc[players['player_id'] == player_id, 'birth_date'].iloc[0]
dob = parse(str(int(dob)))
country = players.loc[players['player_id'] == player_id, 'country_code'].iloc[0]

st.header(player)
st.markdown(f'**Country: ** {country}')
st.markdown(f'**DOB: ** {dob}')
st.markdown(f'**Hand: ** {hand}')

player_matches_losses = matches.loc[matches['loser_id'] == player_id]
player_matches_wins = matches.loc[matches['winner_id'] == player_id]

st.subheader('Matches Lost')
st.write(len(player_matches_losses), ' matches lost.')
# st.markdown(f'**{len(player_matches_losses)}** matches lost.')
# st.table(player_matches_losses)

st.subheader('Matches Won')
st.write(len(player_matches_wins), ' matches won.')
# st.table(player_matches_wins)

st.subheader('All Matches')
player_matches_all = pd.concat([player_matches_losses, player_matches_wins])
st.write(len(player_matches_all), ' matches total.')
st.table(player_matches_all)