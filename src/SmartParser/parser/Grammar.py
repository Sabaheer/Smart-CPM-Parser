from GrammarDesc import GrammarDesc
from parser.MatchField import MatchField


class Grammar:
    def __init__(self, grammarDesc:GrammarDesc):
        self.grammarDesc = grammarDesc

    def get_following(self, field:MatchField):
        folowing = []
        for item in self.grammarDesc.rules:

            if field.field_name in item.depends_on:
                folowing += [item]
        return folowing

    def buildSyntaxTree(self):

        self.grammarDesc.rules[0].gr_start = True
        for item in self.grammarDesc.rules:
            item.gr_followers = self.get_following(item)
