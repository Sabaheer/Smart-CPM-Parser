import json
import string
from unittest import TestCase
from parameterized import parameterized

import PreParser
import helper
from parser.Parser import Parser

class TestParser(TestCase):
    def getjson(self, filename):
        f = open(filename)
        data = json.load(f)
        f.close()
        return data

    def savejson(self, filename, data:string):
        f = open(filename, "w")
        f.write(data)
        f.close()

    @parameterized.expand(
        [["data/CPM_newlines_0.txt", "data/CPM_newlines.txt.json"],
         ["data/CPM_newlines_1.txt", "data/CPM_newlines.txt.json"],
         ["data/CPM_newlines_2.txt", "data/CPM_newlines.txt.json"],
         ["data/CPM_newlines_3.txt", "data/CPM_newlines.txt.json"]
         ])

    def test_newline(self, source, expected_values_file):
        result = Parser().parse_file(source)
        #self.savejson("data/CPM_newlines_0.txt.json", json.dumps(result, indent=4))
        expected = self.getjson(expected_values_file)
        self.assertEqual(expected, result)

    @parameterized.expand(
        [["data/CPM_typo_carrier_0.txt", "data/CPM_typo_carrier.txt.json"],
         ["data/CPM_typo_carrier_1.txt", "data/CPM_typo_carrier.txt.json"],
         ["data/CPM_typo_carrier_2.txt", "data/CPM_typo_carrier.txt.json"]
         ])
    def test_typo_carrier(self, source, expected_values_file):
        result = Parser().parse_file(source)
        # self.savejson(expected_values_file, json.dumps(result, indent=4))

        expected = self.getjson(expected_values_file)
        self.assertEqual(expected, result)

    @parameterized.expand(
        [["data/CPM_typo_ULD_0.txt", "data/CPM_typo_ULD.txt.json"],
         ["data/CPM_typo_ULD_1.txt", "data/CPM_typo_ULD.txt.json"],
         ["data/CPM_typo_ULD_2.txt", "data/CPM_typo_ULD.txt.json"],
         ["data/CPM_typo_ULD_3.txt", "data/CPM_typo_ULD.txt.json"],
         ["data/CPM_typo_ULD_4.txt", "data/CPM_typo_ULD.txt.json"],
         ["data/CPM_typo_ULD_5.txt", "data/CPM_typo_ULD.txt.json"],
         ["data/CPM_typo_ULD_6.txt", "data/CPM_typo_ULD.txt.json"],
         #["data/CPM_typo_ULD_A_0.txt", "data/CPM_typo_ULD_A.txt.json"],
         #["data/CPM_typo_ULD_A_1.txt", "data/CPM_typo_ULD_A.txt.json"],
         #["data/CPM_typo_ULD_A_2.txt", "data/CPM_typo_ULD_A.txt.json"],
         ])
    def test_typo_ULD(self, source, expected_values_file):

        result = Parser().parse_file(source)
        #self.savejson(expected_values_file, json.dumps(result, indent=4))

        expected = self.getjson(expected_values_file)
        self.assertEqual(expected, result)

    @parameterized.expand(
        [["data/CPM_wrongnewlines_0.txt", "data/CPM_wrongnewlines.txt.json"],
         ["data/CPM_wrongnewlines_1.txt", "data/CPM_wrongnewlines.txt.json"],
         ["data/CPM_wrongnewlines_2.txt", "data/CPM_wrongnewlines.txt.json"],
         ["data/CPM_wrongnewlines_3.txt", "data/CPM_wrongnewlines.txt.json"],
         ["data/CPM_wrongnewlines_4.txt", "data/CPM_wrongnewlines.txt.json"],
         ["data/CPM_wrongnewlines_A_0.txt", "data/CPM_wrongnewlines_A.txt.json"],
         ["data/CPM_wrongnewlines_A_1.txt", "data/CPM_wrongnewlines_A.txt.json"]
         ])
    def test_wrongnewlines(self, source, expected_values_file):
        result = Parser().parse_file(source)
        #self.savejson(expected_values_file, json.dumps(result, indent=4))

        expected = self.getjson(expected_values_file)
        self.assertEqual(expected, result)


    def test_wrongnewlines_0(self):
        result = Parser().parse_file("data/CPM_wrongnewlines_0.txt")
        expected = self.getjson("data/CPM_wrongnewlines.txt.json")
        self.assertEqual(expected, result)

    @parameterized.expand(
        [["data/CPM_footer_0.txt", "data/CPM_footer.txt.json"],

         ])
    def test_footer(self, source, expected_values_file):

        result = Parser().parse_file(source)
        #self.savejson(expected_values_file, json.dumps(result, indent=4))

        expected = self.getjson(expected_values_file)
        self.assertEqual(expected, result)

    @parameterized.expand(
        ["data/nonsence0.txt",
         "data/nonsence-long0.txt"

         ])
    def test_nonsence(self, source):
        result = Parser().parse_file(source)
        print(result)
        # self.savejson(expected_values_file, json.dumps(result, indent=4))

        #expected = self.getjson(expected_values_file)
        #self.assertEqual(expected, result)

    @parameterized.expand(
        [["data/CPM1.txt", "data/CPM1.txt.json"],
         ["data/CPM2.txt", "data/CPM2.txt.json"],
         ["data/CPM3.txt", "data/CPM3.txt.json"],
         ["data/CPM4.txt", "data/CPM4.txt.json"],
         ["data/CPM5.txt", "data/CPM5.txt.json"],
         ["data/CPM6.txt", "data/CPM6.txt.json"],
         ["data/CPM7.txt", "data/CPM7.txt.json"],
         ["data/CPM8.txt", "data/CPM8.txt.json"],
         ])
    def test_full(self, source, expected_values_file):
        result = Parser().parse_file(source)
        self.savejson(expected_values_file, json.dumps(result, indent=4))

        expected = self.getjson(expected_values_file)
        self.assertEqual(expected, result)
        self.fail("Not checked yet")

    def test_preparse(self):
        lines = helper.load_file_simple("data/CPM_preparse_invalid_carrier.txt").split("\n")
        preparser = PreParser.PreParser()
        preparser.preparse_engine(lines)
        self.assertEqual([[1, 2]], preparser.unparsable_regions)
        self.assertEqual([{'AirlineDesignator': 'EY'}, None, None], preparser.preparsed_lines)



    def test_preparse_invalid2(self):
        lines = helper.load_file_simple("data/CPM_preparse_invalid_2.txt").split("\n")
        preparser = PreParser.PreParser()
        preparser.preparse_engine(lines)
        print(preparser.unparsable_regions)
        self.assertEqual([[1, 2], [5]], preparser.unparsable_regions)
        self.assertEqual([{'AirlineDesignator': 'EY'}, None, None, {'ULDBayDesignation': 'AR', 'ULDTypeCode': 'PMC72671EY', 'UnloadingStation': 'AUH', 'Weight': '1840', 'LoadCategory': ['C'], 'IMP': ['ELI', 'VUN']}, {'ULDBayDesignation': 'AR', 'ULDTypeCode': 'PMC72671EY', 'UnloadingStation': 'AUH'}, None], preparser.preparsed_lines)

    def test_preparse_valid(self):
        lines = helper.load_file_simple("data/CPM_preparse_valid.txt").split("\n")
        preparser = PreParser.PreParser()
        preparser.preparse_engine(lines)
        print(preparser.unparsable_regions)
        self.assertEqual([], preparser.unparsable_regions)
        self.assertEqual([{'AirlineDesignator': 'EY', 'FlightNumber': '972', 'DepartureDate': '11', 'RegistrationNumber': 'A6DDD', 'DepartureStation': 'HAN'}, {'ULDBayDesignation': 'AR', 'ULDTypeCode': 'PMC72671EY', 'UnloadingStation': 'AUH', 'Weight': '1840', 'LoadCategory': ['C'], 'IMP': ['ELI', 'VUN']}, {'ULDBayDesignation': 'AR', 'ULDTypeCode': 'PMC72671EY', 'UnloadingStation': 'AUH', 'Weight': '1840', 'LoadCategory': ['C'], 'IMP': ['ELI', 'VUN']}]
                        , preparser.preparsed_lines)


    def test_backmatch(self):
        parser = Parser()
        result = parser.parse_file("data/CPM_typo_ULD_0.txt")
        print("----")
        print(result)
        print(parser.backmatches)
        #result.backmatches =

        #self.savejson(expected_values_file, json.dumps(result, indent=4))

        #expected = self.getjson(expected_values_file)
        #self.assertEqual(expected, result)
        self.fail("Not checked yet")