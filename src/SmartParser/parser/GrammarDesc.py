import os

# from DummyValidator import DummyValidator
from ValidatorAirlineDesignator import ValidatorAirlineDesignator
from ValidatorAirport import ValidatorAirport
from ValidatorCategory import ValidatorCategory
from parser import helper
from parser.MatchField import MatchField
from parser.ValidatorList import ValidatorList
from dashboard.GrammarDB import grammar_db

class GrammarDesc:
    def __init__(self, section):
        self.name = section[0]
        self.rules = []
        for row in section:
            field = row['FieldName']

            moc = MatchField.MATCH_FIELD_OPTIONAL
            if row['Necessity'] == 'Mandatory':
                moc = MatchField.MATCH_FIELD_MANDATORY

            precede = row['PrecedeCharacter']
            if precede == 'None':
                precede = ''

            expression = row['Format']

            lt = row['LinkTo']
            links = []
            if lt != 'None':
                links = lt.split(', ')

            self.rules.append(MatchField(moc, expression, field, precede_separator=precede, link_to=links))

        if self.name in ['ULD', 'BLK']:
            self.rules[0].new_res = True

all_rules = grammar_db.get_all_rules()
CPM = None
CARRIER = None
ULD = None
BLK = None
if all_rules[0]:
    CPM = GrammarDesc(all_rules[0])
if all_rules[1]:
    CARRIER = GrammarDesc(all_rules[1])
if all_rules[2]:    
    ULD = GrammarDesc(all_rules[2])
if all_rules[3]:    
    BLK = GrammarDesc(all_rules[3])


'''CPM = GrammarDesc("CPM",
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
       [MatchField(MatchField.MATCH_FIELD_MANDATORY, "m(m)(m)", "ULDBayDesignation", precede_separator="-", new_res=True, link_to=["Weight","LoadCategory"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "amm((fffff)mm(a))", "ULDTypeCode", precede_separator="/"),
            MatchField(MatchField.MATCH_FIELD_MANDATORY, "aam",  "UnloadingStation", validator=ValidatorAirport(), precede_separator="/"),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "f(f)(f)(f)(f)", "Weight",  precede_separator="/"),
            MatchField(MatchField.MATCH_FIELD_MANDATORY, "a(a)(f)", "LoadCategory", validator=ValidatorCategory(), precede_separator="/", link_to=["Weight", "LoadCategory"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "f", "VolumeCode"),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "aaa(/f(f)(f))", "IMP",  validator=ValidatorAirport(), precede_separator=".", link_to=["IMP"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "aaa/mm", "ContourCode",  validator=ValidatorAirport(), precede_separator=".")
       ])

BLK = GrammarDesc("BLK",
       [MatchField(MatchField.MATCH_FIELD_MANDATORY, "f(f)", "Compartment", precede_separator="-", new_res=True, link_to=["LoadCategory"]),
            MatchField(MatchField.MATCH_FIELD_MANDATORY, "aam",  "Destination", validator=ValidatorAirport(), precede_separator="/"),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "f(f)(f)(f)", "Weight",  precede_separator="/"),
            MatchField(MatchField.MATCH_FIELD_MANDATORY, "a(a)(f)", "LoadCategory", validator=ValidatorCategory(), precede_separator="/", link_to=["Weight", "LoadCategory"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "aaa(/f(f)(f))", "IMP",  validator=ValidatorAirport(), precede_separator=".", link_to=["IMP"]),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "PCSn(n)(n)(n)", "NumPieces", validator=ValidatorCategory(),precede_separator="."),
            MatchField(MatchField.MATCH_FIELD_OPTIONAL, "VRf", "AVI", precede_separator=".")
       ])'''
