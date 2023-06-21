import os
import re

from FixRule import FixRule
from GrammarDesc import GrammarDesc
from parser import helper
from parser.Grammar import Grammar
from parser.MatchField import MatchField
from parser.Validator import Validator
from parser.ValidatorList import ValidatorList


class Rule:

    def __init__(self, grammarDesc:GrammarDesc, fixRule:FixRule = FixRule(), metadata = {}):
        self.grammarDesc = grammarDesc
        self.full_text = None
        self.current_text = None
        self.result = {}
        self.final_result = []
        self.counter = 0
        self.backmatch = []
        self.fixRule =fixRule
        self.metadata = metadata

    def consume(self, followers):
        for follower in followers:

            separator = follower.precede_separator
            if separator == ".":
                separator = "\."

            search_expression = f"^{separator}{follower.expression}"
            match = re.search(search_expression, self.current_text)

            # print(self.current_text)
            # print("", follower.field_name)
            # print(f"{separator}{follower.expression}")
            #print(m)

            if not match and follower.type == MatchField.MATCH_FIELD_MANDATORY and follower.field_name not in self.result:
                return None

            if match:
                self.counter += 1

                if follower.new_res:
                    if len(self.result) > 0:
                        self.final_result += [self.result]
                        self.result = {}

                self.current_text = self.current_text[len(match.group(0)):]

                value = match.group()[len(follower.precede_separator):]

                res_backmatch = {"part": match.group(), "field":follower.field_name, "value":value}
                if follower.validator:
                    print("Validator!!!")
                    validate_result = follower.validator.validate(value)
                    print(value, validate_result)
                    if "/" not in value:
                        if validate_result["CODE"] == Validator.CODE_SUGGEST:
                            #res_backmatch["possible"]= ["EY", "EI", "ET"]
                            res_backmatch["possible"] = validate_result["VALUE"]
                            res_backmatch["wrong"] = True

                self.backmatch += [res_backmatch]


                if follower.repeated:
                    if follower.field_name not in self.result:
                        self.result[follower.field_name] = []
                    self.result[follower.field_name] += [value]
                else:
                    if follower.field_name in self.result:
                        self.result[follower.field_name + "_" +str(self.counter)] = value
                    else:
                        self.result[follower.field_name] = value

                return follower
        return None

    def match_line(self, text):
        self.full_text = text
        self.current_text = text

        self.result = {}

        g = Grammar(self.grammarDesc)
        g.buildSyntaxTree()

        node = self.grammarDesc.rules[0]
        node = self.consume([node])
        while node != None:
            #print("--- ", node.field_name)
            node = self.consume(node.gr_followers)

        if len(self.current_text) > 0:
            #print("NOT PARSED", self.current_text, self.result)
            return None

        if len(self.final_result) > 0:
            self.result =  self.final_result + [self.result]

        if isinstance(self.result, list):
            tmp = []
            for itm in self.result:
                tmp += [self.fixRule.fixData(itm, self.metadata)]
            return tmp

        return self.fixRule.fixData(self.result, self.metadata)