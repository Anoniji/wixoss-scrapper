class CardSetInfo:
    def __init__(self, serialString):
        sections = serialString.split('-')
        self.serialNumber = serialString
        self.formatSet = sections[0]
        self.cardSet = sections[1]
        self.cardNumber = sections[2].replace('[EN]', '')

    def asDict(self):
        cardSetDict = self.__dict__
        return cardSetDict
