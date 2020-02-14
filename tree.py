class Tree(object):
    def __init__(self,node,parent=None):
        self.node= node
        self.parent=parent
        self.child=[]