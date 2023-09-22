from ValidatorList import ValidatorList
from parser.Validator import Validator
from Levenshtein import distance as levenshtein_distance
from dashboard.AirportCodes import AirportCodes

class ValidatorAirport(ValidatorList):

    def __init__(self):
        airports = AirportCodes().get_all_codes()
        ValidatorList.__init__(self, airports)

VAL_AIRPORT = ValidatorAirport()
