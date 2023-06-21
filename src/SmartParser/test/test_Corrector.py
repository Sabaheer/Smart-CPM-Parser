import string
import unittest
from unittest import TestCase
from parameterized import parameterized

import parser.Rule
from parser import helper, GrammarDesc
from parser.Corrector import Corrector
from parser.GrammarDesc import CARRIER, ULD
from parser.Rule import Rule


from test_helper import createRule, testEquals


class TestCorrector(unittest.TestCase):
    def parse(self, text):
        rule = Rule(CARRIER)
        return rule.match_line(text)

    def test_alphabet_mistake_simple(self):
        original = "EY980/21.A6DDD.HAN"

        test_count = 0
        correct = 0
        for i in range(len(original)):
            for char1 in set(string.ascii_uppercase):

                new = original
                if new[i] in set(string.ascii_uppercase):
                    new = new[:i] + char1 + new[i + 1:]

                rule = Rule(ULD)
                result = self.parse(new)

                print(new, result)
                expected = {"AirlineDesignator": "EY", "FlightNumber": "980",
                            "DepartureDate": "21",
                            "RegistrationNumber": "A6DDD",
                            "DepartureStation": "HAN"}

                if testEquals(expected, result):
                    correct +=1

                test_count += 1

        print(f"{test_count}, {correct}")

    def test_benchmark_unknown_simple(self):
        original = "EY980/21.A6DDD.HAN"

        test_count = 0
        correct = 0
        for i in range(len(original)):
            for j in range(i, len(original)):
                for char1 in ["@"]:

                    new = original
                    new = new[:i] + char1 + new[i:]
                    new = new[:j] + char1 + new[j:]

                    rule = Rule(GrammarDesc.ULD)
                    result = self.parse(new)

                    corrector = Corrector()
                    fixedValue = corrector.fix(new,GrammarDesc.CARRIER)
                    if fixedValue:
                        correct += 1
                    print(new, fixedValue)
                    expected = {"AirlineDesignator": "EY", "FlightNumber": "980",
                                "DepartureDate": "21",
                                "RegistrationNumber": "A6DDD",
                                "DepartureStation": "HAN"}
                    if testEquals(expected, result):
                        correct +=1

                    test_count += 1

        print(f"{test_count}, {correct}")

    def test_something(self):
        original = "EY980/21.A6DDD.HAN"
        rule = Rule(GrammarDesc.ULD)
        result = self.parse(original)

        #print(new, result)
        expected = {"AirlineDesignator": "EY", "FlightNumber": "980",
                    "DepartureDate": "21",
                    "RegistrationNumber": "A6DDD",
                    "DepartureStation": "HAN"}
        print(f"{expected}, {result}")
        if testEquals(expected, result):
            print("OK")
        else:
            print("KO")


    def test_identifyUnknown(self):
        corrector = Corrector()
        unknown = corrector.identifyUnknownPos("EY980?21?A6DDD?HAN", set.union(set(string.ascii_uppercase), set(string.digits)))
        self.assertEqual([5, 8, 14], unknown)

    @parameterized.expand([
        ["EY980?21?A6DDD?HAN", None],
        ["E Y980/21.A6DDD.HAN", "EY980/21.A6DDD.HAN"],
        ["EY980/21.A   6DDD.HAN", "EY980/21.A6DDD.HAN"],
        ["EY015/27.A6BMB.AUH", "EY015/27.A6BMB.AUH"],
        ["E Y 0 1 5 /27 .A6BMB.A U H", "EY015/27.A6BMB.AUH"],
    ])
    def test_fixCarrier(self, carrier_line, expected):
        corrector = Corrector()
        fixedValue = corrector.fix(carrier_line, GrammarDesc.CARRIER)
        self.assertEqual(expected, fixedValue)

    @parameterized.expand([
        ["-41P/PMC75891EY/MAN/1655/C.HEA", "-41P/PMC75891EY/MAN/1655/C.HEA"],
        ["-   41P /PMC75891EY/MAN/1655/C.HEA", "-41P/PMC75891EY/MAN/1655/C.HEA"],
        ["- AL/PMC77612EY/AUH/1915/C.ELI.VUN", "-AL/PMC77612EY/AUH/1915/C.ELI.VUN"]

    ])
    def test_fixULD(self, uld_line, expected):
        corrector = Corrector()
        fixedValue = corrector.fix(uld_line, GrammarDesc.ULD)
        self.assertEqual(expected, fixedValue)

    def test_fixULD(self):
        corrector = Corrector()
        fixedValue = corrector.fix("- AL/PMC77612EY/AUH/1915/C.ELI.VUN", GrammarDesc.ULD)

        self.assertEqual("-AL/PMC77612EY/AUH/1915/C.ELI.VUN", fixedValue)


    def test_fixULD_missing_start(self):
        corrector = Corrector()
        fixedValue = corrector.fix("AL/PMC77612EY/AUH/1915/C.ELI.VUN", GrammarDesc.ULD)

        self.assertEqual("-AL/PMC77612EY/AUH/1915/C.ELI.VUN", fixedValue)


if __name__ == '__main__':
    unittest.main()
