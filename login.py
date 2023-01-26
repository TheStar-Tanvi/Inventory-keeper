from tkinter import *
from tkinter import messagebox
import pymysql as mydb
import os

class login_sys:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System")
        self.root.geometry("1100x500+0+0")

        #loginframe
        loginframe=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        loginframe.place(x=300,y=40,width=500,height=450)

        title=Label(loginframe,text="Login System",bg="lightblue",fg="black",font=("Elephant",30,"bold")).place(x=0,y=30,relwidth=1)

        lbl_user=Label(loginframe,text="UserName",font=("Andalus",15),bg="white").place(x=200,y=100)
        self.username=StringVar()
        self.password=StringVar()
        txt_username=Entry(loginframe,textvariable=self.username,font=("times new roman",15),bg="lightgray").place(x=125,y=140,width=250)

        lbl_pass=Label(loginframe,text="Password",font=("Andalus",15),bg="white").place(x=200,y=190)
        txt_password=Entry(loginframe,show='*',textvariable=self.password,font=("times new roman",15),bg="lightgray").place(x=125,y=240,width=250)

        loginbtn=Button(loginframe,command=self.login,cursor="hand2",activebackground="lightblue",text='Log in',font=("times new roman",15,"bold"),bg="lightblue").place(x=125,y=350,width=250,height=35)
        

    def login(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "login" )
        cursor=conn.cursor()
        try:
            if self.username.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","All fields required",parent=self.root)
            else:
                cursor.execute("select utype from users where name=%s AND pass=%s",[self.username.get(),self.password.get()])
                customer=cursor.fetchone()
                if customer==None:
                    messagebox.showerror("Error","Invalid Username/Password",parent=self.root)
                else:
                    if customer[0]=="admin":
                        self.root.destroy()
                        os.system("python3  dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python3  billing.py")

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)




root=Tk()
obj=login_sys(root)
root.mainloop()

