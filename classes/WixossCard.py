import string


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
            image_src_url=None,
            timing=None
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
        self.image_src_url = image_src_url
        self.timing = timing
