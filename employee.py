from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image
import pymysql as mydb


class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x700+220+130")
        self.root.title("Invetory Keeper(TorcAI)-USERS")
        self.root.config(bg="white")
        self.root.focus_force() 

        self.var_searchby=StringVar()
        self.var_searchtext=StringVar()
        self.var_eid=IntVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()

        searchframe=LabelFrame(self.root,text="Search User",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        searchframe.place(x=20,y=20,width=600,height=70)


        cmb_search=ttk.Combobox(searchframe,textvariable=self.var_searchby,values=("select" ,"email","Name","Contact"),state='readonly',justify=CENTER,font=("goudy old style",12,"bold") )
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)


        txt_search=Entry(searchframe,textvariable=self.var_searchtext,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(searchframe,text="Search",command=self.search,font=("goudy old style",15),bg="green",fg="white").place(x=410,y=9,width=150,height=30)
        
        btn_add=Button(self.root,text="Add",command=self.add,font=("goudy old style",15),bg="green",fg="white").place(x=650,y=45,width=120,height=30)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="green",fg="white").place(x=800,y=45,width=120,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="green",fg="white").place(x=950,y=45,width=120,height=30)
        
        # title=Label(self.root,text="User Details",font=("goudy old style",15),fg="black").place(x=50,y=100,width=1000)
        details_frame=Frame(self.root,relief=RIDGE)
        details_frame.place(x=0,y=100,relwidth=1,height=190)



        User_id=Label(details_frame,text="User ID:",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        User_id.place(x=10,y=10,width=120,height=30)
        user_name=Label(details_frame,text="UserName:",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        user_name.place(x=10,y=70,width=120,height=30)
        Contact=Label(details_frame,text="CONTACT:",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        Contact.place(x=10,y=130,width=120,height=30)
        Email_lbl=Label(details_frame,text="EMAIL:",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        Email_lbl.place(x=600,y=10,width=120,height=30)
        pass_lbl=Label(details_frame,text="PASSWORD:",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        pass_lbl.place(x=600,y=70,width=120,height=30)
        Usertype_lbl=Label(details_frame,text="USER TYPE:",bg="white",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE)
        Usertype_lbl.place(x=600,y=130,width=120,height=30)

        txt_userid=Entry(details_frame,textvariable=self.var_eid,font=("goudy old style",15),bg="lightyellow").place(x=140,y=10,width=400)
        txt_username=Entry(details_frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=140,y=70,width=400)
        txt_contact=Entry(details_frame,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=140,y=130,width=400)
        txt_mail=Entry(details_frame,textvariable=self.var_email,font=("goudy old style",15),bg="lightyellow").place(x=740,y=10,width=350)
        txt_pswd=Entry(details_frame,textvariable=self.var_pass,font=("goudy old style",15),bg="lightyellow").place(x=740,y=70,width=350)
        txt_utype=Entry(details_frame,textvariable=self.var_utype,font=("goudy old style",15),bg="lightyellow").place(x=740,y=130,width=350)
        

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=300,relwidth=1,height=370)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","contact","email","pass","utype"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading("eid",text="User_ID")
        self.EmployeeTable.heading("name",text="Name")
        self.EmployeeTable.heading("contact",text="Contact")
        self.EmployeeTable.heading("email",text="Email")
        self.EmployeeTable.heading("pass",text="Password")
        self.EmployeeTable.heading("utype",text="User Type")
        self.EmployeeTable["show"]="headings"
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind('<ButtonRelease-1>',self.get_data)

        self.EmployeeTable.column("eid",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("email",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.show()

    def show(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "login" )
        cursor=conn.cursor()
        try:
            cursor.execute("select * from users")
            rows=cursor.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def search(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "login" )
        cursor=conn.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select search by option",parent=self.root)
            elif self.var_searchtext.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cursor.execute("select * from users where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtext.get()+"%'")
                rows=cursor.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    
    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        self.var_eid.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.var_email.set(row[3])
        self.var_pass.set(row[4])
        self.var_utype.set(row[5])
    



    def add(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "login" )
        cursor=conn.cursor()
        try:
            if self.var_eid.get()=="" or self.var_name.get()=="":
                messagebox.showerror("Error","Employee Id/name required",parent=self.root)
            else:
                cursor.execute("select * from users where eid=%s",[self.var_eid.get(),])
                row=cursor.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Employee Id already assigned",parent=self.root)
                else:
                    cursor.execute('Insert into users(eid,name,contact,email,pass,utype) VALUES (%s,%s,%s,%s,%s,%s)',[
                                        self.var_eid.get(),
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.var_email.get(),
                                        self.var_pass.get(),
                                        self.var_utype.get()]
                                    )
                    conn.commit()
                    messagebox.showinfo("Info","User added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def update(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "login" )
        cursor=conn.cursor()
        try:
            if self.var_eid.get()=="":
                messagebox.showerror("Error","Employee Id required",parent=self.root)
            else:
                cursor.execute("select * from users where eid=%s",[self.var_eid.get(),])
                row=cursor.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee Id ",parent=self.root)
                else:
                    cursor.execute('Update users set name=%s,contact=%s,email=%s,pass=%s,utype=%s where eid=%s ',[
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.var_email.get(),
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.var_eid.get(),]
                                    )
                    conn.commit()
                    messagebox.showinfo("Info","User updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)


    def delete(self):
        conn=mydb.connect(host= "127.0.0.1",user= "root" ,passwd= "password" ,db= "login" )
        cursor=conn.cursor()
        try:
            if self.var_eid.get()=="":
                messagebox.showerror("Error","Employee Id required",parent=self.root)
            else:
                cursor.execute("select * from users where eid=%s",[self.var_eid.get(),])
                row=cursor.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee Id ",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you want to delete user?",parent=self.root)
                    if op==True:
                        cursor.execute("delete from users where eid=%s",[self.var_eid.get(),])
                        conn.commit()
                        messagebox.showinfo("Info","User deleted successfully",parent=self.root)
                        self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)





if __name__==  "__main__":      
    root=Tk()   
    obj=employeeClass(root)
    root.mainloop() 