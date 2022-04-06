import card_parsing_functions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from helpers import helper_functions
import csv

from resources.localenv import DRIVER_LOCATION, TAKARATOMY_LINK

if __name__ == '__main__':
    ser = Service(DRIVER_LOCATION)
    ops = webdriver.ChromeOptions()
    #ops.headless = True  # headless causes issues when changing pages
    ops.add_argument('--window-size=1920,1080')
    ops.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=ser, options=ops)
    driver.get(TAKARATOMY_LINK)

    # Parent window
    parentWindow = driver.window_handles[0]

    # Page Navigation Buttons
    pageButtons = driver.find_elements(By.CSS_SELECTOR, 'div.page-nav div.pure-button')
    nextButton = driver.find_element(By.XPATH, '//*[@id="app"]/section/div[2]/div[4]/div[21]')

    csvPath = './resources/cards.csv'
    file = open(csvPath, 'w', newline="")
    headers = (['card_name',
                'rarity',
                'card_type',
                'lrig_type_or_class',
                'color',
                'level',
                'grow_cost',
                'cost',
                'limit',
                'power',
                'team',
                'timing',
                'effects',
                'life_burst',
                'has_effects',
                'has_life_burst',
                'coin',
                'set_format',
                'image_src_url'])
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()

    # For loop
    #for i in range(0, len(pageButtons)):
    for i in range(0, 3):
        print('iteration: ', i)
        wait = WebDriverWait(driver, 30)
        wait.until(expected_conditions.visibility_of_any_elements_located((By.CSS_SELECTOR, 'div.sec_inner div.card')))
        cards = driver.find_elements(By.CSS_SELECTOR, 'div.sec_inner div.card')

        for j in range(1, len(cards)):
        #for j in range(14, 17):
            print('card: ', j)
            cardToParse = cards[j]

            # open the card in a new window
            ActionChains(driver) \
                .key_down(Keys.CONTROL) \
                .click(cardToParse) \
                .key_up(Keys.CONTROL) \
                .perform()

            # switch to newly opened tab, this command switches the driver url`
            driver.switch_to.window(driver.window_handles[1])
            wait = WebDriverWait(driver, 30)
            wait.until(expected_conditions.visibility_of_element_located((By.TAG_NAME, 'dt')))

            # Parsing the card
            cardMainContents = driver.find_element(By.CSS_SELECTOR, 'div.contents_main')
            cardHeaderContents = driver.find_element(By.CSS_SELECTOR, 'div.contents_header')
            parsedCard = card_parsing_functions.parse_card(cardMainContents, cardHeaderContents)
            cardAsJSON = helper_functions.card_to_JSON(parsedCard)
            #print(cardAsJSON)

            # TODO: Write the card to the csv file
            writer.writerow(parsedCard.__dict__)

            # close current tab and go back to parent window
            driver.close()

            # Reset driver to the card list page
            driver.switch_to.window(parentWindow)
            wait = WebDriverWait(driver, 30)
            wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div.contents_main')))
            #print('------------------')

        # Nav to next page
        nextButton.click()
        driver.switch_to.window(parentWindow)

    # TODO: Close the CSV File
    file.close()
    driver.quit()
