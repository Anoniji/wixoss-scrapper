import re
from classes.card_attributes import COLORS, CardAbilityKeywords
from helpers import helper_functions

innerHTML = """<img src="./images/icon_txt_team.png" class="text_icon"> &lt;Ancient Surprise&gt;
<img src="./images/icon_txt_starting_team.png" class="text_icon"> <img src="./images/icon_txt_turn_01.png" class="text_icon"> <img src="./images/icon_txt_green_00.png" class="text_icon">: Target three SIGNI on your field with different classes get +3000 power until end of turn.
<img src="./images/icon_txt_arrival.png" class="text_icon">: 【Ener Charge 2】. If the cards put into your Ener Zone this way do not share a class, 【Ener Charge 1】."""

teamregex = r'&lt;(.*?)&gt;'
imageregex = r'<.*?>'

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
        case CardAbilityKeywords.RISE:
            symbol = '(RISE)'
        case CardAbilityKeywords.ONCE_PER_GAME:
            symbol = '[Once Per Game]'
        case CardAbilityKeywords.USE_CONDITIONS:
            symbol = '(Use Conditions)'
    return symbol


def fixAngleBrackets(inputString):
    returnString = inputString.replace('&lt;', '<')
    returnString = returnString.replace('&gt;', '>')
    return returnString


def parse_images_in_string(inputString):
    resultImgArray = re.findall(imageregex, inputString, re.I)
    returnString = inputString
    for j in range(len(resultImgArray)):
        imageToSub = resultImgArray[j]
        processedForImage = False
        convertedSymbol = None
        for prefix in CardAbilityKeywords:
            if imageToSub.find(prefix) != -1:
                convertedSymbol = convert_symbol(prefix)
                processedForImage = True
                break
        if not processedForImage:
            for color in COLORS:
                if imageToSub.find(color) != -1:
                    convertedSymbol = convert_color(color)
                    processedForImage = True
                    break
        returnString = returnString.replace(imageToSub, convertedSymbol)
    return returnString


def parse_string(inputString):
    returnString = parse_images_in_string(inputString)
    returnString = helper_functions.parse_CJK_chars(returnString)
    returnString = helper_functions.parse_circle_digits(returnString)
    returnString = fixAngleBrackets(returnString)
    print(returnString)
    return returnString



