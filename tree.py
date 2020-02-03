import pickle as p
import requests
url1='http://yuke.wang/upload.php'
url2='http://yuke.wang/data'
class Tree(object):
    def __init__(self,node,parent=None):
        self.node= node
        self.paren=parent
        self.child=[]
def travel(tree):
    if not tree:return
    tree.node
    for t in tree.child:
        travel(t)
def load():
    fr= requests.get(url2)
    if fr.status_code==200:
        return p.loads(fr.content)
def dump(a):
    with open('data','wb+') as f:
        p.dump(a,f)
    files={'a':open('data','rb')}
    return requests.post(url1,files=files)
def add(itree,node):
    if node is Tree:
        node.parent=itree
        itree.child.append(node)
    else:
        itree.child.append(Tree(node,parent=itree))
print('ok')