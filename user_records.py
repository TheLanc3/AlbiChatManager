class UserRecords:
    def __init__(self, basketball: int, football: int, dart: int, dice: int, balling: int):
        self.basketball = basketball
        self.football = football
        self.dart = dart
        self.dice = dice
        self.balling = balling
    def toJSON(self):
        return self.__dict__