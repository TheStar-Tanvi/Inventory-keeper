from tkinter import *
from PIL import Image
from employee import employeeClass
from product import productClass
from sales import SalesClass
import pymysql as mydb
from tkinter import messagebox
import os,time

class System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Keeper(TorcAI)")
        self.root.config(bg="white")
        #title
        # self.icon_title=PhotoImage(file="/home/tanvi/Documents/intern/projects/assignment4-inventory/images/rsz_torcicon.png") 
        title=Label(self.root,text="Inventory Keeper",font=("times new roman",40,"bold"),bg="black",fg="white",anchor="center").place(x=0,y=0,relwidth=1,height=70)
         
        #button
        btn_logout=Button(self.root,command=self.logout,text="Logout",font=("times new roman",15,"bold"),bg="blue",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        # #clock
        self.lbl_clock=Label(self.root,text="Welcome!! \t\t Date:DD-MM-YY \t\t Time: HH:MM:SS",font=("times new roman",15),bg="lightgray",fg="black")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #left menu
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=120,width=1372,height=70)

        # lbl_Menu=Label(LeftMenu,text="Menu",font=("times new roman",20,"bold")).place(x=0,y=123,width=350,height=50)
        lbl_employee=Button(LeftMenu,text="Users",font=("times new roman",20,"bold"),cursor="hand2" ,command=self.employee).place(x=1,y=10,width=250,height=50)
        lbl_product=Button(LeftMenu,text="Products",font=("times new roman",20,"bold"),cursor="hand2",command=self.product).place(x=350,y=10,width=250,height=50)
        lbl_sales=Button(LeftMenu,text="Sales",font=("times new roman",20,"bold"),cursor="hand2",command=self.sales).place(x=710,y=10,width=250,height=50)
        lbl_exit=Button(LeftMenu,text="Exit",font=("times new roman",20,"bold"),cursor="hand2",command=quit).place(x=1070,y=10,width=250,height=50)


        self.lbl_employee=Label(self.root,text="Users \n[0]",relief=RIDGE,font=("goudy old style",20,),bg="lightgray",fg="black")
        self.lbl_employee.place(x=100,y=300,height=150,width=300)
        self.lbl_product=Label(self.root,text="Products\n[0]",relief=RIDGE,font=("goudy old style",20,),bg="lightgray",fg="black")
        self.lbl_product.place(x=500,y=300,height=150,width=300)
        self.lbl_sales=Label(self.root,text="Sales \n[0]",relief=RIDGE,font=("goudy old style",20,),bg="lightgray",fg="black")
        self.lbl_sales.place(x=900,y=300,height=150,width=300)

        
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome!! \t\t Date:{str(date_)} \t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_content)

        self.update_content()

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SalesClass(self.new_win)

    def update_content(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "products" )
        conn2=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "login" )
        cursor=conn.cursor()
        cursor2=conn2.cursor()

        try:
            cursor.execute("select * from products")
            product=cursor.fetchall()
            self.lbl_product.config(text=f'Total Product\n[{str(len(product))}]')

            cursor2.execute("select * from users")
            user=cursor2.fetchall()
            self.lbl_employee.config(text=f'Total Users\n[{str(len(user))}]')
            bills=len(os.listdir('/home/tanvi/Documents/intern/projects/assignment4-inventory/bill'))
            self.lbl_sales.config(text=f'Total Sales\n[{str(bills)}]')

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python3 projects/assignment4-inventory/login.py")

if __name__==  "__main__":      
    root=Tk()   
    obj=System(root)
    root.mainloop()  