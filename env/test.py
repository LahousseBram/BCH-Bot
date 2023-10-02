import sys, os, psutil, logging, requests

current_streak = 0
high_score = 1
amount_of_bets = 1

URL = "http://94.110.172.3:5000/add-statistic"
PARAMS = {
    "current_streak": current_streak,
    "high_score": high_score,
    "current_bet": amount_of_bets
}
requests.post(URL, params=PARAMS)