import os

# from DummyValidator import DummyValidator
from ValidatorAirlineDesignator import ValidatorAirlineDesignator
from ValidatorAirport import ValidatorAirport
from ValidatorCategory import ValidatorCategory
from parser import helper
from parser.MatchField import MatchField
from parser.ValidatorList import ValidatorList


class GrammarDesc:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

CPM = GrammarDesc("CPM",
           [MatchField(MatchField.MATCH_FIELD_MANDATORY, "CPM", "Header", terminator=True)])

# m is alphanumeric
# f is numeric 
# () optional , a is letter
# m{1,12} it can appear one time to twelve times. 

CARRIER = GrammarDesc("CARRIER",
            [MatchField(MatchField.MATCH_FIELD_MANDATORY, "mm(a)", "AirlineDesignator", validator=ValidatorAirlineDesignator()), #validator=ValidatorList(helper.load_file_list(os.path.dirname(__file__)+'/data/airline_codes.txt')))
               MatchField(MatchField.MATCH_FIELD_MANDATORY, "fff(f)(a)", "FlightNumber"),
               MatchField(MatchField.MATCH_FIELD_OPTIONAL, "ff", "DepartureDate", precede_separator="/" ),
               MatchField(MatchField.MATCH_FIELD_MANDATORY, "mm(m)(m)(m)(m)(m)(m)(m)(m)", "RegistrationNumber", precede_separator=".", terminator=True),
               MatchField(MatchField.MATCH_FIELD_OPTIONAL, "aaa", "DepartureStation", validator=ValidatorAirport(), precede_separator=".", terminator=True),
               MatchField(MatchField.MATCH_FIELD_OPTIONAL, "m{1,12}", "ULD_configuration", precede_separator=".", terminator=True)
           ])

ULD = GrammarDesc("ULD",
       [MatchField(MatchField.MATCH_FIELD_MANDATORY, "m(m)(m)", "ULDBayDesignation", precede_separator="-", new_res=True, link_to=["LoadCategory"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "amm((fffff)mm(a))", "ULDTypeCode", precede_separator="/"),
            MatchField(MatchField.MATCH_FIELD_MANDATORY, "aam",  "UnloadingStation", validator=ValidatorAirport(), precede_separator="/"),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "f(f)(f)(f)(f)", "Weight",  precede_separator="/"),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "a(a)(f)", "LoadCategory", validator=ValidatorCategory(), precede_separator="/", link_to=["Weight", "LoadCategory"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "f", "VolumeCode"),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "aaa/mm", "ContourCode",  validator=ValidatorAirport(), precede_separator="."),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "aaa(/f(f)(f))", "IMP",  validator=ValidatorAirport(), precede_separator=".", link_to=["IMP"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "VRf", "AVI", precede_separator=".")
       ])
