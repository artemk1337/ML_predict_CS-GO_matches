import hltv.main as hltv
import pprint as pp
import requests
import datetime
from bs4 import BeautifulSoup
from re import sub
import re


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
matches = results.find_all('div', {"class": "result-con"})
current_match = matches[0]
match_url = prefix + current_match.find('a', {"class": "a-reset"})['href']
match_page = get_parsed_page(match_url)









