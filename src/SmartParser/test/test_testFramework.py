import unittest

import GrammarDesc
import helper
from Parser import Parser
from TestFramework import TestFramework


def parse_callback_carrier(text, demanded_result):
    debug = True

    result = Parser().parse_line(text, GrammarDesc.CARRIER)
    if result is not None and result != demanded_result:
        if debug:
            print("fishy ", text)
            print(result)
            print("----")
            print(demanded_result)

        return TestFramework.STATUS_UNDETECTED

    if result is None:
        return TestFramework.STATUS_DETECTED

    if result == demanded_result:
        return TestFramework.STATUS_CORRECTED

    return False


def parse_callback_file(text, demanded_result):
    debug = True

    result = Parser().parse_text(text)
    if result is not None and result != demanded_result:
        if debug:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! fishy", text)
            print(result)
            print("----")
            print(demanded_result)

        return TestFramework.STATUS_UNDETECTED

    if result is None:
        return TestFramework.STATUS_DETECTED

    if result == demanded_result:
        return TestFramework.STATUS_CORRECTED

    return False

class MyTestCase(unittest.TestCase):

    def test_carrier_wrong_separators(self):
        print("test_carrier_wrong_separators")

        line = "EY972/11.A6DDD.HAN"
        expected_result = Parser().parse_line(line, GrammarDesc.CARRIER)
        for mistakes in range(1, 3):
            TestFramework().test(line, mistakes, ['.', '\\', '/', '-',' '], ["replace", "add"], parse_callback_carrier,
                                 expected_result)


    def test_carrier_spaces(self):
        print("test_carrier_spaces")

        line = "EY972/11.A6DDD.HAN"
        expected_result = Parser().parse_line(line, GrammarDesc.CARRIER)
        for mistakes in range(1, 2):
            TestFramework().test(line, mistakes, [' '], ["add"], parse_callback_carrier,
                                 expected_result)

    def test_carrier_spaces(self):
        print("test_file")

        line = helper.load_file_simple("test_framework/simple_CPM.txt")
        for mistakes in range(1, 2):
            TestFramework().test(line, mistakes, [' '], ["add"], parse_callback_carrier,
                                 Parser().parse_line(line, GrammarDesc.CARRIER))

    def test_newlines(self):
        print("test_file")

        line = helper.load_file_simple("test_framework/simple_CPM.txt")
        for mistakes in range(1, 2):
            TestFramework().test(line, mistakes, ['\n'], ["add"], parse_callback_file,
                                 Parser().parse_text(line))


if __name__ == '__main__':
    unittest.main()