
class Node:
    def __init__(self, rule, text_index, parent):
        self.rule = rule
        self.parent = parent
        self.text_index = text_index
        self.result = None

    
