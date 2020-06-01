import pprint as pp
import re
import requests
import datetime
from bs4 import BeautifulSoup

from contextlib import closing
import sqlite3


pr = pp.PrettyPrinter()


def get_parsed_page(url):
    # This fixes a blocked by cloudflare error i've encountered
    headers = {
        "referer": "https://www.hltv.org/stats",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")


with sqlite3.connect("matches.db") as conn:
    cur = conn.cursor()
    cur.execute("""CREATE TABLE matches (match_url text,
                                         team1_url text, team2_url text,
                                         last5_matches1 blob, last5_matches2 blob,
                                         history_h2h blob,
                                         rank1 int, rank2 int,
                                         top30_for_core1 int, top30_for_core2 int,
                                         average_age1 int, average_age2 int,
                                         score1 int, score2 int, total_maps int, star_cell int,
                                         prize_pool int, type_tour text, teams_tour int,
                                         players_age blob, players_info blob)""")
    conn.commit()
    cur.close()



