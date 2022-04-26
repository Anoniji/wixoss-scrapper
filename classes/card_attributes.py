# Attributes for the card
import string
from enum import Enum, unique
from helpers.ClassAsDict import classAsDict


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
    RISE = 'rise'
    ONCE_PER_GAME = 'game_01'
    HARMONY = '[Harmony]'
    USE_CONDITIONS = 'terms_use'


@unique
class COLORS(str, Enum):
    BLACK = 'black'
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'
    WHITE = 'white'
    COLORLESS = 'null'

    def asDict(self):
        classAsDict(self)


class Effect:
    def __init__(self, baseStringEffect: string, effectType, condition, effect, cost):
        self.baseStringEffect = baseStringEffect
        self.effectType = effectType
        self.condition = condition
        self.effect = effect
        self.cost = cost


class CardEffects:
    def __init__(self, effects: list[string] = None, lifeBust: string = None):
        self.effects = effects
        self.lifeBurst = lifeBust


