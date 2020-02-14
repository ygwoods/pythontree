from tkinter import Tk,Label,Entry,Menu,Frame
from tkinter.ttk import Label,Entry,Combobox,Treeview,Scrollbar
from tkinter.messagebox import *
from icon import icon
import os,re,time,pickle#,pyperclip
import base64
import os.path
class Tree(object):
    def __init__(self, node,parent=None):
        self.node = node
        self.parent=parent
        self.child=[]
active=roots=None
dictree={}
dictv={}
listview=None
def update():
    global roots,active
    roots.child=[]
    if not  isinstance(roots,Tree):
        roots=Tree('root',None)
        roots.pos=('400','550','300','0')
    dirroot='datas'#'\\\\Xcmgcqgl\\装配物料清单'
    for f in os.listdir(dirroot):
        if f[:-4:-1]=="txt":
            file=open(dirroot+"\\"+f)
            fl=file.readlines()
            file.close()
            a=fl[0].split('\t')
            a[0]='0'
            a[4]="a"#f.split('.')[0]
            pin=trees=Tree(tuple(a),None)
            for line in fl[1:]:
                a=tuple(line.split('\t'))
                if a[0][-1]>pin.node[0][-1]:
                    pin.child=[Tree(a,pin)]
                    pin=pin.child[0]
                elif a[0][-1]==pin.node[0][-1] :
                    pin.parent.child.insert(0,Tree(a,pin.parent))
                    pin=pin.parent.child[0]
                else:
                    while a[0][-1]<pin.node[0][-1]:pin=pin.parent
                    pin.parent.child.insert(0,Tree(a,pin.parent))
                    pin=pin.parent.child[0]
            roots.child.append(trees)
    active=roots
def updateandsave():
    update()
    with open('data.dat','wb+') as f:
        pickle.dump(roots,f)
    showinfo(message='数据已更新')
if os.path.isfile('data.dat'):
    with open('data.dat','rb') as f:
        active=roots = pickle.load(f)
else:
    update()
def listview_sort_fill(listviewview, col, reverse):#Treeview、列名、排列方式
    l = [(listviewview.set(k, col), k) for k in listviewview.get_children('')]
    l.sort(reverse=reverse)#排序方式
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):#根据排序后索引移动
        listviewview.move(k, '', index)
    listviewview.heading(col, command=lambda: listview_sort_fill(listviewview, col, not reverse))
def copylist():
	 if listview.selection():
	 	text=''
	 	for i in listview.selection():
	 		te=''
	 		for td in listview.item(i)['values']:te+=str(td)+'\t'
	 		text+=te[:len(te)-1]+'\n'
	 	#pyperclip.copy(text[:len(text)-1])
def uplook():
    sel=listview.selection()
    if len(sel)==1:
        te=listview.item(sel)['values']
        for item in listview.get_children():listview.delete(item)
        #ltree=listtree.copy()
        ltree=[active]
        while ltree!=[]:
            wt=ltree.pop()
            if str(wt.node[3]) == str(te[0]):
                w=wt.parent
                listview.insert('',0,values=(w.node[3],w.node[4],w.node[5],w.node[6],w.node[7])) 
            ltree.extend(wt.child)
            
def showtree(event):
    global active
    if  not treeview.selection() :return
    active=dictv[treeview.selection()[0]]
    for item in listview.get_children():listview.delete(item)
    for w in active.child:
            listview.insert('',0,values=(w.node[3],w.node[4],w.node[5],w.node[6],w.node[7]))
def sort(event):
    for item in listview.get_children():listview.delete(item)
    relist=[]
    dic={}
    ltree=active.child.copy()
    while ltree!=[]:
        wt=ltree.pop()
        if wt.child==[]:
            word='(.?)+'+eword.get().replace('*','.+')
            if  eno.get()!='':nums= eno.get() if len(eno.get())>=9 or eno.get()[0]=='^' else '(.?)+'+eno.get().replace('*','.+')
            if (eno.get()==''or re.match(nums,wt.node[3])) and (eword.get()==''or re.match(word,wt.node[4])) and (pbox.get()=='' or wt.node[7][-1]==pbox.get()):
                relist.append(wt)
        else:
            ltree.extend(wt.child)
    for i in relist:
        key=i.node[3]+i.node[7]
        if key in dic:
            print(i.node)
            no=float(dic[key][2])+float(i.node[5])
            no='{:g}'.format(no)
            dic[key]=(i.node[3],i.node[4],no,i.node[6],i.node[7])
        else:
            no="{:g}".format(float(i.node[5]))
            dic.setdefault(key,(i.node[3],i.node[4],no,i.node[6],i.node[7]))
    for k in dic:
        listview.insert('','end',values=dic[k])
def travel(treelist):
    for tr in treelist:
        tv=treeview.insert(dictree[tr.parent],'end',text=tr.node[4])
        dictv[tv]=tr
        dictree[tr]=tv
        if tr.child:travel(tr.child)
def topset(e):
    if len(str(e.widget))==1 and int(e.width>400):
        roots.pos=(e.width,str(int(e.height)+25),e.x,e.y)
#main
top = Tk()
top.geometry("%sx%s+%s+%s"%roots.pos)
top.title("装配BOM查询工具")
with open("tmp.ico","wb+") as f:
    f.write(base64.b64decode(icon))
top.iconbitmap("tmp.ico")
os.remove("tmp.ico")
manu=Menu(top,tearoff=0)
manu.add_command(label="复制", command=copylist)
manu.add_command(label="反查", command=uplook)

treeview=Treeview(top,height=21)
listview= Treeview(top,columns=('no','disc','qty','unit','p'),height=24,show="headings")
for (col,val,wid) in [('no',"料号",90),('disc','描述',270),('qty','数量',40),('unit','单位',35),('p','工位',60)]:
    listview.heading(col,text=val,command=lambda _col=col: listview_sort_fill(listview, _col,False))
    listview.column(col,width=wid)
sb=Scrollbar(listview)
sb.config(command=listview.yview)
listview.config(yscrollcommand=sb.set)
sortargs=[]
panel=Frame(top)
pbox = Combobox(panel,width=2,value= ('','1','2','3','4','5','6','7','8','9'))
pbox.current(0)
eword=Entry(panel)#,width=14)
eno=Entry(panel)#,width=9)
lb=Label(top,text='⇧ Version: 0.98   ')

#init data
for tr in roots.child:  
    tv=treeview.insert('','end',text=tr.node[4])
    dictv[tv]=tr
    dictree[tr]=tv
    if tr.child:travel(tr.child)

#treeview.heading('#0',text='在用机型组件列表',command= showlog)
top.bind('<Configure>',topset)
top.bind('<space>',lambda e: eword.focus_force())
treeview.bind("<<TreeviewSelect>>",showtree)
listview.bind("<Button-3>",lambda e:manu.post(e.x_root,e.y_root))
listview.bind("<Button-2>",copylist)
panel.bind('<Return>',sort)
pbox.bind("<<ComboboxSelected>>",sort)
eno.bind('<Return>',sort)
eword.bind('<Return>',sort)
lb.bind('<Button-1>',lambda e:updateandsave())

treeview.pack(side='left',fill='y',anchor='w')
listview.pack(side='top',fill='both',expand=1,anchor='n')
panel.pack(side='top',fill='x')
sb.pack(side='right',fill='y',anchor='e')

Label(panel,text='名称').pack(side='left',anchor='w')
eword.pack(side='left',fill='x',expand=1)
Label(panel,text='料号').pack(side='left')
eno.pack(side='left',fill='x',expand=1,anchor='e')
Label(panel,text='工位').pack(side='left')
pbox.pack(side='left',fill='x',expand=1)
lb.pack(side='right',anchor='e')
top.mainloop()