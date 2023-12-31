import os
import re

from FixRule import FixRule
from GrammarDesc import GrammarDesc
from parser import helper
from parser.Grammar import Grammar
from parser.MatchField import MatchField
from parser.Validator import Validator
from parser.ValidatorList import ValidatorList
from parser.Semantics import Semantics, LineSemantics

class Node:
    def __init__(self, rule, parent, progress):
        self.rule = rule
        self.parent = parent
        self.progress = progress

class Segment:
    def __init__(self, part, field, value):
        self.part = part
        self.field = field
        self.value = value

        self.allwrong = False
        self.possible = []

    def suggest(self, sugs):
        self.possible += sugs

class Rule:

    def __init__(self, grammarDesc:GrammarDesc, sem:Semantics, fixRule:FixRule = FixRule(), metadata = {}):
        self.grammarDesc = grammarDesc
        self.sem = sem
        self.line_sem = LineSemantics()
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
            node = sequence.pop(0) # we are popping the first node in sequence
            if node.progress >= len(text) and node.rule.terminator: # if current node is greater than length of text
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
            seg = Segment(c_node.part, c_node.rule.field_name, c_node.result)

            #Turning off validators temporarily
            if c_node.rule.validator:
                #print("Validator!!!")
                validate_result = c_node.rule.validator.validate(c_node.result)
                #print(value, validate_result)
                if "/" not in c_node.result:
                    if validate_result["CODE"] == Validator.CODE_SUGGEST:
                        #res_backmatch["possible"]= ["EY", "EI", "ET"]
                        seg.suggest(validate_result["VALUE"])
 
            self.backmatch = [seg] + self.backmatch 
            if c_node.rule.repeated:
                if c_node.rule.field_name not in self.result:
                    self.result[c_node.rule.field_name] = []
                self.result[c_node.rule.field_name].insert(0, c_node.result)
            else:
                self.result[c_node.rule.field_name] = c_node.result # result = {'Airline: EY'}


            # Collect semantic information
            match c_node.rule.field_name:
                case 'Weight':
                    self.sem.total_weight += int(c_node.result)
                case 'UnloadingStation' | 'Destination':
                    if c_node.result not in self.sem.stations:
                        self.sem.stations[c_node.result] = 1
                    else:
                        self.sem.stations[c_node.result] += 1
                case 'ULDBayDesignation' | 'Compartment':
                    if c_node.result not in self.sem.bays:
                        self.sem.bays.append(c_node.result)
                    else:
                        seg.suggest(['This bay/compartment designation is repeated'])
                case 'ULDTypeCode':
                    if c_node.result not in self.sem.uld_types:
                        self.sem.uld_types.append(c_node.result)
                    else:
                        seg.suggest(['This ULD type code is repeated'])
                case 'LoadCategory':
                    if c_node.result in self.line_sem.load_categories:
                        seg.suggest(['This load category is repeated'])
                    else:
                        self.line_sem.load_categories.append(c_node.result)
                    if c_node.result == 'N':
                        self.line_sem.load_empty = True
                    if not self.line_sem.load_empty and (not c_node.parent
                                    or c_node.parent.rule.field_name in ['ULDBayDesignation','Compartment']):
                        seg.suggest(['Missing essential information for non-empty load '+seg.value])

                case 'IMP':
                    if c_node.result in self.line_sem.imps:
                        seg.suggest(['This IMP is repeated'])
                    else:
                        self.line_sem.imps = [c_node.result] + self.line_sem.imps


            c_node = c_node.parent

        # Check line semantics
        if self.line_sem.load_empty:
            for seg in self.backmatch:
                fn = seg.field
                if fn not in ['ULDBayDesignation','Compartment','LoadCategory']:
                    seg.suggest([fn+' should not exist for empty load'])
                elif fn == 'LoadCategory' and seg.value != 'N':
                    seg.suggest(['No other load category should coexist with Empty'])

        if len(self.line_sem.imps) >= 2:
            for i in range(len(self.line_sem.imps)-1):
                iflws = []
                if self.line_sem.imps[i] in self.sem.imp_seq:
                    iflws = self.sem.imp_seq[self.line_sem.imps[i]]
                else:
                    self.sem.imp_seq[self.line_sem.imps[i]] = iflws
                for j in range(i+1, len(self.line_sem.imps)):
                    if self.line_sem.imps[j] in self.sem.imp_seq:
                        jflws = self.sem.imp_seq[self.line_sem.imps[j]]
                        addjtoi = True
                        for jn in range(len(jflws)):
                            if jflws[jn] == self.line_sem.imps[i]:
                                jflws.pop(jn)
                                addjtoi = False
                                self.sem.imp_debates.append((self.line_sem.imps[i],self.line_sem.imps[j]))
                                break
                        if addjtoi:
                            if not self.sem.imp_flw(self.line_sem.imps[j], self.line_sem.imps[i]):
                                iflws.append(self.line_sem.imps[j])
                            else:
                                for seg in self.backmatch:
                                    if (seg.field == 'IMP' and seg.value in
                                            [self.line_sem.imps[i], self.line_sem.imps[j]]):
                                        seg.suggest(['IMP ordering ('+self.line_sem.imps[i]+
                                                ' and '+self.line_sem.imps[j]+') is inconsistent with other lines'])
                    else:
                        iflws.append(self.line_sem.imps[j])


        if len(self.final_result) > 0:
            self.result = self.final_result + [self.result]

        if isinstance(self.result, list): # for each key-value pair in result
            tmp = []
            for itm in self.result:
                tmp += [self.fixRule.fixData(itm, self.metadata)]
            return tmp

        return self.fixRule.fixData(self.result, self.metadata)

