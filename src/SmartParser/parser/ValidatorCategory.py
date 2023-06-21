from ValidatorList import ValidatorList
from parser.Validator import Validator
from Levenshtein import distance as levenshtein_distance

class ValidatorCategory(ValidatorList):
    def __init__(self):
        ValidatorList.__init__(self, ["B", "C", "M", "H", "HB", "BF", "BT", "Q", "C", "X", "N"])
