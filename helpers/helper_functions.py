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
from classes.card_attributes import COLORS, CardEffects
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
    returnColor = ''
    for color in COLORS:
        if color.value.casefold() in srcString.casefold():
            returnColor = color.name
    return returnColor


# Get Colors and their cost from the card, usually for spells and pieces
def get_colors_and_cost(costString):
    color_cost_array = costString.split(' ')
    parsed_colors_and_cost = []
    if costString != '-':
        for color_and_cost in color_cost_array:
            item_pair = color_and_cost.split('×')
            color = parse_full_width_string(get_cost_color(item_pair[0]))
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
def get_effects(effectsAndLifebursts: list[WebElement]):
    if (len(effectsAndLifebursts)) != 0:
        effect = effectsAndLifebursts[0].text
        lifeBurst = effectsAndLifebursts[1].text
        if effect != '-':
            effect = parse_string(effectsAndLifebursts[0].get_attribute('innerHTML')).split('\n')
        else:
            effect = ['-']
        if lifeBurst != '-':
            lifeBurst = parse_string(effectsAndLifebursts[1].get_attribute('innerHTML')).split('\n')
        cardEffect = CardEffects(effect, lifeBurst)
        return cardEffect


# Parse the string and convert full width to normal
def parse_full_width_string(string):
    return unicodedata.normalize('NFKC', string)


# Convert class to json
def card_to_JSON(card: WixossCard):
    return json.dumps(card.classAsDict())


# Parse the string and convert CJK Chars to csv readable ones
def parse_CJK_chars(string):
    returnString = re.sub(r'\u3011', ']', string)
    returnString = re.sub(r'\u3010', '[', returnString)
    returnString = re.sub(r'\u300b', '', returnString)  # weird double angle bracket
    returnString = re.sub(r'\u300a', '', returnString)
    return returnString


# Parse circled digits, there should be more than 4
def parse_circle_digits(string):
    returnString = re.sub(r'\u2460', '(1)', string)
    returnString = re.sub(r'\u2461', '(2)', returnString)
    returnString = re.sub(r'\u2462', '(3)', returnString)
    returnString = re.sub(r'\u2463', '(4)', returnString)
    returnString = re.sub(r'\u2014', '-', returnString) # technically not a circle digit but w/e
    return returnString


# Download the image to the specified path
def download_image(downloadPath, imageURL, fileName):
    imageContent = requests.get(imageURL).content
    imageFile = io.BytesIO(imageContent)
    image = Image.open(imageFile)
    filePath = downloadPath + fileName

    if not os.path.isfile(filePath):
        with open(filePath, "wb") as f:
            image.save(f, "JPEG")
        #print('Image Saved')
    else:
        pass
        #print('Image already Exists')
    return filePath

