# Attributes for the card
from enum import Enum, unique


@unique
class CardAttributeLabels(str, Enum):
    CARD_TYPE = 'Card Type'
    LRIG_TYPE_OR_CLASS = 'LRIG Type/Class'
    COLOR = 'Color'
    LEVEL = 'Level'
    GROW_COST = 'Grow Cost'
    COST = 'Cost'
    LIMIT = 'Limit'
    POWER = 'Power'
    TEAM = 'Team'
    COIN = 'Coin'
    FORMAT = 'Format'
    TIMING = 'Timing'


@unique
class CardAbilityKeywords(str, Enum):
    # Card Ability Keywords
    CONST = 'regular'
    ENTER = 'arrival'
    ACTION = 'starting'
    AUTO = 'auto'
    ONCE_PER_TURN = 'turn_01'
    TEAM = 'team'
    GUARD = 'Guard'
    MULTI_ENER = 'Multi Ener'
    LIFE_BURST = 'life burst'
    AUTO_TEAM = 'auto_team'
    ACTION_TEAM = 'starting_team'
    CONSTANT_TEAM = 'regular_team'
    ENTER_TEAM = 'arrival_team'
    TAP = 'down'


@unique
class COLORS(str, Enum):
    BLACK = 'black'
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'
    WHITE = 'white'
    COLORLESS = 'null'


class EffectSymbol:
    def __init__(self, symbolText, position):
        self. symbolText = symbolText
        self. position = position



