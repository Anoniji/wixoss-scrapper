import string

from classes.WixossCard import WixossCard
from classes.CardSetInfo import CardSetInfo
from classes.card_attributes import CardAttributeLabels, CardEffects

from helpers import helper_functions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def parse_card(mainContents: WebElement, contentHeader: WebElement):
    imageDownloadPath = 'resources/cardImages/'
    # Name of Card
    cardNameWithSerial = contentHeader.find_element(By.CSS_SELECTOR, 'div.sec_inner h2').text
    serialNumber = contentHeader.find_element(By.CSS_SELECTOR, 'div.sec_inner h2 span').text
    cardName = cardNameWithSerial.replace(serialNumber, "").replace('\n', "")
    cardName = cardName.replace('\u266f', "#")
    rarity = contentHeader.find_element(By.CSS_SELECTOR, 'p.rarelity').text

    # Card Image
    thumbNail = mainContents.find_element(By.CSS_SELECTOR, 'div.imageBox img').get_attribute('src')
    filepath = helper_functions.download_image(imageDownloadPath, thumbNail, serialNumber + '.jpg')

    parsed_card = WixossCard(card_name=cardName, rarity=rarity)
    parsed_card.image_src_url = thumbNail
    parsed_card.image_path = filepath
    parsed_card.serial = CardSetInfo(serialNumber)

    # list of tags, and their values in separate arrays
    descTags = mainContents.find_elements(By.TAG_NAME, 'dt')
    descTagValues = mainContents.find_elements(By.TAG_NAME, 'dd')

    # This determines the type of card it is
    cTValue = descTagValues[0].text

    # Effects Section
    effectsAndLifeBursts = mainContents.find_elements(By.TAG_NAME, 'div.fullWidth')

    get_card_info(parsed_card, descTags, descTagValues, cTValue)

    card_effects = helper_functions.get_effects(effectsAndLifeBursts)
    assign_abilities(parsed_card, card_effects)
    return parsed_card


# Generic card info
def get_card_info(parsed_card: WixossCard, descTags: list[WebElement], descTagValues: list[WebElement], cTValue: string):
    for i in range(0, len(descTags)):
        cardAttributeLabel = descTags[i].text
        tagValuesConverted = helper_functions.parse_CJK_chars(descTagValues[i].text) # TODO: Make it so the values are parsed for full width and CJK, 2 functions
        tagValuesConverted = helper_functions.parse_full_width_string(tagValuesConverted)
        # make this a switch statement
        if i == 1:
            #cardAttributeValue = helper_functions.parse_full_width_string(descTagValues[i].text)
            cardAttributeValue = helper_functions.parse_full_width_string(tagValuesConverted)
        elif i == 2:
            colorSrcValue = descTagValues[2].find_elements(By.TAG_NAME, 'img')
            colorCount = len(colorSrcValue)
            cardAttributeValue = ''
            if len(colorSrcValue) > 1:
                for j in range(0, colorCount):
                    cardAttributeValue += helper_functions.get_color(colorSrcValue[j].get_attribute('src'))
                    if j != colorCount - 1:
                        cardAttributeValue += ';'
            else:
                cardAttributeValue = helper_functions.get_color(colorSrcValue[0].get_attribute('src'))
        elif i == 4:
            # else its the 4th index which is the grow cost one
            if cTValue == helper_functions.CENTER_LRIG or cTValue == helper_functions.ASSIST_LRIG:
                colorSrcValue = descTagValues[4].find_element(By.TAG_NAME, 'img')
                growColor = helper_functions.get_color(colorSrcValue.get_attribute('src'))
                growCost = descTagValues[4].text.replace('×', '', 1)
                growCost = str(int(growCost))
                cardAttributeValue = growColor + ' x ' + growCost
        elif i == 5:
            # Cost which has a value of << color >> x # which isn't supported in csv and full width digits
            #cardAttributeValue = helper_functions.get_colors_and_cost(descTagValues[i].text)
            cardAttributeValue = helper_functions.get_colors_and_cost(tagValuesConverted)
            cardAttributeValue = helper_functions.parse_full_width_string(cardAttributeValue)
        elif i == 6:
            # Limit which as full width digits that cant be written to csv
            #cardAttributeValue = helper_functions.parse_full_width_string(descTagValues[i].text)
            cardAttributeValue = helper_functions.parse_full_width_string(tagValuesConverted)
        else:
            #cardAttributeValue = descTagValues[i].text
            cardAttributeValue = tagValuesConverted

        assign_attribute(parsed_card, cardAttributeLabel, cardAttributeValue)


# Assign attributes based on the value
def assign_attribute(parsed_card: WixossCard, cardAttributeLabel: string, cardAttributeValue: string):
    match cardAttributeLabel:
        case CardAttributeLabels.CARD_TYPE:
            parsed_card.card_type = cardAttributeValue
        case CardAttributeLabels.LRIG_TYPE_OR_CLASS:
            parsed_card.lrig_type_or_class = cardAttributeValue
        case CardAttributeLabels.COLOR:
            parsed_card.color = cardAttributeValue
        case CardAttributeLabels.LEVEL:
            parsed_card.level = cardAttributeValue
        case CardAttributeLabels.GROW_COST:
            parsed_card.grow_cost = cardAttributeValue
        case CardAttributeLabels.COST:
            parsed_card.cost = cardAttributeValue
        case CardAttributeLabels.LIMIT:
            parsed_card.limit = cardAttributeValue
        case CardAttributeLabels.POWER:
            parsed_card.power = cardAttributeValue
        case CardAttributeLabels.TEAM:
            parsed_card.team = cardAttributeValue
        case CardAttributeLabels.COIN:
            parsed_card.coin = cardAttributeValue
        case CardAttributeLabels.TIMING:
            parsed_card.timing = cardAttributeValue
        case CardAttributeLabels.FORMAT:
            parsed_card.set_format = cardAttributeValue


# Assign the effects and life burst to the card
def assign_abilities(parsed_card: WixossCard, card_effects: CardEffects):
    if card_effects.effects[0] != '-':
        parsed_card.has_effects = True
    else:
        parsed_card.has_effects = False
    if card_effects.lifeBurst != '-':
        parsed_card.has_life_burst = True
    else:
        parsed_card.has_life_burst = False

    parsed_card.effects = card_effects.effects
    parsed_card.life_burst = card_effects.lifeBurst


# Sanitize the Values
"""
Idea here is that the values obtained when parsing a card aren't always clean.  And to clean them within
the encapsulating parse function could get ugly.

schema:
    inputs: 
        -an array that contains information
        -what type of card it is
    outputs:
        an object of the type the card is with clean attributes that are usable for a database
"""
def sanitize_card_data(array):
    print('TO DO')




