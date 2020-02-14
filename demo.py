import tool as t 
from tkinter import Tk,Entry,Label,Menu,Text,Toplevel
from tkinter.ttk import *
from tkinter.font import Font
from icon import icon
import base64
import os
import webbrowser
class Tool(Tk):
    def __init__(self):
        super().__init__()
        self.dic={}
        self.dictv={}
        self.diclist={}
        self.style=Style()
        self.style.configure("F.TButton", relief='flat',font=('tahoma','16','normal'),foreground="black", background="white")
        self.style.configure("L.Treeview", borderwidth=1,relief='flat',foreground="black", background="white")
        self.title('树图笔记')
        try:
            self.pos=t.root.pos
        except BaseException:
            self.pos=('400','550','300','0')
            t.root.pos=self.pos
        self.geometry("%sx%s+%s+%s"%self.pos)
        with open("tmp.ico","wb+") as f:
            f.write(base64.b64decode(icon))
        self.iconbitmap("tmp.ico")
        os.remove("tmp.ico")
        self.textboard=None
        self.top=None
        self.tbflag=False

        
        #define view windget

        self.treeview=Treeview(self,height=27,show="tree");self.treeview.heading('#0',text='树目')
        self.treeview.column('#0',width=250)
        self.searchview=Entry(self)
        self.listview=Treeview(self,height=26,show='headings',style='L.Treeview',columns=('a','b','c','d'))
        for (ia,iw,it) in [('a',30,'no.'),('b',200,'tree'),('c',200,'tag'),('d',150,'link')]:
            self.listview.column(ia,width=iw)
            self.listview.heading(ia,text=it)
        self.tbar=Scrollbar(self.treeview,orient='horizontal')
        self.sbar=Scrollbar(self.listview)
        self.listview.config(yscrollcommand=self.sbar.set)
        self.treeview.config(xscrollcommand=self.tbar.set)
        self.tbar.config(command=self.treeview.xview)
        self.sbar.config(command=self.listview.yview)

        #add menu
        menubar = Menu(self)
        self.fMenu=Menu(menubar,tearoff=0)
        self.sMenu=Menu(menubar,tearoff=0)
        self.eMenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label = "File ",menu = self.fMenu)
        menubar.add_cascade(label =  "Edit ",menu = self.eMenu)
        menubar.add_cascade(label = "Set  ",menu = self.sMenu)
        menubar.add_command(label = "About",command = self.about)
        #self.fMenu.add_command(label='open', command=None)
        self.fMenu.add_command(label='Save', command=t.dump)
        #self.fMenu.add_command(label='download', command=None)
        #self.fMenu.add_command(label='upload', command=None)
        self.eMenu.add_command(label='Copy  Tree', command=None)
        self.eMenu.add_command(label='Paste Tree', command=None)
        self.eMenu.add_command(label='Del   Tree', command=self.delete)
        self.sMenu.add_command(label='On/off textboard', command=self.showtextboard)
        self.sMenu.add_command(label='Check for Updates', command=lambda:self.openweb("http://www.yuke.wang"))
        self.sMenu.add_command(label='Current version：0.1', command=None)
        self.config(menu=menubar)


        #layout view
        self.tbar.pack(side='bottom',fill='x',expand=1,anchor="s")
        self.treeview.pack(side='left',fill='y',ipadx=50,anchor="w")
        #Label(self,width=0).pack(side='left',fill='y',ipadx=0,ipady=0,padx=0,pady=0,anchor="w")
        self.searchview.pack(side='top',fill='both',anchor="w")
        self.listview.pack(side='top',fill='both',ipadx=2,expand=1,anchor="w")
        self.sbar.pack(side='right',fill='y',anchor="e")
        self.viewbind()
        #init data
        for i in t.root.child:
            tv=self.treeview.insert('','end',text=i.node)
            self.dic[i]=tv
            self.dictv[tv]=i
            self.travel(i.child)
        for i in range(0,len(t.querylist)):
            self.listview.insert('','end',text=t.querylist[i].node)
    def viewbind(self):           #bind event handle function
        self.bind('<Configure>',self.tbset)
        self.bind('<space>',lambda e: self.searchview.focus_force())
        self.bind('<Escape>',lambda e: self.home(e))
        self.bind('<quoteleft>',lambda e: self.home(e))
        self.treeview.bind('<<TreeviewSelect>>',self.showtree)
        self.listview.bind('<<TreeviewSelect>>',self.treeshow)
        for i in ['0','1','2','3','4','5','6','7','8','9']:self.bind("<KeyPress-%s>"%i,self.treeishow)
        #self.treeview.bind('<2>',self.copy_tree)
        for i in ['<Return>','<Delete>','<Up>']:self.searchview.bind(i,self.action)
    def openweb(self,urls):
        webbrowser.open(urls)
    def showtextboard(self):
        if not self.top:
            self.top=Toplevel()
            x=self.pos
            self.top.geometry("%sx%s+%s+%s"%('600',x[1],str(int(x[0])+int(x[2])+10),x[3]))
            self.top.overrideredirect(1)
            self.top.attributes('-alpha', 0.95)
            ft=Font(family='等线',size=12)
            self.textboard=Text(self.top,bg='snow',fg='maroon',font=ft)
            self.textboard.bind('<Control-KeyPress-s>',self.addtreetext)
            self.textboard.pack(fill='both',expand=1)
            self.tbflag=True
            return
        if self.tbflag :
            self.top.withdraw()
            self.tbflag=False
        else:
            self.top.deiconify()
            self.tbflag=True
    def tbset(self,e):
        if e.widget==self and int(e.width)>300:
            self.pos=t.root.pos=(e.width,str(int(e.height)+25),e.x,e.y)
            print(e)
        if self.tbflag:
            x=self.pos
            print(x)
            self.top.geometry("%sx%s+%s+%s"%(str(int(self.winfo_screenwidth())-int(x[0])-int(x[2])),x[1],str(int(x[0])+int(x[2])+10),x[3]))
    def about(self):
        pass
    def addtreetext(self,e):
        text=self.textboard.get('1.0','end')
        t.activetree.text=text
    def treeishow(self,e):
        i=int(e.keysym)
        if i<=len(t.querylist) and len(t.querylist):self.treeview.see(self.dic[t.querylist[i]])
    def treeshow(self,e):
        tr=self.diclist[self.listview.selection()[0]]
        self.treeview.see(self.dic[tr])
    def showtree(self,e):
        if  not self.treeview.selection() :return
        t.activetree=self.dictv[self.treeview.selection()[0]]
        for item in self.listview.get_children():self.listview.delete(item)
        if self.tbflag:
            self.textboard.delete('1.0','end')
            if hasattr(t.activetree, 'text'):
                self.textboard.insert('end',t.activetree.text)
        for i in t.activetree.child:
            self.listview.insert('','end',i.node)
        #listview show child
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
        self.treeview.selection_set(())
        t.activetree=t.root
    def action(self,e):#searchview events
        entr_str=self.searchview.get()
        self.searchview.delete('0','end')
        if e.keysym=='Return':
            t.query(entr_str)
            lv=''
            for i in range(0,len(t.querylist)):
                for item in self.listview.get_children():self.listview.delete(item)
                tg=lk=''
                if hasattr(t.querylist[i], 'tag'):tg=t.querylist[i].tag
                if hasattr(t.querylist[i],'link'):lk=t.querylist[i].link
                lv=self.listview.insert('','end',values=(i,t.querylist[i].node,tg,lk))
                print('no.',i,t.querylist[i].node,tg,lk)
                self.diclist[lv]=t.querylist[i]
                self.listview.focus_force()

        elif e.keysym=='Up':
            if len(entr_str)>20:return
            #tr=t.Tree()
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