from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image
import pymysql as mydb
import time
import sys,subprocess,os
import tempfile


class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Keeper(TorcAI)-BILL AREA")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        #title
        title=Label(self.root,text="Inventory Keeper",font=("times new roman",40,"bold"),bg="lightgray",fg="black",anchor="center").place(x=0,y=0,relwidth=1,height=70)
        #button
        btn_logout=Button(self.root,command=self.logout,text="Logout",font=("times new roman",15,"bold"),bg="black",fg="white",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #clock
        self.lbl_clock=Label(self.root,text="Welcome!! \t\t Date:DD-MM-YY \t\t Time: HH:MM:SS",font=("times new roman",15),bg="white",fg="black")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)


        #product frame
        self.var_search=StringVar()
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        ptitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="lightgray",fg="black").pack(side=TOP,fill=X)


        ProductFrame2=Frame(ProductFrame1,bd=4,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product|By Name",font=("goudy old style",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        
        lbl_name=Label(ProductFrame2,text="Product Name",font=("goudy old style",13,"bold"),bg="white",fg="black").place(x=2,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("goudy old style",15),bg="lightyellow",fg="black").place(x=142,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,command=self.search,cursor="hand2",text="Search",font=("goudy old style",15,"bold"),bg="green",fg="white").place(x=297,y=45,width=90,height=25)
        btn_showall=Button(ProductFrame2,command=self.show,cursor="hand2",text="Show All",font=("goudy old style",15,"bold"),bg="blue",fg="white").place(x=292,y=10,width=96,height=25)


        product_frame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        product_frame3.place(x=2,y=140,width=398,height=385)

        scrolly=Scrollbar(product_frame3,orient=VERTICAL)
        scrollx=Scrollbar(product_frame3,orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(product_frame3,columns=("pid","Name","Price","Quantity","Status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("Name",text="Name")
        self.product_Table.heading("Price",text="Price")
        self.product_Table.heading("Quantity",text="Qty")
        self.product_Table.heading("Status",text="Status")
        self.product_Table["show"]="headings" #to remove extra column
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)

        self.product_Table.column("pid",width=50)
        self.product_Table.column("Name",width=100)
        self.product_Table.column("Price",width=100)
        self.product_Table.column("Quantity",width=50)
        self.product_Table.column("Status",width=100)

        lbl_note=Label(ProductFrame1,anchor='w',text="Note:'Enter 0 Quantity to remove product from the Cart'",font=("goudy old style",10),bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #customer frame
        self.var_name=StringVar()
        self.var_contact=StringVar()
        CustomerFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame1.place(x=420,y=110,width=530,height=70)

        ctitle=Label(CustomerFrame1,text="User Details",font=("goudy old style",13,"bold"),bg="lightgray",fg="black").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame1,text="Name",font=("goudy old style",15),bg="white").place(x=5,y=33)
        txt_name=Entry(CustomerFrame1,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow",fg="black").place(x=80,y=33,width=180)


        lbl_contact=Label(CustomerFrame1,text="Contact",font=("goudy old style",15),bg="white").place(x=270,y=33)
        txt_contct=Entry(CustomerFrame1,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow",fg="black").place(x=380,y=33,width=140)

        #cart frame
        Cal_CartFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_CartFrame.place(x=420,y=190,width=530,height=360)
        #calculator frame
        # self.var_calInput=StringVar()
        # Cal_Frame=Frame(Cal_CartFrame,bd=2,relief=RIDGE,bg="white")
        # Cal_Frame.place(x=5,y=10,width=268,height=340)

        # txt_calInput=Entry(Cal_Frame,textvariable=self.var_calInput,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state="readonly")
        # txt_calInput.grid(row=0,columnspan=4)

        # btn_7=Button(Cal_Frame,text='7',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input(7)).grid(row=1,column=0)
        # btn_8=Button(Cal_Frame,text='8',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input(8)).grid(row=1,column=1)
        # btn_9=Button(Cal_Frame,text='9',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input(9)).grid(row=1,column=2)
        # btn_sum=Button(Cal_Frame,text='+',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input('+')).grid(row=1,column=3)

        # btn_4=Button(Cal_Frame,text='4',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input(4)).grid(row=2,column=0)
        # btn_5=Button(Cal_Frame,text='5',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input(5)).grid(row=2,column=1)
        # btn_6=Button(Cal_Frame,text='6',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input(6)).grid(row=2,column=2)
        # btn_subtract=Button(Cal_Frame,text='-',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input('-')).grid(row=2,column=3)


        # btn_1=Button(Cal_Frame,text='1',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input(1)).grid(row=3,column=0)
        # btn_2=Button(Cal_Frame,text='2',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input(2)).grid(row=3,column=1)
        # btn_3=Button(Cal_Frame,text='3',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input(3)).grid(row=3,column=2)
        # btn_mul=Button(Cal_Frame,text='*',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=15,command=lambda:self.get_input('*')).grid(row=3,column=3)


        # btn_0=Button(Cal_Frame,text='0',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=22,command=lambda:self.get_input(0)).grid(row=4,column=0)
        # btn_c=Button(Cal_Frame,text='c',command=self.clear_cal,cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=22).grid(row=4,column=1)
        # btn_eq=Button(Cal_Frame,text='=',command=self.perform_cal,cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=22).grid(row=4,column=2)
        # btn_div=Button(Cal_Frame,text='/',cursor="hand2",font=('arial',15,'bold'),bd=5,width=3,pady=22,command=lambda:self.get_input('/')).grid(row=4,column=3)

        #cart frame
        cart_frame=Frame(Cal_CartFrame,bd=3,relief=RIDGE)
        cart_frame.place(x=5,y=8,width=520,height=342)

        self.cart_title=Label(cart_frame,text="Cart \t Total Product:[0]",font=("goudy old style",10,"bold"),bg="white",fg="black")
        self.cart_title.pack(side=TOP,fill=X)
        

        scrolly=Scrollbar(cart_frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_frame,orient=HORIZONTAL)

        self.cart_Table=ttk.Treeview(cart_frame,columns=("pid","Name","Price","Quantity"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cart_Table.xview)
        scrolly.config(command=self.cart_Table.yview)
        self.cart_Table.heading("pid",text="PID")
        self.cart_Table.heading("Name",text="Name")
        self.cart_Table.heading("Price",text="Price")
        self.cart_Table.heading("Quantity",text="Qty")
        # self.cart_Table.heading("Status",text="Status")
        self.cart_Table["show"]="headings" #to remove extra column
        self.cart_Table.pack(fill=BOTH,expand=1)
        self.cart_Table.bind('<ButtonRelease-1>',self.get_cartdata)

        self.cart_Table.column("pid",width=40)
        self.cart_Table.column("Name",width=80)
        self.cart_Table.column("Price",width=60)
        self.cart_Table.column("Quantity",width=30)
        # self.cart_Table.column("Status",width=70)

        #add cart widgets
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_qty=StringVar()
        self.var_price=StringVar()
        self.var_stock=StringVar()
        self.var_status=StringVar()
        Add_CartFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartFrame.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(Add_CartFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_pname=Entry(Add_CartFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(Add_CartFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_pprice=Entry(Add_CartFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)
        
        lbl_p_qty=Label(Add_CartFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_qty=Entry(Add_CartFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)
        

        self.lbl_instock=Label(Add_CartFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)
        
        btn_clearCart=Button(Add_CartFrame,command=self.clear_Cart,text="Clear",font=("times new roman",15,"bold"),bg="white",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_addCart=Button(Add_CartFrame,command=self.add_cart,text="Add | Update Cart",font=("times new roman",15,"bold"),bg="white",cursor="hand2").place(x=340,y=70,width=180,height=30)

        #billing area 
        bill_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        bill_frame.place(x=953,y=110,width=393,height=410)


        btitle=Label(bill_frame,text="User Bill Area",font=("goudy old style",20,"bold"),bg="lightgray",fg="black").pack(side=TOP,fill=X)

        scrolly3=Scrollbar(bill_frame,orient=VERTICAL)
        scrolly3.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(bill_frame,yscrollcommand=scrolly3.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)

        scrolly3.config(command=self.txt_bill_area.yview)


        #billing buttons
        bill_menuframe=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        bill_menuframe.place(x=953,y=520,width=393,height=140)

        self.lbl_amount=Label(bill_menuframe,text="Bill Amount \n[0]",font=('goudy old style',13,"bold"),bg="lightgray")
        self.lbl_amount.place(x=2,y=5,width=130,height=70)

        self.lbl_discount=Label(bill_menuframe,text="Discount \n[5%]",font=('goudy old style',13,"bold"),bg="lightgray")
        self.lbl_discount.place(x=124,y=5,width=130,height=70)

        self.lbl_netpay=Label(bill_menuframe,text="Net Pay \n[0]",font=('goudy old style',13,"bold"),bg="lightgray")
        self.lbl_netpay.place(x=246,y=5,width=140,height=70)


        btn_lbl_print=Button(bill_menuframe,command=self.print_bill,cursor="hand2",text="Print",font=('goudy old style',13,"bold"),bg="lightgray")
        btn_lbl_print.place(x=2,y=80,width=100,height=50)

        btn_lbl_clearall=Button(bill_menuframe,command=self.clearall,cursor="hand2",text="Clear",font=('goudy old style',13,"bold"),bg="lightgray")
        btn_lbl_clearall.place(x=103,y=80,width=100,height=50)

        btn_lbl_generate=Button(bill_menuframe,command=self.generate_bill,cursor="hand2",text="Generate/Save \n Bill ",font=('goudy old style',13,"bold"),bg="lightgray")
        btn_lbl_generate.place(x=200,y=80,width=187,height=50)

        self.show()
        self.updatetime()
        # self.bill_top()


    def get_input(self,num):
        xnum=self.var_calInput.get()+str(num)
        self.var_calInput.set(xnum)

    def clear_cal(self):
        self.var_calInput.set('')

    def perform_cal(self):
        result=self.var_calInput.get()
        self.var_calInput.set(eval(result))

    def show(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "products" )
        cursor=conn.cursor()
        try:
            cursor.execute("select * from products where Status='Active'")
            rows=cursor.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    
    
    def search(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "products" )
        cursor=conn.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cursor.execute("select * from products where  Name LIKE '%"+self.var_search.get()+"%'")
                rows=cursor.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set("1")

    def get_cartdata(self,ev):
        f=self.cart_Table.focus()
        content=(self.cart_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
       


    def add_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror('Error',"Select product from list",parent=self.root)

        elif self.var_qty.get()=='' :
                messagebox.showerror('Error',"Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
                messagebox.showerror('Error',"Invalid Quantity",parent=self.root)
        
        else:
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #update cart
            present='no'
            index=-1 #for product already present or not 
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm','Product already present.\n Do you want to  Update| Remove from Cart')
                if op==True:
                    if self.var_qty.get()=='0':
                        self.cart_list.pop(index)
                    else:
                        self.cart_list[index][3]= self.var_qty.get() #qty
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()



    def bill_updates(self):
        self.bill_amt=0
        self.netpay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amt=self.bill_amt+(float(row[2])*int(row[3]))  #price*qty
        self.discount=((self.bill_amt*5)/100)
        self.netpay=self.bill_amt-self.discount
        self.lbl_amount.config(text=f'Bill Amount\nRs.{str(self.bill_amt)}')
        self.lbl_netpay.config(text=f'Net Pay(Rs.)\n[{str(self.netpay)}]')
        self.cart_title.config(text=f"Cart \t Total Product:[{str(len(self.cart_list))}]")


    def show_cart(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "products" )
        cursor=conn.cursor()
        try:
            self.cart_Table.delete(*self.cart_Table.get_children())
            for row in self.cart_list:
                self.cart_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def generate_bill(self):
        if self.var_name.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Add Products to generate bill",parent=self.root)
        else:
            #bill top 
            self.bill_top()
            #bill middle
            self.bill_middle()
            #bill bottom
            self.bill_bottom()

            fp=open(f'/home/tanvi/Documents/intern/projects/assignment4-inventory/bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/Save in Backend",parent=self.root)
            self.chk_print=1


    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 98725***** , Delhi-125001
{str("="*47)}
 Customer Name: {self.var_name.get()}
 Ph no. :{self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)



    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
 Bill Amount\t\t\t\tRs.{self.bill_amt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.netpay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)
        


    def bill_middle(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "products" )
        cursor=conn.cursor()
        try:
            
            for row in self.cart_list:
            # pid,name,price,qty,stock
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                qty=str(qty)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                cursor.execute('Update products set Quantity=%s,Status=%s where pid=%s',[
                     qty,status,pid]
                    )
                conn.commit()
            conn.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


        
    def clear_Cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock ")
        self.var_stock.set('')

    def clearall(self):
        del self.cart_list[:]
        self.var_name.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cart_title.config(text=f"Cart \t Total Product:[0]")
        self.var_search.set("")
        self.chk_print=0
        self.clear_Cart()
        self.show()
        self.show_cart()

    def updatetime(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome!! \t\t Date:{str(date_)} \t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.updatetime)
    
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            pr=subprocess.Popen(new_file,stdin=subprocess.PIPE)
            pr.stdin.write(new_file)

        else: 
            messagebox.showerror("Print","Please generate bill",parent=self.root)
    

    def logout(self):
        self.root.destroy()
        os.system("python3 projects/assignment4-inventory/login.py")

                

if __name__==  "__main__":      
    root=Tk()   
    obj=BillClass(root)
    root.mainloop()  