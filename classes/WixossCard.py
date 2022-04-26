import json
import string


def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))


class WixossCard:
    def __init__(
            self,
            card_name: string,
            rarity=None,
            card_type=None,
            lrig_type_or_class=None,
            color=None,
            level=None,
            grow_cost=None,
            cost=None,
            limit=None,
            power=None,
            team=None,
            effects=None,
            life_burst=None,
            has_effects=None,
            has_life_burst=None,
            coin=None,
            set_format=None,
            timing=None,
            serial=None,
            image=None
    ):
        self.card_name = card_name
        self.rarity = rarity
        self.card_type = card_type
        self.lrig_type_or_class = lrig_type_or_class
        self.color = color
        self.level = level
        self.grow_cost = grow_cost
        self.cost = cost
        self.limit = limit
        self.power = power
        self.team = team
        self.effects = effects
        self.life_burst = life_burst
        self.has_effects = has_effects
        self.has_life_burst = has_life_burst
        self.coin = coin
        self.set_format = set_format
        self.timing = timing
        self.serial = serial
        self.image = image

    def asDict(self):
        wixossDict = self.__dict__
        wixossDict['serial'] = to_dict(self.serial)
        wixossDict['image'] = to_dict(self.image)
        wixossDict['cost'] = to_dict(self.cost)
        wixossDict['grow_cost'] = to_dict(self.grow_cost)
        return wixossDict
