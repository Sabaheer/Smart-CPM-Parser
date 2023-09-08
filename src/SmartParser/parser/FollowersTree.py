
class Node:
    def __init__(self, rule, text_index, parent):
        self.rule = rule
        self.parent = parent
        self.children = []
        self.text_index = text_index

    def add_child(self, child):
        self.children.append(child)

    

    
class FollowersTree:

    def __init__(self, root): 
        self.root = root

    
