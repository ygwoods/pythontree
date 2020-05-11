import pickle as p
import requests
import os.path,time
from tree import *
querylist=[]
def load():
    fr =requests.get(root.url+'/data')
    if fr.status_code==200:
        with open('data','wb+') as f:
            f.write(fr.content)
        return 'Data loaded, restart to check.'
    else:
        with open('data','rb') as f:
            return p.load(f)
def dump():
    if isinstance(root,Tree):
        with open('data','wb+') as f:
            p.dump(root,f)
        with open('root.txt','w+',encoding='utf-8') as f:
            root.layer=0
            stk=[root] 
            while stk:
                tr = stk.pop()
                if not hasattr(tr,'layer'):
                    tr.layer=tr.parent.layer+1
                if hasattr(tr,'text'):
                    f.write(str(tr.layer)+'\t'+tr.node+'\t'+'tr.text'+'\n')
                else:
                    f.write(str(tr.layer)+'\t'+tr.node+'\t'+''+'\n')
                if tr.child:
                    stk.extend(tr.child)

def dumptoweb():
    if isinstance(root,Tree):
        with open('data','wb+') as f:
            p.dump(root,f)
        with open('data','rb') as f:
            files={'a':f}
            t=requests.post(root.url+'upload.php',files=files)
            if 200 == t.status_code:return 'ok'
            else:return 'network error:'+t


def initdata():
    if os.path.isfile('data'):
        with open('data','rb') as f:
            return p.load(f)
    else:
        tr=Tree('root')
        tr.pos=('600','550','300','0')
        tr.url='https://yuke.wang/note'
        return tr
activetree=root=initdata()    
def add(node):
    if node is Tree:
        node.parent=activetree
        activetree.child.append(node)
    else:
        tr=Tree(node,parent=activetree)
        activetree.child.append(tr)
        return tr
def update(node,comment=''):
    activetree.node=node
def delete():
    global activetree
    temp = activetree.parent
    temp.child.remove(activetree)
    activetree=temp
def query(qstr):
    global querylist
    querylist=[]
    qstrs=qstr.split('>')
    relists=[]
    travels([activetree],relists,qstrs[0])
    if len(qstrs)>1:
        for tr in relists:
            for tc in tr.child:
                if qstrs[1] in tc.node:querylist.append(tc)

    elif len(qstrs)==1:
        querylist=relists
    else:pass
    for i in range(0,len(querylist)):print(i,querylist[i].node)
def travel(tlist):
    while tlist:
        tree=tlist.pop()
        print(tree.node)
        if tree.child:
            for i in tree.child:travel([i])
def travels(tlists,relist,qstr):
    while tlists:
        tr=tlists.pop()
        if qstr in tr.node:relist.append(tr)
        if tr.child:
            for i in tr.child:travels([i],relist,qstr)
def layer():
    a=0
    pin =activetree
    print(pin.parent)
    while  pin.parent:
        a=a+1
        pin = pin.parent
    return a