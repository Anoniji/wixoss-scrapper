import io
import json
import os
import re
import requests
import unicodedata
from PIL import Image
from selenium.webdriver.remote.webelement import WebElement

from classes import WixossCard
from classes.Costs import ColorCost
from classes.card_attributes import COLORS, CardAbilities
from helpers.parseEffects import parse_string


# Card Types
CENTER_LRIG = 'LRIG'
ASSIST_LRIG = 'ASSIST LRIG'
SIGNI = 'SIGNI'
PIECE = 'PIECE'
SPELL = 'SPELL'
PROMO = 'PR'


# Get color from cost, when it is abbreviated with a single character
def get_cost_color(cost_char):
    cost_colors_abbreviated = {
        "B": COLORS.BLACK,
        "U": COLORS.BLUE,
        "G": COLORS.GREEN,
        "R": COLORS.RED,
        "W": COLORS.WHITE,
        "C": COLORS.COLORLESS
    }
    return cost_colors_abbreviated.get(cost_char, cost_char)


# Get Color of card
def get_color(srcString):
    return_color = ''
    for color in COLORS:
        if color.value.casefold() in srcString.casefold():
            return_color = color.name
    return return_color


# Get Colors and their cost from the card, usually for spells and pieces
def get_colors_and_cost(cost_string):
    color_cost_array = cost_string.split(' ')
    parsed_colors_and_cost = []
    if cost_string != '-':
        for color_and_cost in color_cost_array:
            item_pair = color_and_cost.split('×')
            color_from_char = get_cost_color(item_pair[0])
            color = parse_full_width_string(get_color(color_from_char))
            cost = parse_full_width_string(item_pair[1])
            parsed_item_pair = ColorCost(color, cost)
            parsed_colors_and_cost.append(parsed_item_pair)
        return parsed_colors_and_cost
    else:
        return None


# Get Effects Section
    # Effects is effects[0]
    # LifeBurst is effects[1]
    # effects[3] is unknown right now, sig for sanbaka?
    # Cards with effects and lifeburts of '-' will return null instead
def get_effects(effects_and_lifebursts: list[WebElement]):
    if (len(effects_and_lifebursts)) != 0:
        effect = effects_and_lifebursts[0].text
        life_burst = effects_and_lifebursts[1].text
        parsed_effect_array = None
        parsed_life_burst = None
        if effect != '-':
            parsed_effect_array = parse_string(effects_and_lifebursts[0].get_attribute('innerHTML')).split('\n')
        if life_burst != '-':
            parsed_life_burst = parse_string(effects_and_lifebursts[1].get_attribute('innerHTML')).split('\n')

        card_effect = CardAbilities(parsed_effect_array, parsed_life_burst)
        return card_effect


# Parse the string and convert full width to normal
def parse_full_width_string(string):
    return unicodedata.normalize('NFKC', string)


# Convert class to json
def card_to_JSON(card: WixossCard):
    return json.dumps(card.classAsDict())


# Parse the string and convert CJK Chars to csv readable ones
def parse_CJK_chars(string):
    return_string = re.sub(r'\u3011', ']', string)
    return_string = re.sub(r'\u3010', '[', return_string)
    return_string = re.sub(r'\u300b', '', return_string)  # weird double angle bracket
    return_string = re.sub(r'\u300a', '', return_string)
    return return_string


# Parse circled digits, there should be more than 4
def parse_circle_digits(string):
    return_string = re.sub(r'\u2460', '(1)', string)
    return_string = re.sub(r'\u2461', '(2)', return_string)
    return_string = re.sub(r'\u2462', '(3)', return_string)
    return_string = re.sub(r'\u2463', '(4)', return_string)
    return_string = re.sub(r'\u2014', '-', return_string)  # technically not a circle digit but w/e
    return return_string


# Download the image to the specified path
def download_image(download_path, image_URL, file_name):
    image_content = requests.get(image_URL).content
    image_file = io.BytesIO(image_content)
    image = Image.open(image_file)
    file_path = download_path + file_name

    if not os.path.isfile(file_path):
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
        #print('Image Saved')
    else:
        pass
        #print('Image already Exists')
    return file_path


# Check if card exists in data set
def checkIfExists(data, val):
    return any(card['serial']['serialNumber'] == val for card in data['cardData'])