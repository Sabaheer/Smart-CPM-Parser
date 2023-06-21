import json
import string

from Parser import Parser


class TestFramework:
    STATUS_CORRECTED = 1
    STATUS_DETECTED = 2
    STATUS_UNDETECTED = 3

    def __init__(self):
        pass

    def test(self, content, changes, characters, operations, parse_callback, demanded_result):

        self.parse_callback = parse_callback
        self.corrected = 0
        self.detected = 0
        self.undetected = 0
        self.total = 0
        self.demanded_result = demanded_result

        self.operations = operations
        self.operations_ADD = "add" in self.operations
        self.operations_REPLACE = "replace" in self.operations


        #content = self.get_file_content(filename)
        self.characters = characters


        self._test(content, 0, changes)
        print(f"corrected = {self.corrected}, detected = {self.detected}, uncorrected={self.undetected},  TOTAL={self.total}")

    def add(self, s:string, pos:int, ch:string):
        return s[:pos] + ch + s[pos:]

    def replace(self, s:string, pos:int, ch:string):
        return s[:pos] + ch + s[pos + 1:]

    def _test(self, text, pos, changes):

        if (changes == 0):
            status = self.parse_callback(text, self.demanded_result)
            if status == TestFramework.STATUS_CORRECTED:
                self.corrected += 1
            elif status == TestFramework.STATUS_DETECTED:
                self.detected += 1
            else:
                self.undetected += 1



            self.total += 1
            return

        if pos >= len(text):
            return

        for character in self.characters:
            if self.operations_REPLACE:
                tmp = self.replace(text, pos, character)
                self._test(tmp, pos + 1, changes-1)

            if self.operations_ADD:
                tmp = self.add(text, pos, character)
                self._test(tmp, pos + 1, changes - 1)

        self._test(text, pos + 1, changes)