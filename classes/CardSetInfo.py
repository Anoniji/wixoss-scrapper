from helpers.ClassAsDict import classAsDict

"""
    Card serial numbers are in either form
    WXDi-Dxx-xxx[EN]
    OR
    WXDi-Pxxx[EN]
"""
class CardSetInfo:
    def __init__(self, serialString):
        sections = serialString.split('-')
        self.serialNumber = serialString
        if len(sections) == 3:
            self.formatSet = sections[0]
            self.cardSet = sections[1]
            self.cardNumber = sections[2].replace('[EN]', '')
        else:
            self.formatSet = sections[0]
            self.cardSet = 'Promo'
            self.cardNumber = sections[1].replace('[EN]', '')

    def asDict(self):
        classAsDict(self)
