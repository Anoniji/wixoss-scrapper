import json
import re


# Colors
import unicodedata
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from classes import WixossCard
from helpers.card_attributes import CardAbilityKeywords, EffectSymbol, COLORS




# TODO: DELETE THIS
BLACK = 'black'
BLUE = 'blue'
GREEN = 'green'
RED = 'red'
WHITE = 'white'
COLORLESS = 'null'

# Card Types
CENTER_LRIG = 'LRIG'
ASSIST_LRIG = 'ASSIST LRIG'
SIGNI = 'SIGNI'
PIECE = 'PIECE'
SPELL = 'SPELL'
PROMO = 'PR'

# TODO: DELETE THIS
colors = [BLACK, BLUE, GREEN, RED, WHITE, COLORLESS]


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
            returnColor = color
    return returnColor


# Get Colors and their cost from the card, usually for spells and pieces
def get_colors_and_cost(costString):
    color_cost_array = costString.split(' ')
    parsed_colors_and_cost = ''
    if costString != '-':
        for color_and_cost in color_cost_array:
            item_pair = color_and_cost.split('×')
            #color_char_without_brackets = item_pair[0].replace('《', '', 1).replace('》', '', 1)
            #color = get_cost_color(color_char_without_brackets)
            color = get_cost_color(item_pair[0])
            cost = item_pair[1]
            parsed_item_pair = color + ' x ' + cost
            if len(parsed_colors_and_cost) > 0:
                parsed_colors_and_cost += ';'
            parsed_colors_and_cost += parsed_item_pair
        return parsed_colors_and_cost
    else:
        return costString


# Get Effects Section
    # Effects is effects[0]
    # LifeBurst is effects[1]
    # effects[3] is unknown right now, sig for sanbaka?
    # TODO: Effects will have to have further parsing to detect images such as "TEAM" "AUTO" "TAP" "ONCE PER TURN" ETC
def get_effects(effectsAndLifebursts: list[WebElement]):
    effectsArray = []
    if (len(effectsAndLifebursts)) != 0:
        effect = effectsAndLifebursts[0].text
        lifeBurst = effectsAndLifebursts[1].text

        if effect != '-':
            effect = parse_effects(effectsAndLifebursts[0])
            #effect = re.sub(r': ', '', effect)
            #effect = re.sub(r'\u3010', '[', effect)  # Kept as a redundancy
            #effect = re.sub(r'\u3011', ']', effect)  # Kept as a redundancy
        if lifeBurst != '-':
            lifeBurst = parse_effects(effectsAndLifebursts[1])
        effectsArray.append(effect)
        effectsArray.append(lifeBurst)
    return effectsArray


# Effects shouldn't have full width symbols, usually only CJK and circled digits
def parse_effects(string: WebElement):
    returnString = parse_symbols(string)
    returnString = parse_CJK_chars(returnString)
    returnString = parse_circle_digits(returnString)
    return returnString


# Convert image symbols for certain effects (Auto, team, once per turn, etc)
def parse_symbols(effects: WebElement):
    parsedString = ''
    images = effects.find_elements(By.CSS_SELECTOR, '*')
    # Convert the images to text
    prefixArray = []
    for i in range(0, len(images)):
        symbolImageUrl = images[i].get_attribute('src')
        for prefix in CardAbilityKeywords:
            if symbolImageUrl.find(prefix) != -1:
                convertedSymbol = convert_symbol(prefix)
                if convertedSymbol.startswith('['):
                    convertedPrefix = EffectSymbol(convertedSymbol, 'middle')
                else:
                    convertedPrefix = EffectSymbol(convertedSymbol, 'start')
                prefixArray.append(convertedPrefix)
                continue
        for color in COLORS:
            if symbolImageUrl.find(color) != -1:
                convertedColor = EffectSymbol(convert_color(color), 'end')
                prefixArray.append(convertedColor)
                continue
    # Get the text
    text = effects.text
    splitText = text.split('\n')
    for j in range(0, len(splitText)):
        if len(prefixArray) >= 1:
            effectText = splitText[j].lstrip().rstrip()
            parsedString += prefixArray[0].symbolText
            prefixArray.pop(0)
            while len(prefixArray) >= 1 and prefixArray[0].position != 'start':
                parsedString += prefixArray[0].symbolText
                prefixArray.pop(0)
            parsedString += effectText
            if j != len(splitText)-1:
                parsedString += ';'
    if parsedString == '':
        parsedString = text
    return parsedString


def convert_color(color: COLORS):
    symbol = ''
    match color:
        case COLORS.BLACK:
            symbol = '(Blk)'
        case COLORS.BLUE:
            symbol = '(Blu)'
        case COLORS.GREEN:
            symbol = '(Grn)'
        case COLORS.RED:
            symbol = '(Red)'
        case COLORS.WHITE:
            symbol = '(Wht)'
        case COLORS.COLORLESS:
            symbol = '(Any)'
    return symbol

# Map the keyword enum to a text friendly conversion
def convert_symbol(keyword: CardAbilityKeywords):
    symbol = ''
    match keyword:
        case CardAbilityKeywords.CONST:
            symbol = '(CONST)'
        case CardAbilityKeywords.ENTER:
            symbol = '(ENTER)'
        case CardAbilityKeywords.ACTION:
            symbol = '(ACTION)'
        case CardAbilityKeywords.AUTO:
            symbol = '(AUTO)'
        case CardAbilityKeywords.ONCE_PER_TURN:
            symbol = '[Once]'
        case CardAbilityKeywords.TEAM:
            symbol = '(TEAM)'
        case CardAbilityKeywords.AUTO_TEAM:
            symbol = '(TEAM AUTO)'
        case CardAbilityKeywords.ACTION_TEAM:
            symbol = '(TEAM ACTION)'
        case CardAbilityKeywords.CONSTANT_TEAM:
            symbol = '(TEAM CONST)'
        case CardAbilityKeywords.ENTER_TEAM:
            symbol = '(TEAM ENTER)'
        case CardAbilityKeywords.TAP:
            symbol = '[TAP CARD]'
    return symbol


# Parse the string and convert full width to normal
def parse_full_width_string(string):
    return unicodedata.normalize('NFKC', string)


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
    return returnString

# Timing TODO: This is obs
def get_timing(descTags: list[WebElement], descTagValues: list[WebElement]):
    timing = descTags[9].text
    timingValue = descTagValues[9].text
    #print(timing, ' | ', timingValue)


# Convert class to json
def card_to_JSON(card: WixossCard):
    return json.dumps(card.__dict__)
