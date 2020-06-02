import pprint as pp
import requests
import datetime
from bs4 import BeautifulSoup
from re import sub
import re
import numpy as np
import pandas as pd

import pickle as pk
import sqlite3


pr = pp.PrettyPrinter()
prefix = 'https://www.hltv.org'
max_rank = 1000


def get_parsed_page(url):
    # This fixes a blocked by cloudflare error i've encountered
    headers = {
        "referer": "https://www.hltv.org/stats",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")


results = get_parsed_page('https://www.hltv.org/results')

# list of matches
matches = results.find('div', {"class": "results-all", 'data-zonedgrouping-group-classes': "results-sublist"}).\
    find_all('div', {"class": "result-con"})


def get_teams_url(match_page):
    return [prefix + match_page.find_all('div', {"class": "team"})[0].find('a')['href'],
            prefix + match_page.find_all('div', {"class": "team"})[1].find('a')['href']]


# get score
def get_score(current_match):
    return [int(i.text) for i in current_match.find('td', {'class': 'result-score'}).find_all('span')]


# get total_maps
def get_total_maps(current_match):
    return current_match.find('td', {'class': 'star-cell'}).find('div', {'class': 'map-text'}).text


# get star_cell
def get_star_cell(current_match):
    try:
        return len(current_match.find('td', {'class': 'star-cell'}).find_all('i', {'class': 'star'}))
    except Exception:
        print('None stars')
        return 0


# get history_h2h
def get_history_h2h(match_page):
    return [int(i.find('div', {'class': 'bold'}).text) for i in match_page.find_all('div', {'class': 'flexbox-center'})]


# get teams_rank
def get_team_rank(team):
    try:
        return max_rank - int(team.find('div', {'class': 'profile-team-stats-container'}).
                              find_all('span', {'class': "right"})[0].text[1:])
    except:
        return 0


# get teams_top30_for_core
def get_top30_for_core(team):
    try:
        return int(team.find('div', {'class': 'profile-team-stats-container'}).
                   find_all('span', {'class': "right"})[1].text)
    except Exception as e:
        return 0


# get average_ages
def get_ave_age(team):
    try:
        return float(team.find('div', {'class': 'profile-team-stats-container'}).
                     find_all('span', {'class': "right"})[2].text)
    except Exception as e:
        return 0


# get prize_pool
def get_prize_pool(event_page):
    try:
        return int(sub(r'[^\d.]', '', event_page.find('td', {'class': 'prizepool'}).text))
    except:
        return 0


# get teams_on_tour
def get_teams_on_tour(event_page):
    return int(re.findall(r"[-+]?\d*\.\d+|\d+", event_page.find('td', {'class': 'teamsNumber'}).text)[0])


# get type_of_tour
def get_type_tour(event_page):
    tmp = event_page.find('td', {'class': 'location'}).find('span').text
    return [i for i in re.split('\(|\)| ', tmp) if i is not ''][-1]


# get last_5_matches
def get_last5_matches(match_page):
    def get_url_opponent(url1, i):
        return prefix + url1.find_all('tr', {'class': 'table'})[i].find('a', {'class': 'text-ellipsis'})['href']

    def get_type_match(url1, i):
        return url1.find_all('tr', {'class': 'table'})[i].find('a').text

    def get_score_array(url1, i):
        return [int(k) for k in
                url1.find_all('tr', {'class': 'table'})[i].find('td', {'class': 'spoiler'}).text.split(' - ')]

    def get_all(array, table, k):
        for i in range(5):
            try:
                array += [get_type_match(table[k], i),
                          get_url_opponent(table[k], i),
                          get_team_rank(get_parsed_page(get_url_opponent(table[k], i))),
                          *get_score_array(table[k], i)]
            except:
                array += [None, None, 0, 0, 0]
        return array

    table_last5_matches = (match_page.find('div', {'class': 'past-matches'}).
                           find_all('div', {'class': 'half-width'}))
    last5_matches1 = []
    last5_matches2 = []
    last5_matches1 = get_all(last5_matches1, table_last5_matches, 0)
    last5_matches2 = get_all(last5_matches2, table_last5_matches, 1)
    return last5_matches1, last5_matches2


def get_players(team):
    return team.find('div', {'class': 'bodyshot-team'}).find_all('a')


def get_players_from_match(match):
    return [[i.find('a') for i in k.find_all('td', {'class': 'player'})]
            for k in match.find_all('div', {'class': 'lineup standard-box'})]


def get_player_stat(player_profile):
    stats = []
    for i in range(6):
        tmp = player_profile.find('div', {'class': 'tab-content'}). \
            find_all('div', {'class': 'cell'})[i]. \
            find('span', {'class': 'statsVal'}).text
        if tmp[-1] == '%':
            tmp = float(tmp[:-1]) / 100
        else:
            tmp = float(tmp)
        stats += [tmp]
    return stats


def get_player_age(player_profile):
    try:
        return int(''.join(
            i for i in re.findall('.* years', player_profile.find('div', {'class': 'playerProfile'}).text)[0] if
            i.isdigit()))
    except:
        return 0


# get players stats and age
def get_players_stat_and_age(team):
    players = get_players(team)
    ages = []
    players_stat = []
    for pl in players:
        player_profile = get_parsed_page(prefix + pl['href'])
        players_stat += [*get_player_stat(player_profile)]
        ages += [get_player_age(player_profile)]
    return ages, players_stat


# get players stats and age from match
def get_players_stat_and_age_from_match(match_page):
    players_all = get_players_from_match(match_page)
    ages = []
    players_stat = []
    for players in players_all:
        for pl in players[:5]:
            player_profile = get_parsed_page(prefix + pl['href'])
            players_stat += [*get_player_stat(player_profile)]
            ages += [get_player_age(player_profile)]
    return ages, players_stat


# <=============== FORMATTING ===============> #


def create_vec_features(current_match):
    match_url = prefix + current_match.find('a', {"class": "a-reset"})['href']  # to DB
    match_page = get_parsed_page(match_url)
    event_page = get_parsed_page(prefix + match_page.find('div', {'class': 'event'}).find('a')['href'])
    teams_pages = [get_parsed_page(i) for i in get_teams_url(match_page)]
    team1_url, team2_url = get_teams_url(match_page)  # to DB

    last5_matches1, last5_matches2 = get_last5_matches(match_page)  # to DB

    history_h2h = get_history_h2h(match_page)  # to DB

    rank1, rank2 = get_team_rank(teams_pages[0]), get_team_rank(teams_pages[1])  # to DB

    top30_for_core1, top30_for_core2 = get_top30_for_core(teams_pages[0]), get_top30_for_core(teams_pages[1])  # to DB

    average_age1, average_age2 = get_ave_age(teams_pages[0]), get_ave_age(teams_pages[1])  # to DB

    score1, score2 = get_score(current_match)

    total_maps, star_cell = get_total_maps(current_match), get_star_cell(current_match)  # to DB

    prize_pool, type_tour, teams_tour = get_prize_pool(event_page),\
                                        get_type_tour(event_page),\
                                        get_teams_on_tour(event_page)

    players_age, players_info = get_players_stat_and_age_from_match(match_page)

    return np.array([match_url, team1_url, team2_url, *last5_matches1, *last5_matches2, *history_h2h,
            rank1, rank2, top30_for_core1, top30_for_core2, average_age1, average_age2,
            score1, score2, total_maps, star_cell, prize_pool, type_tour, teams_tour,
            *players_age, *players_info])


header = ['match_url', 'team1_url', 'team2_url',
          *[f'5last_matches1_{k}_{i}' for k in range(5) for i in range(5)],
          *[f'5last_matches2_{k}_{i}' for k in range(5) for i in range(5)],
          'history_h2h_1win', 'history_h2h', 'history_h2h_2win',
          'rank1', 'rank2', 'top30_for_core1', 'top30_for_core2', 'average_age1', 'average_age2',
          'score1', 'score2', 'total_maps', 'star_cell', 'prize_pool', 'type_tour', 'teams_tour',
          *[f'player{i}_age' for i in range(10)], *[f'player{k}_stat_{i}' for k in range(10) for i in range(6)]]


len_head = len(header)
data = [np.array(header)]
print(data)


for i in range(10):
    if i == 0:
        results = get_parsed_page('https://www.hltv.org/results')
    else:
        results = get_parsed_page(f'https://www.hltv.org/results?offset={i}00')
    # list of matches
    matches = results.find('div', {"class": "results-all", 'data-zonedgrouping-group-classes': "results-sublist"}). \
        find_all('div', {"class": "result-con"})
    for k in range(len(matches)):
        print(i*100 + k)
        try:
            tmp = create_vec_features(matches[k])
            if len_head == len(tmp):
                data.append(tmp)
        except Exception as e:
            print(e)


data = np.array(data)
print(data)
df = pd.DataFrame(data=data[1:,:], columns=data[0, :])
df.to_csv('df.csv')


# https://www.hltv.org/results?offset=100



