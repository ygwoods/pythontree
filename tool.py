import pickle as p
import requests
import re,time
from tree import *
url1='http://192.168.0.100/upload.php'
url2='http://192.168.0.100/data'
querylist=[]

def load():
    fr =requests.get(url2)
    if fr.status_code==200:
        print('netwerk is ok')
        return p.loads(fr.content)
    else:
        with open('data','rb') as f:
            print('local data')
            return p.load(f)
def dump():
    if isinstance(root,Tree):
        with open('data','wb+') as f:
            p.dump(root,f)
        with open('data','rb') as f:
            files={'a':f}
            return requests.post(url1,files=files)
activetree=root=load()

def add(node):
    if node is Tree:
        node.parent=activetree
        activetree.child.append(node)
        print(node.parent)
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
def router(str):
    global activetree,root
    #if len(str)<=1:print('help message')
    if len(str)<=2:#pick a tree
        try:
            i=int(str)
            if i<=len(querylist):
                activetree=querylist[i]
                a=layer()
                print("L%d"%a,activetree.node)
            else:print('out of range')
        except ValueError:
            if str[0]=='t':
                travel([activetree])
            elif str[0]=='d':
                delete()
            elif str[0]=='s':
                dump()
            elif str[0]=='n':
                root=Tree('root')
                dump()
            elif str[0]=='x':
                a=layer()
                print("L%d"%a,activetree.node)
            elif str[0]=='<':activetree=activetree.parent
            else:pass
    else:
        if str[0]=='a':
            add(str[2:])
        elif str[0]=='q':
            query(str[2:])
        elif str[0]=='u':
            update(str[2:])
        else:
            print('help message s- save q- query a-add  t- travel d- delete u- update n- newtree')  
if __name__ == "__main__":
    a=''
    while a !='!q':
        a=input()
        router(a)