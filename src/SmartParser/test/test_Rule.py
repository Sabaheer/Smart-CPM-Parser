from unittest import TestCase
from parameterized import parameterized

from parser import helper, GrammarDesc
from parser.Rule import Rule, MatchField
from test_helper import createRule


class TestRule(TestCase):

    @parameterized.expand([
        ["1234", [("M", "mm", "f1", "", []), ("M", "mm", "f2", "", ["f1"])], {"f1": "12", "f2": "34"}],
        ["1234", [("M", "mmmm", "f1", "", [])], {"f1": "1234"}],


        ["1234", [("M", "mmm(m)", "f1", "", [])], {"f1": "1234"}],
        ["12345", [("M", "mmm(m)", "f1", "", []), ("M", "m", "f2", "", ["f1"])], {"f1": "1234", "f2":"5"}],

        ["12ab", [("M", "ff", "f1", "", []), ("M", "aa", "f2", "", ["f1"])], {"f1": "12", "f2":"ab"}],
    ])
    def test_simple(self, text, fields, expected):
        rule = createRule(fields)
        res = rule.match_line(text)
        self.assertTrue(expected, res)


    @parameterized.expand([
        ["EY980/21.A6DDD.HAN", GrammarDesc.CARRIER,
         {"AirlineDesignator": "EY",
          "FlightNumber":"980",
          "DepartureDate": "21",
          "RegistrationNumber":"A6DDD",
          "DepartureStation": "HAN"}],
        ["EY9868/12.A6DDF.RUH", GrammarDesc.CARRIER,
         {"AirlineDesignator": "EY",
          "FlightNumber": "9868",
          "DepartureDate": "12",
          "RegistrationNumber": "A6DDF",
          "DepartureStation": "RUH"}],
        ["EY917/08.A6DDB.AUH", GrammarDesc.CARRIER,
         {"AirlineDesignator": "EY",
          "FlightNumber": "917",
          "DepartureDate": "08",
          "RegistrationNumber": "A6DDB",
          "DepartureStation": "AUH"}],
    ])
    def test_carrier(self, text, fields, expected):
        rule = Rule(fields)
        res = rule.match_line(text)
        self.assertTrue(expected, res)


    @parameterized.expand([
        ["-41P/PMC75891EY/MAN/1655/C.HEA", GrammarDesc.ULD,
         {"ULDBayDesignation": "41P",
          "ULDTypeCode": "PMC75891EY",
          "UnloadingStation": "MAN",
          'Weight': '1655',
          'LoadCategory': ["C"],
          'IMP': ['HEA']}],
        ["-AL/PMC77612EY/AUH/1915/C.ELI.VUN", GrammarDesc.ULD,
         {"ULDBayDesignation": "AL",
          "ULDTypeCode":"PMC77612EY",
          "UnloadingStation": "AUH",
          'Weight': '1915',
          'LoadCategory':["C"],
          'IMP': ['ELI', "VUN"]}],
        ["-41L/AKE26910EY/AUH/65/X", GrammarDesc.ULD,
         {'ULDBayDesignation': '41L',
          'ULDTypeCode': 'AKE26910EY',
          'UnloadingStation': 'AUH',
          'Weight': '65',
          'LoadCategory': ['X']}],
        ["-44R/AKE23963EY/AUH/778/M", GrammarDesc.ULD,
         {'ULDBayDesignation': '44R',
          'ULDTypeCode': 'AKE23963EY',
          'UnloadingStation': 'AUH',
          'Weight': '778',
          'LoadCategory': ['M']}]
    ])
    def test_ULD(self, text, fields, expected):
        rule = Rule(fields)
        res = rule.match_line(text)
        self.assertEqual(expected, res)

    '''
    def test_SI(self):
        self.fail()
    '''

    @parameterized.expand([
        ["1234", [("M", "aaaa", "f1", "", [])], None],
    ])
    def test_unmatched(self, text, fields, expected):
        rule = createRule(fields)
        res = rule.match_line(text)
        self.assertIsNone(res)

    def test_file(self):
        cpm = helper.load_file("data/CPM1.txt")

        for line in cpm[2:]:
            rule = Rule(GrammarDesc.ULD)
            res = rule.match_line(line.strip())
            print(line.strip())
            print("\t", res)

    def test_repeating(self):
        fields = [MatchField("M", "aa", "AirlineDesignator",  repeated=True, precede_separator="/", depends_on=["AirlineDesignator"]),
                  MatchField("M", "aaaa", "hehe", precede_separator="-", depends_on=["AirlineDesignator"])]
        rule = Rule(GrammarDesc.GrammarDesc("dummy", fields))
        result = rule.match_line("./AA/BB/CC-ABCD")
        print(result)

    def test_repeating1(self):
        rule = Rule(GrammarDesc.ULD)
        toParse="-PL/PMC75956EY/AUH/2564/C/MD-PR/PMC76540EY/AUH/2338/C/MD"
        print(toParse)
        result = rule.match_line(toParse)
        print(result)

    def test_ULD(self):
        rule = Rule(GrammarDesc.ULD)
        toParse="-AL/PMC77612EY/AUH/1915/C.ELI.VUN"
        print(toParse)
        result = rule.match_line(toParse)
        self.assertIsNotNone(result)

    def test_ULD1(self):
        rule = Rule(GrammarDesc.ULD)
        toParse="-41P/PMC75891EY/MAN/1655/C.HEA"
        print(toParse)
        result = rule.match_line(toParse)
        print("backmatch", rule.backmatch)
        self.assertIsNotNone(result)

    def test_ULD2(self):
        rule = Rule(GrammarDesc.ULD)
        toParse="-44L/600/E.EIC"
        print(toParse)
        result = rule.match_line(toParse)
        print(result)
        self.assertEqual({'ULDBayDesignation': '44L', 'Weight': '600', 'LoadCategory': ['E'], 'IMP': ['EIC']}, result)

    def test_ULD3(self):
        rule = Rule(GrammarDesc.ULD, )
        toParse="-51/AMS/26/M"
        print(toParse)
        result = rule.match_line(toParse)

        print(result)
        self.assertEqual({'ULDBayDesignation': '51', 'ULDTypeCode': 'AMS', 'Weight': '26', 'LoadCategory': ['M']}, result)

    def test_ULD4(self):
        rule = Rule(GrammarDesc.ULD)
        toParse = "-12L/AKE/MAN/551/BJ1-12R/N"
        print(toParse)
        result = rule.match_line(toParse)
        print(result)
        self.assertEqual({'ULDBayDesignation': '51', 'ULDTypeCode': 'AMS', 'Weight': '26', 'LoadCategory': ['M']},
                         result)

    def test_ULD5(self):
        rule = Rule(GrammarDesc.ULD)
        toParse="-KL/PMC72929EY/AUH/2395/C.ELI.ELM.VUN/Q5"
        print(toParse)
        result = rule.match_line(toParse)

        print(result)
        self.assertEqual({'ContourCode': 'VUN/Q5',
 'IMP': ['ELI', 'ELM'],
 'LoadCategory': ['C'],
 'ULDBayDesignation': 'KL',
 'ULDTypeCode': 'PMC72929EY',
 'UnloadingStation': 'AUH',
 'Weight': '2395'}, result)

    def test_ULD_repeating(self):
        rule = Rule(GrammarDesc.ULD)
        toParse = "-12R/AKE24439EY/AUH/274/BJ/150/BY1"
        print(toParse)
        result = rule.match_line(toParse)
        print(result)
        self.assertIsNotNone(result)

    @parameterized.expand([
        ["-GL/PMC77740EY/AUH/2266/C/MD-GR/PMC75259EY/AUH/2402/C/MD",
         [{'ULDBayDesignation': 'GL',
           'ULDTypeCode': 'PMC77740EY',
           'UnloadingStation': 'AUH',
           'Weight': '2266',
           'LoadCategory': ['C', 'MD']},
          {'ULDBayDesignation': 'GR',
           'ULDTypeCode': 'PMC75259EY',
           'UnloadingStation': 'AUH',
           'Weight': '2402',
           'LoadCategory': ['C', 'MD']}],
         ],
    ])
    def test_long_ULD(self, text, expected):
        rule = Rule(GrammarDesc.ULD)

        result = rule.match_line(text)
        print(result)

        self.assertEqual(expected,result)

    def test_repeatingNotMatched(self):
        rule = Rule(GrammarDesc.CARRIER)
        toParse = "EY980-21.A6DDD-HAN"
        result = rule.match_line(toParse)
        print(result)