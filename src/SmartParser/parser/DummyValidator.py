from parser.Validator import Validator
from Levenshtein import distance as levenshtein_distance


class DummyValidator(Validator):
    def __init__(self):
        pass

    def validate(self, toBeValidated):

        return {"CODE": self.CODE_SUGGEST, "SUGGESTIONS": ['ABC', 'DDD', 'YYY']}
        # return {"CODE": self.CODE_REJECT}