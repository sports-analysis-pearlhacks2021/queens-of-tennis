import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


import plotly.graph_objects as go
from plotly import graph_objs as go

# from streamlit_echarts import st_echarts

# from pyecharts import options as opts
# from pyecharts.charts import Bar
# from streamlit_echarts import st_pyecharts

# import plotly.express as px

def parseDate(date):
    date = str(int(date))
    return "{}-{}-{}".format(date[:4], date[4:6], date[6:])

def displayWinLossPie(num_wins, num_losses):
    labels = 'Wins', 'Losses'
    sizes = [num_wins, num_losses]
    colors = ['lightgreen', 'lightcoral']
    explode = (0.1, 0)  # explode 1st slice

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.savefig('./images/pie.png')
    st.image('./images/pie.png')

    # option = {
    #     'title' : {
    #         'text': 'Win/Loss Ratio',
    #         #'subtext': '',
    #         'x':'center'
    #     },
    #     'tooltip' : {
    #         'trigger': 'item',
    #         'formatter': "{b} ({d}%)"
    #     },
    #     # 'legend': {
    #     #     'orient': 'vertical',
    #     #     'left': 'left',
    #     #     'data': ['Wins', 'Losses']
    #     # },
    #     'series' : [{
    #         'name': 'Wins/Losses',
    #         'type': 'pie',
    #         'radius' : '55%',
    #         'center': ['50%', '60%'],
    #         'data':[
    #             {'value':num_wins, 'name':str(num_wins) + ' Wins'},
    #             {'value':num_losses, 'name':str(num_losses) + ' Losses'},
    #         ],
    #         'itemStyle': {
    #             'emphasis': {
    #             'shadowBlur': 10,
    #             'shadowOffsetX': 0,
    #             'shadowColor': 'rgba(0, 0, 0, 0.5)'
    #             }
    #         }
    #     }]
    # }
    # st_echarts(options=option)

def displayTourneysBar():
    pass

def highlight_wins(x):
    if x.winner_name.contains('Mart'):
        return ['background-color: green']*13
    else:
        return ['background-color: white']*13



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
    dob = parseDate(dob)
    country = players.loc[players['player_id'] == player_id, 'country_code'].iloc[0]

    st.header(player)
    st.markdown(f'**Country: ** {country}')
    st.markdown(f'**DOB: ** {dob}')
    st.markdown(f'**Hand: ** {hand}')

    matches_won = matches.loc[matches['winner_id'] == player_id]
    matches_lost = matches.loc[matches['loser_id'] == player_id]
    num_wins = len(matches_won)
    num_losses = len(matches_lost)

    st.subheader('Matches Won')
    st.write(num_wins, ' matches won.')

    st.subheader('Matches Lost')
    st.write(num_losses, ' matches lost.')

    displayWinLossPie(num_wins, num_losses)

    st.subheader('All Matches')
    matches_all = pd.concat([matches_lost, matches_won])
    st.write(len(matches_all), ' matches total.')
    # st.dataframe(matches_all)

    clean_matches_all = pd.DataFrame()

    clean_matches_all['Date'] = matches_all['tourney_date'].apply(parseDate)
    clean_matches_all['Date'] = pd.to_datetime(clean_matches_all['Date'])

    boxplot()
    count()

    # st.table(player_matches_all)

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

    if st.checkbox("View all matches"):
        st.markdown(f'**Won** matches are highlighted in green!')
         # highlight rows where selected player won
        clean_matches_all = clean_matches_all.style.apply(lambda x: ["background: lightgreen" if x.Winner == player else "" for i in x], axis = 1)
        st.dataframe(clean_matches_all)
    else:
        # get the list of columns
        columns = clean_matches_all.columns.tolist()
        st.write("#### Select the columns to display:")
        selected_cols = st.multiselect("", columns)
        if len(selected_cols) > 0:
            selected_df = clean_matches_all[selected_cols]
            # selected_df = selected_df.style.apply(lambda x: ["background: lightgreen" if x.Winner == player else "" for i in x], axis = 1)
            st.dataframe(selected_df)
       
    st.subheader('Tourneys')
    tourneys = matches.loc[matches['winner_id'] == player_id, 'tourney_name']
    displayTourneysBar()
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