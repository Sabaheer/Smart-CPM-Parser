import os
import re

from FixRule import FixRule
from GrammarDesc import GrammarDesc
from parser import helper
from parser.Grammar import Grammar
from parser.MatchField import MatchField
from parser.Validator import Validator
from parser.ValidatorList import ValidatorList
from parser.FollowersTree import FollowersTree, Node


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

    def consume(self, node): #
        followers = node.rule.gr_followers
        for follower in followers: # followers list only contain 1 node and it is the first match field. 

            separator = follower.precede_separator # precede separator is just a empty string " "
            if separator == ".": # temporarily adds a /. if there is a . 
                separator = "\."

            search_expression = f"^{separator}{follower.expression}" # " "[a-zA-Z0-9][a-zA-Z0-9](a-zA-Z)
            match = re.search(search_expression, self.current_text) # match([a-zA-Z0-9][a-zA-Z0-9](a-zA-Z),EY972/11.A6DDD.HAN) = EY

            # print(self.current_text)
            # print("", follower.field_name)
            # print(f"{separator}{follower.expression}")
            #print(m)

            if not match and follower.type == MatchField.MATCH_FIELD_MANDATORY and follower.field_name not in self.result: # result is empty dictionary {}
                break

            if match: # if found a match rule counter increased. 
                self.counter += 1

                if follower.new_res: # if new res is true then
                    if len(self.result) > 0:
                        self.final_result += [self.result]
                        self.result = {}

                self.current_text = self.current_text[len(match.group(0)):] # current text reassigned | It eliminates the matched text. | group(0) gives entire matched text.

                value = match.group()[len(follower.precede_separator):] # group() is similar to group(0) | it skips the " " separator. 

                res_backmatch = {"part": match.group(), "field":follower.field_name, "value":value} #{part: ''EY, field: Airline, value: EY}

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
                child = Node(follower, node)
                child.result = (follower.field_name, value)
                node.add_child(child)

                if follower.repeated:
                    if follower.field_name not in self.result:
                        self.result[follower.field_name] = []
                    self.result[follower.field_name] += [value]
                else:
                    if follower.field_name in self.result:
                        self.result[follower.field_name + "_" +str(self.counter)] = value
                    else:
                        self.result[follower.field_name] = value # result = {'Airline: EY'}

                

    def match_line(self, text): # match according to the rules without fixing it. 
        self.full_text = text
        self.current_text = text

        self.result = {}
        # was temporarily eliminated 
        g = Grammar(self.grammarDesc) #takes as input one of the grammars (header, carrier, etc)
        g.buildSyntaxTree()

        sequence = [Node(self.grammarDesc.rules[0], None)]
        final_node = None
        while len(sequence) > 0:
            if len(sequence[0].rule.gr_followers) == 0:
                final_node = sequence #continue here
            self.consume(sequence[0])
            sequence += sequence.pop(0).children

        # Consume function needs to clear partial results. Currently it is always adding results. 
        # Make the 

        

        
        node = self.grammarDesc.rules[0]
        node = self.consume([node]) # the first node of list has first match field. 
        while node != None:
            #print("--- ", node.field_name)
            node = self.consume(node.gr_followers)

        if len(self.current_text) > 0:
            #print("NOT PARSED", self.current_text, self.result)
            return None

        if len(self.final_result) > 0:
            self.result =  self.final_result + [self.result]

        if isinstance(self.result, list): # for each key-value pair in result
            tmp = []
            for itm in self.result:
                tmp += [self.fixRule.fixData(itm, self.metadata)]
            return tmp

        return self.fixRule.fixData(self.result, self.metadata)