
class MatchField:
    MATCH_FIELD_MANDATORY = "M"
    MATCH_FIELD_CONDITIONAL = "C"
    MATCH_FIELD_OPTIONAL = "O"

    def __init__(self, type,
                 simple_expression,
                 field_name,
                 precede_separator ="",
                 repeated = False,
                 validator = None,
                 depends_on = [],
                 terminator=False,
                 new_res = False):
        self.type = type
        self.simple_expression = simple_expression
        self.field_name = field_name
        self.expression = self.to_reg_expression(self.simple_expression)
        self.precede_separator = precede_separator
        self.repeated = repeated
        self.validator = validator
        self.depends_on = depends_on
        self.terminator = terminator
        self.new_res = new_res

        self.gr_start = False # it is set to true when it starts building syntax tree. 
        self.gr_followers = []


    def to_reg_expression(self, format): # format is mm(a) airline designator format
        res = ""
        change = {"m": "[a-zA-Z0-9]", "a":"[a-zA-Z]", "f":"[0-9]", ")":")?"} # m=alphanumeric, a=alphabet and f=alphanumeric ? is optional
        for s in format:
            if s in change:
                res += change[s]
            else:
                res += s

        return res
