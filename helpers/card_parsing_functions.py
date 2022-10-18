import string

from classes.Image import Image
from classes.WixossCard import WixossCard
from classes.CardSetInfo import CardSetInfo
from classes.card_attributes import CardAttributeLabels, CardAbilities, Ability, CardAbilityKeywords
from classes.Costs import ColorCost

from helpers import helper_functions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def parse_card(main_contents: WebElement, content_header: WebElement):
    image_download_path = 'resources/cardImages/'

    rarity = main_contents.find_element(By.CSS_SELECTOR, 'p.rarelity').text
    card_name_with_serial = content_header.find_element(By.CSS_SELECTOR, 'div.sec_inner h2').text
    serial_number = content_header.find_element(By.CSS_SELECTOR, 'div.sec_inner h2 span').text
    card_name = card_name_with_serial.replace(serial_number, "").replace('\n', "")

    # Card Image
    thumb_nail_url = main_contents.find_element(By.CSS_SELECTOR, 'div.imageBox img').get_attribute('src')
    file_path = helper_functions.download_image(image_download_path, thumb_nail_url, serial_number + '.jpg')

    # Begin the new Card class
    parsed_card = WixossCard(card_name=card_name, rarity=rarity)
    parsed_card.image = Image(thumb_nail_url, file_path)
    parsed_card.serial = CardSetInfo(serial_number)

    # list of tags, and their values in separate arrays
    desc_tags = main_contents.find_elements(By.TAG_NAME, 'dt')
    desc_tag_values = main_contents.find_elements(By.TAG_NAME, 'dd')

    # Determine the type of card it is and get the meat
    card_type_value = desc_tag_values[0].text
    get_card_info(parsed_card, desc_tags, desc_tag_values, card_type_value)

    # Effects Section
    effects_and_life_bursts = main_contents.find_elements(By.TAG_NAME, 'div.fullWidth')
    card_effects = helper_functions.get_effects(effects_and_life_bursts)
    assign_abilities(parsed_card, card_effects)
    return parsed_card


# Generic card info
def get_card_info(parsed_card: WixossCard, desc_tags: list[WebElement], desc_tag_values: list[WebElement],
                  card_type_value: string):
    for i in range(0, len(desc_tags)):
        card_attribute_label = desc_tags[i].text
        tag_values_converted = helper_functions.parse_CJK_chars(desc_tag_values[i].text)
        tag_values_converted = helper_functions.parse_full_width_string(tag_values_converted)
        # make this a switch statement
        if i == 1:
            card_attribute_value = helper_functions.parse_full_width_string(tag_values_converted)
        elif i == 2:
            color_src_value = desc_tag_values[2].find_elements(By.TAG_NAME, 'img')
            color_count = len(color_src_value)
            card_attribute_value = []
            if len(color_src_value) > 1:
                for j in range(0, color_count):
                    card_attribute_value.append(helper_functions.get_color(color_src_value[j].get_attribute('src')))
            else:
                card_attribute_value = helper_functions.get_color(color_src_value[0].get_attribute('src'))
        elif i == 4:
            # else its the 4th index which is the grow cost one
            if card_type_value == helper_functions.CENTER_LRIG or card_type_value == helper_functions.ASSIST_LRIG:
                color_src_value = desc_tag_values[4].find_element(By.TAG_NAME, 'img')
                grow_color = helper_functions.get_color(color_src_value.get_attribute('src'))
                grow_cost = desc_tag_values[4].text.replace('×', '', 1)
                grow_cost = str(int(grow_cost))
                grow_cost_object = ColorCost(grow_color, grow_cost)
                card_attribute_value = grow_cost_object
            else:
                card_attribute_value = None
        elif i == 5:
            # Cost which has a value of << color >> x # which isn't supported in csv and full width digits
            card_attribute_value = helper_functions.get_colors_and_cost(tag_values_converted)
        elif i == 6:
            # Limit which as full width digits that cant be written to csv
            card_attribute_value = helper_functions.parse_full_width_string(tag_values_converted)
        else:
            if tag_values_converted == '-':
                tag_values_converted = None
            card_attribute_value = tag_values_converted

        assign_attribute(parsed_card, card_attribute_label, card_attribute_value)


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
def assign_abilities(parsed_card: WixossCard, card_effects: CardAbilities):
    effect = Ability(card_effects.effects, CardAbilityKeywords.EFFECT)
    life_burst = Ability(card_effects.life_burst, CardAbilityKeywords.LIFE_BURST)
    parsed_card.effects = effect if effect.ability is not None else None
    parsed_card.life_burst = life_burst if life_burst.ability is not None else None
