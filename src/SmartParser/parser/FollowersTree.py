
class Node:
    def __init__(self, rule, parent):
        self.rule = rule
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def write_result(self, result):
        self.result = result
    

    
class FollowersTree:

    def __init__(self, root): 
        self.root = root

    
