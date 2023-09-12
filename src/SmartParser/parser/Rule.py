import os
import re

from FixRule import FixRule
from GrammarDesc import GrammarDesc
from parser import helper
from parser.Grammar import Grammar
from parser.MatchField import MatchField
from parser.Validator import Validator
from parser.ValidatorList import ValidatorList
from parser.FollowersTree import Node


class Rule:

    def __init__(self, grammarDesc:GrammarDesc, fixRule:FixRule = FixRule(), metadata = {}):
        self.grammarDesc = grammarDesc
        self.full_text = None
        self.result = {}
        self.final_result = []
        self.backmatch = []
        self.fixRule =fixRule
        self.metadata = metadata

    def consume(self, nodes): #
        valid_nodes = []
        for node in nodes: # followers list only contain 1 node and it is the first match field. 
            follower = node.rule
            separator = follower.precede_separator # precede separator is just a empty string " "
            if separator == ".": # temporarily adds a /. if there is a . 
                separator = "\." # this is acceptable in regex

            search_expression = f"^{separator}{follower.expression}" # " "[a-zA-Z0-9][a-zA-Z0-9](a-zA-Z)
            match = re.search(search_expression, self.full_text[node.progress:]) # match([a-zA-Z0-9][a-zA-Z0-9](a-zA-Z),EY972/11.A6DDD.HAN) = EY
            print("matching...", follower.field_name, ":::", self.full_text[node.progress:])
            # print(self.current_text)
            # print("", follower.field_name)
            # print(f"{separator}{follower.expression}")
            #print(m)

            if not match and follower.type == MatchField.MATCH_FIELD_MANDATORY and follower.field_name not in self.result: # result is empty dictionary {}
                break

            if match: # if found a match rule counter increased.
                print("..",follower.field_name, "GOOD")

                if node.rule.new_res: # if new res is true then
                    if len(self.result) > 0:
                        self.final_result += [self.result]
                        self.result = {}

                node.progress += len(match.group(0)) # current text reassigned | It eliminates the matched text. | group(0) gives entire matched text.

                value = match.group()[len(node.rule.precede_separator):] # group() is similar to group(0) | it skips the " " separator. 

                res_backmatch = {"part": match.group(), "field":node.rule.field_name, "value":value} #{part: ''EY, field: Airline, value: EY}

                if follower.validator:
                    #print("Validator!!!")
                    validate_result = follower.validator.validate(value)
                    #print(value, validate_result)
                    if "/" not in value:
                        if validate_result["CODE"] == Validator.CODE_SUGGEST:
                            #res_backmatch["possible"]= ["EY", "EI", "ET"]
                            res_backmatch["possible"] = validate_result["VALUE"]
                            res_backmatch["wrong"] = True
                
                self.backmatch += [res_backmatch]
                node.result = (follower.field_name, value)       

                # Add partial result to corresponding node, no need to check repeated here
                '''if follower.repeated:
                    if follower.field_name not in self.result:
                        self.result[follower.field_name] = []
                    self.result[follower.field_name] += [value]
                else:
                    if follower.field_name in self.result:
                        self.result[follower.field_name + "_" +str(self.counter)] = value
                    else:
                        self.result[follower.field_name] = value # result = {'Airline: EY'}'''

                valid_nodes.append(node)
        return valid_nodes

                
    def match_line(self, text): # match according to the rules without fixing it. 
        self.full_text = text

        self.result = {}
        # was temporarily eliminated 
        g = Grammar(self.grammarDesc) #takes as input one of the grammars (header, carrier, etc)
        g.buildSyntaxTree()

        sequence = self.consume([Node(self.grammarDesc.rules[0], None, 0)]) # the first node of list has first match field. 
        final_node = None
        while len(sequence) > 0:
            node = sequence.pop(0)
            if node.progress >= len(text):
                final_node = node
                break
            next_nodes = []

            
            for follower in node.rule.gr_followers: # create child nodes for each grammar follower
                next_nodes.append(Node(follower, node, node.progress))
            sequence = self.consume(next_nodes) + sequence

        print("--result", text, "--")
        if final_node == None:
            return None
                
        c_node = final_node
        while c_node:
            print("result:",c_node.result)
            if c_node.rule.repeated:
                if c_node.rule.field_name not in self.result:
                    self.result[c_node.result[0]] = []
                self.result[c_node.result[0]].insert(0, c_node.result[1])
            else:
                self.result[c_node.result[0]] = c_node.result[1] # result = {'Airline: EY'}
            c_node = c_node.parent

        if len(self.final_result) > 0:
            self.result =  self.final_result + [self.result]

        if isinstance(self.result, list): # for each key-value pair in result
            tmp = []
            for itm in self.result:
                tmp += [self.fixRule.fixData(itm, self.metadata)]
            return tmp

        return self.fixRule.fixData(self.result, self.metadata)