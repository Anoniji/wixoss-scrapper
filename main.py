import json
import os.path
import time
from string import Template

from helpers import card_parsing_functions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from resources.localenv import DRIVER_LOCATION, TAKARATOMY_LINK

if __name__ == '__main__':
    ser = Service(DRIVER_LOCATION)
    ops = webdriver.ChromeOptions()
    #ops.headless = True  # headless causes issues when changing pages
    ops.add_argument('--window-size=1920,1080')
    ops.add_argument('--start-maximized')
    ops.add_argument('--lang=en_US') # Required to make it run headless
    driver = webdriver.Chrome(service=ser, options=ops)
    driver.get(TAKARATOMY_LINK)
    parent_window = driver.window_handles[0]

    # Page Navigation Buttons
    page_buttons = driver.find_elements(By.CSS_SELECTOR, 'div.page-nav div.pure-button')
    next_button = driver.find_element(By.XPATH, '//*[@id="app"]/section/div[2]/div[4]/div[21]')

    jsonPath = './resources/cards.json'

    # pages
    total_pages = 20
    start_page = 20
    pages_to_parse = 1
    for p in range(start_page - 1):
        next_button.click()
        driver.switch_to.window(parent_window)
        time.sleep(3)  # Hate to do it
        wait = WebDriverWait(driver, 60)
        wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div.sec_inner div.card')))

    total_card_count = driver.find_element(By.CSS_SELECTOR, 'p.results').text # wrong?
    current_card_count = (start_page - 1) * 21
    tic = time.perf_counter()
    for i in range(pages_to_parse):
        current_page = start_page + i
        print('Page: ', current_page)
        time.sleep(1)  # Hate to do it
        wait = WebDriverWait(driver, 60)
        wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div.sec_inner div.card')))
        cards = driver.find_elements(By.CSS_SELECTOR, 'div.sec_inner div.card')

        for j in range(1, len(cards)):
            card_to_parse = cards[j]

            # open the card in a new window
            ActionChains(driver) \
                .key_down(Keys.CONTROL) \
                .click(card_to_parse) \
                .key_up(Keys.CONTROL) \
                .perform()

            # switch to newly opened tab, this command switches the driver url`
            driver.switch_to.window(driver.window_handles[1])
            wait = WebDriverWait(driver, 30)
            wait.until(expected_conditions.visibility_of_element_located((By.TAG_NAME, 'dt')))

            # Parsing the card
            card_main_contents = driver.find_element(By.CSS_SELECTOR, 'div.contents_main')
            card_header_contents = driver.find_element(By.CSS_SELECTOR, 'div.contents_header')
            parsed_card = card_parsing_functions.parse_card(card_main_contents, card_header_contents)

            """
                The Json file must be manually deleted after each run during the testing phase
                The except allows you to create a new json file from an empty one
            """
            try:
                with open(jsonPath, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    temp = data["cardData"]
                    temp.append(parsed_card.asDict())
                with open(jsonPath, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(data, indent=4))
            except:
                if os.path.exists(jsonPath):
                    os.remove(jsonPath)
                    print('Starting new Json file')
                with open(jsonPath, "w", encoding='utf-8') as outfile:
                    data = {"cardData": [parsed_card.asDict()]}
                    outfile.write(json.dumps(data, indent=4))
            current_card_count += 1
            current_card_output = Template('Card $current_card_count processed')
            print(current_card_output.substitute(current_card_count=current_card_count))
            # close current tab and go back to parent window
            driver.close()

            # Reset driver to the card list page
            driver.switch_to.window(parent_window)
            #time.sleep(1)  # Hate to do it
            wait = WebDriverWait(driver, 60)
            wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div.contents_main')))

        # Nav to next page
        if current_page != total_pages:
            next_button.click()
            driver.switch_to.window(parent_window)
        else:
            print('All Cards Parsed')
    driver.quit()
    toc = time.perf_counter()
    t = Template('Completed $current_card_count out of $total_card_count')
    print(t.substitute(current_card_count=current_card_count, total_card_count=total_card_count))
    print(f"Program End: Downloaded the cards in {toc - tic:0.4f} seconds")
