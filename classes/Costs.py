from classes.WixossCard import to_dict
from helpers.ClassAsDict import classAsDict


class ColorCost:
    def __init__(self, color, amount):
        self.color = color
        self.amount = amount

    def asDict(self):
        classAsDict(self)

