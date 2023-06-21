import unittest

import graphviz

import parser.Rule
from parser import GrammarDesc
from parser.Corrector import Corrector
from parser.Grammar import Grammar
from parser.MatchField import MatchField


class TestGrammar(unittest.TestCase):
    def test_grammar(self):

        grammar = Grammar(GrammarDesc.CARRIER)
        grammar.buildSyntaxTree()

        self.show_grammar("other/carrier", grammar)

        grammar = Grammar(GrammarDesc.ULD)
        grammar.buildSyntaxTree()

        self.show_grammar("other/uld", grammar)
        #self.assertEqual(True, False)  # add assertion here

    def show_grammar(self, filename, grammar):

        dot = graphviz.Digraph(filename, comment='The Round Table')
        for field in grammar.grammarDesc.rules:
            color = "black"
            if field.type == MatchField.MATCH_FIELD_OPTIONAL:
                color = "gray"
            terminator = ""
            if field.terminator:
                terminator = "\nt"
            dot.node(field.field_name, f"{field.field_name}\n{field.simple_expression}{terminator}", color=color)

        for field in grammar.grammarDesc.rules:
            for follower in field.gr_followers:
                dot.edge(field.field_name, follower.field_name, constraint='false', label=f"{follower.precede_separator}")

        dot.render(filename)


if __name__ == '__main__':
    unittest.main()
