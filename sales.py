from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image
from employee import employeeClass
from product import productClass
import pymysql as mydb
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

class SalesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Keeper(TorcAI)-Sales")
        self.root.config(bg="white")

        self.bill_list=[]
        self.var_invoice=StringVar()
        title=Label(self.root,text="View User Bill",font=("times new roman",30,"bold"),bg="grey",fg="black",relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root,text="Invoice No.",font=("times new roman",15,"bold"),bg="white").place(x=50,y=100)
        
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15,"bold"),bg="lightyellow").place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Search",command=self.search,cursor="hand2",font=("goudy old style",15),bg="green",fg="white").place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,cursor="hand2",font=("goudy old style",15),bg="lightgray",fg="black").place(x=490,y=100,width=120,height=28)
    
        sales_frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=140,width=300,height=330)
        
        scrolly=Scrollbar(sales_frame,orient=VERTICAL)
        self.sales_List=Listbox(sales_frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_List.yview)
        self.sales_List.pack(fill=BOTH,expand=1)
        self.sales_List.bind("<ButtonRelease-1>",self.get_data)

        #bill 
        bill_frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=370,y=140,width=350,height=330)

        lbl_title2=Label(bill_frame,text="User Bill Area",font=("times new roman",15,"bold"),bg="grey",fg="black",relief=RIDGE).pack(side=TOP,fill=X)


        scrolly2=Scrollbar(bill_frame,orient=VERTICAL)
        self.bill_area=Text(bill_frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        self.graph_frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        self.graph_frame.place(x=740,y=140,width=350,height=330)

        self.graphsales()
        self.show()

    
    def show(self):
        self.bill_list[:]
        self.sales_List.delete(0,END)
        for i in os.listdir('/home/tanvi/Documents/intern/projects/assignment4-inventory/bill'):
            if i.split('.')[-1]=='txt':
                self.sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.sales_List.curselection()
        file_name=self.sales_List.get(index_)
        self.bill_area.delete('1.0',END)
        fp=open(f'/home/tanvi/Documents/intern/projects/assignment4-inventory/bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()


    def search(self):
        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
            else:
                if self.var_invoice.get() in self.bill_list:
                    fp=open(f'/home/tanvi/Documents/intern/projects/assignment4-inventory/bill/{self.var_invoice.get()}.txt','r')
                    self.bill_area.delete('1.0',END)
                    for i in fp:
                        self.bill_area.insert(END,i)
                    fp.close()
                else:
                    messagebox.showerror("Error","Invalid invoice no",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete("1.0",END)

    def graphsales(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "products" )
        cursor=conn.cursor()
        self.graph=[]
        cursor.execute('Select * from products')
        row=cursor.fetchall()

        for product in row: 
            print(product[2], product[5])
            totalsales=int(product[2])*int(product[5])
            self.graph.append((product[1], totalsales))

    
        df=pd.DataFrame(self.graph)

        fig = Figure(figsize = (3, 3),
                    dpi = 100)
        plot1 = fig.add_subplot(111)
    
        # plotting the graph
        plot1.plot(df[0], df[1])
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                master = self.graph_frame)  
        canvas.draw()
    
        # placing the canvas on the T
        # kinter window
        canvas.get_tk_widget().pack()




if __name__==  "__main__":      
    root=Tk()   
    obj=SalesClass(root)
    root.mainloop() 