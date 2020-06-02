import pprint as pp
import re
import requests
import datetime
from bs4 import BeautifulSoup
import numpy as np
from catboost import CatBoostClassifier


import sqlite3
import pickle as pk


with sqlite3.connect("matches.db") as conn:
    cur = conn.cursor()
    cur.execute("""SELECT * FROM matches""")
    data = []
    for (match_url, team1_url, team2_url, last5_matches1, last5_matches2, history_h2h, rank1, rank2,\
        top30_for_core1, top30_for_core2, average_age1, average_age2, score1, score2, total_maps, star_cell,\
        prize_pool, type_tour, teams_tour, players_age, players_info) in cur:
        last5_matches1, last5_matches2 = pk.loads(last5_matches1), pk.loads(last5_matches2)
        history_h2h = pk.loads(history_h2h)
        players_age, players_info = pk.loads(players_age), pk.loads(players_info)
        data.append(np.asarray([match_url, team1_url, team2_url, *last5_matches1, *last5_matches2, *history_h2h, rank1, rank2,\
        top30_for_core1, top30_for_core2, average_age1, average_age2, score1, score2, total_maps, star_cell,\
        prize_pool, type_tour, teams_tour, *players_age, *players_info]))
    cur.close()


data = np.asarray(data)[:, 5:]
print(data[0])
new = data[:, 0]
print(new[0])
for i in range(1, data.shape[-1]):
    try:
        tmp = data[:, i].astype(float)
        new = np.concatenate((new, tmp))
    except Exception as e:
        print(e)
        pass

print(new[0])



