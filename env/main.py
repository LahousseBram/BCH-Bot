import undetected_chromedriver as uc

import time
import os
from datetime import datetime
import requests
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start_time = datetime.now()
BOT_ID = -1

def reset_program(driver):
    print("resetting program")
    driver.delete_all_cookies()
    driver.close()
    driver.quit()
    os.system("py main.py")
    quit()

def refresh_bch(driver, wait=False):
    if wait:
        time.sleep(5)
    driver.execute_script("localStorage.clear()")
    driver.get("https://bch.games/play/sBNy13Am")
    open_dice(driver=driver)

def hard_reset(driver):
    driver.execute_script("localStorage.clear()")
    os.system("mullvad account login 7931360708700858")
    os.system("mullvad disconnect")
    time.sleep(1)
    os.system("mullvad connect")
    time.sleep(6)
    driver.execute_script("window.close()")
    driver.switch_to.window(driver.window_handles[0])
    open_bch(driver=driver)

def open_bch(driver):
    driver.get('https://google.com')
    time.sleep(1)
    driver.execute_script("window.open('https://bch.games/play/sBNy13Am','_blank')")
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    open_dice(driver=driver)

def open_dice(driver):
    try:
        print("opening dice")
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div[1]/a[5]/div[1]'))).click()
        bet_dice(driver=driver)
    except:
        reset_program(driver=driver)

def bet_dice(driver):
    global amount_of_bets
    global current_streak
    global high_score
    global start_time
    current_streak += 1
    amount_of_bets += 1

    print("==================")
    print(f"Elapsed: {datetime.now() - start_time}\nAmount of bets: {amount_of_bets}\nCurrent streak: {current_streak}\nHigh Score: {high_score}")
    print("==================")

    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[2]/div/div[1]/input')))
        if driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[2]/div/div[1]/input') == '15.00000000':
            time.sleep(5)
            current_streak = 0
            refresh_bch(driver=driver)
    except:
        current_streak = 0
        print("test")
        refresh_bch(driver=driver)

    time.sleep(1)
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[3]/button[2]'))).click()
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[3]/button'))).click()
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[3]/button/div[2]'))).click()
    time.sleep(2)

    current_money = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/header/div/a/div").get_attribute("title")

    URL = "http://94.110.172.3:5000/add-statistic"
    DATA = {
        "bot_id": BOT_ID,
        "current_streak": current_streak,
        "high_score": high_score,
        "current_bet": amount_of_bets
    }
    requests.post(URL, data=DATA)

    print(current_money)

    if "loading" in current_money:
        current_streak = 0
        hard_reset(driver=driver)
    
    if current_money != "0.00000000":
        try:
            bet_dice(driver=driver)
        except:
            time.sleep(5)
            current_streak = 0
            refresh_bch(driver=driver)
    elif current_money == "0.10000000":
        while True:
            print("Goal Reached!")
            time.sleep(100000000)
    else:
        if current_streak > high_score:
            high_score = current_streak
        current_streak = 0
        refresh_bch(driver=driver)

def main():
    options = uc.ChromeOptions()
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--incognito')

    driver = uc.Chrome(options=options)
    open_bch(driver)

if __name__ == "__main__":
    amount_of_bets = 0
    current_streak = 0
    high_score = 0

    art = """
        /$$$$$$$   /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$  /$$$$$$$$
        | $$__  $$ /$$__  $$| $$  | $$| $$__  $$ /$$__  $$|__  $$__/
        | $$  \ $$| $$  \__/| $$  | $$| $$  \ $$| $$  \ $$   | $$   
        | $$$$$$$ | $$      | $$$$$$$$| $$$$$$$ | $$  | $$   | $$   
        | $$__  $$| $$      | $$__  $$| $$__  $$| $$  | $$   | $$   
        | $$  \ $$| $$    $$| $$  | $$| $$  \ $$| $$  | $$   | $$   
        | $$$$$$$/|  $$$$$$/| $$  | $$| $$$$$$$/|  $$$$$$/   | $$   
        |_______/  \______/ |__/  |__/|_______/  \______/    |__/   
                                                                    
    """
    print(art)
    BOT_ID = input("What is the ID for this bot?\n")

    main()