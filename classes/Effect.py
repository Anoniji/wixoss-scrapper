import string


class ColorCost:
    def __init__(self, color: string = None, amount: int = None):
        self.color = color
        self.amount = amount


class Effect:
    def __init__(self, effect: string = None, cost: list[ColorCost] = None):
        self.effect = effect
        self.cost = cost

    def hasEffect(self):
        return self.effect is not None
