import undetected_chromedriver as uc

import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def refresh_bch(driver, wait=False):
    if wait:
        time.sleep(5)
    driver.execute_script("localStorage.clear()")
    driver.get("https://bch.games")
    open_dice(driver=driver)

def hard_reset(driver):
    driver.execute_script("localStorage.clear()")
    os.system("mullvad account login 3556952017300720")
    os.system("mullvad disconnect")
    time.sleep(1)
    os.system("mullvad connect")
    time.sleep(10)
    driver.execute_script("window.close()")
    driver.switch_to.window(driver.window_handles[0])
    open_bch(driver=driver)

def open_bch(driver):
    driver.get('https://google.com')
    time.sleep(1)
    driver.execute_script("window.open('https://bch.games','_blank')")
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    open_dice(driver=driver)

def open_dice(driver):
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div[1]/a[5]/div[1]'))).click()
        time.sleep(3)
        bet_dice(driver=driver)
    except:
        time.sleep(5)
        print("resetting program")
        driver.close()
        driver.quit()
        main()

def bet_dice(driver):
    global amount_of_bets
    global current_streak
    global high_score
    current_streak += 1
    amount_of_bets += 1

    print("==================")
    print(f"Amount of bets: {amount_of_bets}\nCurrent streak: {current_streak}\nHigh Score: {high_score}")
    print("==================")

    try:
        if driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[2]/div/div[1]/input') == '15.00000000':
            time.sleep(10)
            refresh_bch(driver=driver)
    except:
        refresh_bch(driver=driver)

    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[3]/button[2]'))).click()
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[3]/button'))).click()
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[3]/button/div[2]'))).click()
    time.sleep(2)

    current_money = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/header/div/a/div").get_attribute("title")

    print(current_money)

    if "loading" in current_money:
        hard_reset(driver=driver)
    
    if current_money != "0.00000000":
        try:
            bet_dice(driver=driver)
        except:
            time.sleep(5)
            refresh_bch(driver=driver)
    elif current_money == "0.10000000":
        while True:
            time.sleep(100000000)
    else:
        if current_streak > high_score:
            high_score = current_streak
        current_streak = 0
        refresh_bch(driver=driver)

def main():
    options = uc.ChromeOptions()
    options.add_argument('--disable-popup-blocking')

    driver = uc.Chrome(options=options)
    open_bch(driver)

if __name__ == "__main__":
    amount_of_bets = 0
    current_streak = 0
    high_score = 0


    main()