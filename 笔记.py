import tool as t 
from tkinter import Tk,Entry,Label,Menu,Text,Toplevel
from tkinter.ttk import *
from tkinter.font import Font
from tkinter.messagebox import *
import icon
import os
import webbrowser
class Tool(Tk):
    def __init__(self):
        super().__init__()
        self.dic={}
        self.dictv={}
        self.diclist={}
        self.title('树图笔记')
        self.geometry("%sx%s+%s+%s"%t.root.pos)
        self.iconbitmap("tmp.ico")
        os.remove('tmp.ico')
        self.textboard=None
        self.listview=None 
        self.top = None

        #define view windget

        self.treeview=Treeview(self,height=27,show="tree");self.treeview.heading('#0',text='树目')
        self.searchview=Entry(self)
        ft=Font(family='等线',size=12)
        self.textboard=Text(self,bg='snow',fg='maroon',font=ft)
        self.tbar=Scrollbar(self.treeview,orient='horizontal')
        self.treeview.config(xscrollcommand=self.tbar.set)
        self.tbar.config(command=self.treeview.xview)

        #layout view
        
        self.tbar.pack(side='bottom',fill='x',expand=1,anchor="s")
        self.treeview.pack(side='left',fill='y',ipadx=50,anchor="w")
        self.searchview.pack(side='top',fill='both',anchor="w")
        self.textboard.pack(side='top',fill='both',expand=1,anchor="w")
        #init data
        #self.top.deiconify()
        for i in t.root.child:
            tv=self.treeview.insert('','end',text=i.node)
            self.dic[i]=tv
            self.dictv[tv]=i
            self.travel(i.child)
        self.viewbind()
    def viewbind(self):           #bind event handle function
        self.bind('<Configure>',self.tbset)
        self.bind('<space>',lambda e: self.searchview.focus_force())
        self.bind('<Escape>',lambda e: self.home(e))
        self.treeview.bind('<<TreeviewSelect>>',self.showtree)
        self.textboard.bind('<Control-KeyPress-s>',self.addtreetext)
        for i in ['<Return>','<Delete>','<Up>']:self.searchview.bind(i,self.action)
        
    def saveto(self):
        t.dumptoweb()

    def tbset(self,e):
        if e.widget==self and int(e.width)>300:
            t.root.pos=(e.width,str(int(e.height)+25),e.x,e.y)
        if self.top:
            self.top.deiconify()
            #x=t.root.pos
            #self.top.geometry("%sx%s+%s+%s"%(str(int(self.winfo_screenwidth())-int(x[0])-int(x[2])),x[1],str(int(x[0])+int(x[2])+10),x[3]))

    def addtreetext(self,e):
        text=self.textboard.get('1.0','end')
        t.activetree.text=text
    def treeishow(self,e):
        i=int(e.keysym)
        if i<=len(t.querylist) and len(t.querylist):self.treeview.see(self.dic[t.querylist[i]])
        if(self.top):
            self.top.deiconify()
    def treeshow(self,e):
        tr=self.diclist[self.listview.selection()[0]]
        self.treeview.see(self.dic[tr])
    def showtree(self,e):
        if  not self.treeview.selection() :return
        t.activetree=self.dictv[self.treeview.selection()[0]]
        #for item in self.listview.get_children():self.listview.delete(item)
        self.textboard.delete('1.0','end')
        if hasattr(t.activetree, 'text'):
            self.textboard.insert('end',t.activetree.text)
    def delete(self):
        if t.activetree==self.dictv[self.treeview.selection()[0]]:
            tv=self.dic[t.activetree]
        del(self.dic[t.activetree])
        del(self.dictv[tv])
        t.activetree.parent.child.remove(t.activetree)
        t.activetree=t.root
        self.treeview.delete(tv)
    def travel(self,treelist):
        for tree in treelist:
            tv=self.treeview.insert(self.dic[tree.parent],'end',text=tree.node)
            self.dic[tree]=tv
            self.dictv[tv]=tree
            self.travel(tree.child)
    def home(self,e):
        t.root.url='https://yuke.wang/note/'
        self.treeview.selection_set(())
        t.activetree=t.root
    def action(self,e):#searchview events
        entr_str=self.searchview.get()
        self.searchview.delete('0','end')
        if e.keysym=='Return':
            t.query(entr_str)
            lv=''
            self.top=Toplevel()
            self.top.geometry("300x400+50+50")
            #self.top.overrideredirect(1)
            self.top.attributes('-alpha', 0.95)
            #self.top.withdraw()
            self.listview=Treeview(self.top,height=26,show='headings',style='L.Treeview',columns=('a','b','c','d'))
            for (ia,iw,it) in [('a',30,'no.'),('b',200,'tree'),('c',200,'tag'),('d',150,'link')]:
                self.listview.column(ia,width=iw)
                self.listview.heading(ia,text=it)
            self.sbar=Scrollbar(self.listview)
            self.listview.config(yscrollcommand=self.sbar.set)
            self.sbar.config(command=self.listview.yview)
            self.listview.bind('<<TreeviewSelect>>',self.treeshow)
            for i in ['0','1','2','3','4','5','6','7','8','9']:self.listview.bind("<KeyPress-%s>"%i,self.treeishow)
            self.listview.pack(side='top',fill='both',ipadx=2,expand=1,anchor="w")
            self.sbar.pack(side='right',fill='y',anchor="e")
            #for item in self.listview.get_children():self.listview.delete(item)
            for i in range(0,len(t.querylist)):
                tg=lk=''
                if hasattr(t.querylist[i], 'tag'):tg=t.querylist[i].tag
                if hasattr(t.querylist[i],'link'):lk=t.querylist[i].link
                lv=self.listview.insert('','end',values=(i,t.querylist[i].node,tg,lk))
                print('no.',i,t.querylist[i].node,tg,lk)
                self.diclist[lv]=t.querylist[i]
                self.listview.focus_force()

        elif e.keysym=='Up':
            if len(entr_str)>20:return
            tr=t.add(entr_str)
            if not tr.parent.parent:
                self.dic[tr]=self.treeview.insert('','end',text=tr.node)
            else:
                self.dic[tr]=self.treeview.insert(self.dic[tr.parent],'end',text=tr.node)
            self.dictv[self.dic[tr]]=tr
        elif e.keysym=='Delete':
            self.delete()
        else:
            pass
if __name__ == "__main__":Tool().mainloop()