import undetected_chromedriver as uc
import time
import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration settings
BET_AMOUNT = 0.00002
RESET_THRESHOLD = 0.00002
MAX_STREAK = 200

def reset_program(driver):
    logger.info("Resetting program")
    driver.close()
    driver.quit()
    main()

def refresh_bch(driver, wait=False):
    if wait:
        time.sleep(5)
    driver.execute_script("localStorage.clear()")
    driver.get("https://bch.games")
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
    driver.execute_script("window.open('https://bch.games','_blank')")
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)
    open_dice(driver=driver)

def open_dice(driver):
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div[1]/a[5]/div[1]'))).click()
        time.sleep(2)
        bet_dice(driver=driver)
    except Exception as e:
        logger.error(f"Error opening dice: {e}")
        reset_program(driver=driver)

def bet_dice(driver):
    current_streak = 0
    amount_of_bets = 0
    high_score = 0

    while True:
        amount_of_bets += 1
        current_streak += 1

        logger.info("==================")
        logger.info(f"Amount of bets: {amount_of_bets}\nCurrent streak: {current_streak}\nHigh Score: {high_score}")
        logger.info("==================")

        try:
            input_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[2]/div/div[1]/input')
            if input_element.get_attribute("value") == '15.00000000':
                time.sleep(5)
                current_streak = 0
                refresh_bch(driver=driver)
        except Exception as e:
            logger.error(f"Error checking input element: {e}")
            current_streak = 0
            refresh_bch(driver=driver)

        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[3]/button[2]'))).click()
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[4]/div/div/div[3]/button'))).click()
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div/div/main/div/div/div[1]/div/div[3]/button/div[2]'))).click()
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error placing bet: {e}")
            current_streak = 0
            refresh_bch(driver=driver)

        current_money = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/header/div/a/div").get_attribute("title")
        logger.info(f"Current balance: {current_money}")

        if "loading" in current_money:
            current_streak = 0
            hard_reset(driver=driver)

        if float(current_money) < BET_AMOUNT:
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
    main()
