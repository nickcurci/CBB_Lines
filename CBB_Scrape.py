import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.vegasinsider.com/college-basketball/odds/las-vegas/money/"
soup = BeautifulSoup(requests.get(url).content, "html.parser")

# clean-up the cells:
for br in soup.select("br"):
    br.replace_with("\n")

base = pd.read_html(str(soup.select_one(".frodds-data-tbl")))[0]

# set column names:
base.columns = ['Matchup', 'VI_Open',
              'VI_Consensus', 'BET_MGM',
              'Ceasars', 'FanDuel',
              'DraftKings', 'PointsBet',
              'WynnBet', 'Superbook']

base.to_csv("/Users/nicholascurci/Downloads/basedata.csv", index=False)
print(base)


# top 25 teams
import re

url = 'https://www.cbssports.com/college-basketball/rankings/ap/'
soup = BeautifulSoup(requests.get(url).content, "html.parser")

# clean-up the cells:
for br in soup.select("br"):
    br.replace_with("\n")

t25 = pd.read_html(str(soup.select_one(".TableBase-overflow")))[0]
# # set column names:
t25.columns = ['Rank', 'Team',
              'Trend', 'Points', 'Blank',
              'Next Game', 'Opponent']
t25.to_csv("/Users/nicholascurci/Downloads/top25data.csv", index=False)
top25 = t25['Team'].tolist()
top25list = []
for team in top25:
    team = re.split(r'(\d+)', team)
    team = team[0]
    team = team.split('(', 1)
    team = team[0].rstrip()
    top25list.append(team)
print(top25list)

# featured games
import numpy as np

def match(x):
    for i in top25list:
        if i.lower() in x.lower():
            return i
    else:
        return np.nan

featured = base[base['Matchup'].apply(match).notna()]
print(featured)

import datetime
today = datetime.datetime.today().strftime('%m/%d')
print(today)

featuredfinal = featured[featured["Matchup"].str.contains(today)==True]

featuredfinal = featuredfinal.drop(featuredfinal.columns.difference(['Matchup', 'DraftKings']), axis=1)

featuredfinal['Matchup'] = featuredfinal['Matchup'].str.split(n=4).str[-1]
featuredfinal['Matchup'] = featuredfinal['Matchup'].str.replace('\d+', '@')
featuredfinal.to_csv("/Users/nicholascurci/Downloads/featuredfinal.csv", index=False)
print(featuredfinal)

# send in telegram
TOKEN = '5111519988:AAG2VqyfR0wgNfnfsWoKy1UAuqR4hw62dCs' # token to access the HTTP API of your bot created with @BotFather
CHANNEL_ID = -1001640287624 # id of your channel, for example @durov
from telegram import Bot
bot = Bot(TOKEN)


#Create the message
code_html=''
if featuredfinal.empty == False:
    for i in range(len(featuredfinal)):
        code_html=code_html + '\n\n Matchup: ' + str((featuredfinal['Matchup'].iloc[i])) +'\n DraftKings: ' + str((featuredfinal['DraftKings'].iloc[i]))
print(code_html)
# featuredfinal.to_html('featuredfinal.html')
# with open('featuredfinal.html', 'rb') as fme:
bot.send_message(CHANNEL_ID, text=f'Featured CBB Match Ups {today}: {code_html}')

