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

            # print(self.current_text)
            # print("", follower.field_name)
            # print(f"{separator}{follower.expression}")
            #print(m)

            if not match and follower.type == MatchField.MATCH_FIELD_MANDATORY: # result is empty dictionary {}
                traversed = False
                c_node = node.parent
                while c_node:
                    if c_node.rule.field_name == follower.field_name:
                        traversed = True
                        break
                    c_node = c_node.parent
                if not traversed:
                    break

            if match: # if found a match rule counter increased.
                if node.rule.new_res: # if new res is true then
                    if len(self.result) > 0:
                        self.final_result += [self.result]
                        self.result = {}

                node.progress += len(match.group(0)) # current text reassigned | It eliminates the matched text. | group(0) gives entire matched text.
                value = match.group()[len(node.rule.precede_separator):] # group() is similar to group(0) | it skips the " " separator. 
                
                node.part = match.group()
                node.result = value       

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
            node = sequence.pop(0) # we are poping the first node in sequence
            if node.progress >= len(text): # if current node is greater than length of text
                final_node = node # replace the final node with current node
                break # and break the loop
            next_nodes = []
            
            for follower in node.rule.gr_followers: # create child nodes for each grammar follower
                next_nodes.append(Node(follower, node, node.progress))
            csm = self.consume(next_nodes)
            sequence = csm + sequence

        if final_node == None:
            return None
                
        c_node = final_node
        while c_node:
            bm = {"part": c_node.part, "field":c_node.rule.field_name, "value":c_node.result}
            if c_node.rule.validator:
                #print("Validator!!!")
                validate_result = c_node.rule.validator.validate(c_node.result)
                #print(value, validate_result)
                if "/" not in c_node.result:
                    if validate_result["CODE"] == Validator.CODE_SUGGEST:
                        #res_backmatch["possible"]= ["EY", "EI", "ET"]
                        bm["possible"] = validate_result["VALUE"]
                        bm["wrong"] = True
            self.backmatch = [bm] + self.backmatch 
            if c_node.rule.repeated:
                if c_node.rule.field_name not in self.result:
                    self.result[c_node.rule.field_name] = []
                self.result[c_node.rule.field_name].insert(0, c_node.result)
            else:
                self.result[c_node.rule.field_name] = c_node.result # result = {'Airline: EY'}

            c_node = c_node.parent

        if len(self.final_result) > 0:
            self.result =  self.final_result + [self.result]

        if isinstance(self.result, list): # for each key-value pair in result
            tmp = []
            for itm in self.result:
                tmp += [self.fixRule.fixData(itm, self.metadata)]
            return tmp

        return self.fixRule.fixData(self.result, self.metadata)

