#-------------------------------------------------------------------------------
# Name:        Scrap Project
# Purpose:     To make a GUI scrapper
#
# Author:      X____X
#
# Created:     25-06-2018
# Copyright:   (c) X____X 2018
# Licence:     Open Software License 2.0
#-------------------------------------------------------------------------------

from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
#----------------------------Scraping Class-------------------------------------
class datascraping():
    def __init__(self):
        pass

    def scrapit(self,url,tag,attr="",content=False,**kwargs):
        req = requests.get(url)
        soup = BeautifulSoup(req.text,'html5lib')
        out =[]
        #print(kwargs)
        #print(tag)
        if len(tag) !=0 and attr == "" and content is False:
            for lines in soup.find_all(tag):
                out.append(lines)
        elif len(tag) is not 0 and len(attr) is not 0:
            for lines in soup.find_all(tag):
                txt = lines.get(attr)
                out.append(txt)
        elif len(tag) is not 0 and content is True:
            for lines in soup.find_all(tag):
                out.append(lines.text)
        else:
            out.append('Extracting raw html data...')
            for lines in soup:
                out.append(lines)
        return out

    def scrapitreg(self,url,tag,*args):
        req = requests.get(url)
        soup = BeautifulSoup(req.text,'html5lib')
        out =[]
        return out


#test site https://www.practicepython.org
class scrapprojgui(datascraping):
    def __init__(self,master):
        v=[]
        v.append(IntVar())
        self.visible=[]
        self.optbox = []
        self.master = master
        master.title("GUI Scraport")
        #---------------------------Main Input Data-----------------------------
        self.frame1 = LabelFrame(master,width=640,height=480,text="Input Data",highlightcolor="Black")
        self.frame1.grid(row=0,column=0,padx=10,pady=5,sticky=W)
        #---------------------------Main Input Data-----------------------------
        self.url_label = ttk.Label(self.frame1,text="URL:",anchor=E)
        self.url_label.grid(row=1,column=0,padx=3)

        self.url_textbox = ttk.Entry(self.frame1,textvariable = "",width=50)
        self.url_textbox.grid(row=1,column=1,padx=5,pady=5)
        #-----------------------------Option Box--------------------------------
        self.optbox.append(ttk.Checkbutton(self.frame1,text = "Tagwise search"))
        self.optbox[0].configure(command=self.tagwise,variable=v[0],onvalue=1,offvalue=0)
        self.optbox[0].grid(row=2,column=1,sticky=W)
        self.visible.append(v[0])

        v.append(IntVar())
        self.optbox.append(ttk.Checkbutton(self.frame1,text="Exclude Tags on Output"))
        self.optbox[1].configure(command=self.conshow,variable=v[1],onvalue=1,offvalue=0)
        self.optbox[1].grid(row=3,column=1,sticky=W)
        self.visible.append(v[1])


        #---------------------------Optional Text-------------------------------
        self.tag_inp = ttk.Entry(self.frame1,textvariable = "",width=5)
        self.attr_inp = ttk.Entry(self.frame1,textvariable="",width=6)
        self.attrlb = Label(self.frame1,text = "Attribute:",width=7)
        #-----------------------------------------------------------------------

        self.extrc_but = ttk.Button(master,text="Scrap it!",command=self.retscrp)
        self.extrc_but.place_configure(in_=master,x=500,y=30)
        self.clr_but = ttk.Button(master,text="Clear",command=self.clear,state=DISABLED)
        self.clr_but.place_configure(in_=master,x=500,y=70)
        #grid(row=1,column=0,padx=2)
        #--------------------------Output Frame---------------------------------
        self.outfr = LabelFrame(master,width=720,height=480,text="Output")
        self.outfr.grid(row=2,column=0,padx=5,pady=5)
        #-----------------------------------------------------------------------
        self.outp = Text(self.outfr,width=100,height=20,insertborderwidth=63,state=DISABLED)
        self.scrlly=Scrollbar(self.outfr,command=self.outp.yview)
        self.scrlly.pack(side='right',fill='y')
        self.outp.configure(yscrollcommand=self.scrlly.set,wrap='word')
        self.outp.pack(side="left", fill="both", expand=True,padx=5,pady=5)
        self.outp.see('end')
        self.content =False



    def retscrp(self):
        self.geturl = str(self.url_textbox.get())
        self.gettag = str(self.tag_inp.get())
        self.attrinp = str(self.attr_inp.get())
        self.outp.configure(state=NORMAL)
        try:
            output = self.scrapit(self.geturl,self.gettag,self.attrinp,self.content)
            for lines in output:
                ln=str(lines)+'\n'
                self.outp.insert('end',ln)
            self.outp.configure(state=DISABLED)
            self.clr_but.state(['!disabled'])
        except:
            print("Url not found or http(s):// is missing")

    def clear(self):
        self.outp.configure(state=NORMAL)
        self.outp.delete('1.0',END)
        self.outp.configure(state=DISABLED)
        self.clr_but.state(['disabled'])

    def conshow(self):
        if(self.visible[1].get()):
            self.content = True
        else:
            self.content = False

    def tagwise(self):
        if(self.visible[0].get()):
            self.tag_inp.place_configure(in_=self.frame1,x=150,y=32)
            self.attrlb.place_configure(in_=self.frame1,x=195,y=32)
            self.attr_inp.place_configure(in_=self.frame1,x=260,y=32)
        else:
            self.attr_inp.delete(0,END)
            self.tag_inp.delete(0,END)
            self.tag_inp.place_forget()
            self.attr_inp.place_forget()
            self.attrlb.place_forget()


def main():
    root = Tk()
    gui = scrapprojgui(root)
    root.mainloop()

if __name__ == '__main__':
    main()
