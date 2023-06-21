import unittest
from parameterized import parameterized

from parser import helper, GrammarDesc
from parser.Rule import Rule, MatchField
from test_helper import createRule, testEquals

class TestValidator(unittest.TestCase):
    @parameterized.expand([
        ["name1", "EY980/21.A6DDD.HAN", GrammarDesc.CARRIER,
         {"AirlineDesignator": "EY", "FlightNumber": "980",
          "DepartureDate": "21",
          "RegistrationNumber": "A6DDD",
          "DepartureStation": "HAN"}],
        ["name2", "EY9868/12.A6DDF.RUH", GrammarDesc.CARRIER,
         {"AirlineDesignator": "EY", "FlightNumber": "9868",
          "DepartureDate": "12",
          "RegistrationNumber": "A6DDF",
          "DepartureStation": "RUH"}],
        ["name3", "EY917/08.A6DDB.AUH", GrammarDesc.CARRIER,
         {"AirlineDesignator": "EY", "FlightNumber": "917",
          "DepartureDate": "08",
          "RegistrationNumber": "A6DDB",
          "DepartureStation": "AUH"}],
    ])
    def test_carrier(self, name, text, fields, expected):
        rule = Rule(fields)
        res = rule.match_line(text)
        self.assertTrue(testEquals(expected, res), f"{name}: {res} != {expected}")


if __name__ == '__main__':
    unittest.main()
