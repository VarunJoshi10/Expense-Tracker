from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
from random import randint
import customtkinter
import tkinter.messagebox as tkmsg
from tkcalendar import DateEntry
from pymongo import MongoClient

try:
    client=MongoClient(port=27017)
    db=client.Practical9
    expense=db['expense']
    print("Connected to MongoDB")
except:
    print("Database connection Error")
    tkmsg.showerror("Error","Connection Failed")
    sys.exit(1)


def total():
    fuel_total=expense.aggregate([{"$match":{"TYPE":"Fuel"}},{"$group":{"_id":"$TYPE","total":{"$sum":"$COST"}}}])
    food_total=expense.aggregate([{"$match":{"TYPE":"Food"}},{"$group":{"_id":"$TYPE","total":{"$sum":"$COST"}}}])
    gift_total=expense.aggregate([{"$match":{"TYPE":"Gift"}},{"$group":{"_id":"$TYPE","total":{"$sum":"$COST"}}}])
    others_total=expense.aggregate([{"$match":{"TYPE":"Others"}},{"$group":{"_id":"$TYPE","total":{"$sum":"$COST"}}}])
    t1=list(fuel_total)
    global ft,fot,gt,ot
    if(len(t1)==0):
        ft=0
    else:
        ft=t1[0]['total']
    t1=list(food_total)
    if(len(t1)==0):
        fot=0
    else:
        fot=t1[0]['total']
    t1=list(gift_total)
    if(len(t1)==0):
        gt=0
    else:
        gt=t1[0]['total']
    t1=list(others_total)
    if(len(t1)==0):
        ot=0
    else:
        ot=t1[0]['total']
    global total_cost
    total_cost=ft+fot+gt+ot
    print(total_cost)

def stats():
    thirdlvl=customtkinter.CTkToplevel(root)
    thirdlvl.geometry("400x400")
    frameChartsLT = customtkinter.CTkFrame(thirdlvl)
    frameChartsLT.pack()

    stockListExp = ['Fuel' , 'Gift', 'Food', 'Others']
    stockSplitExp = [ft,gt,fot,ot]

    fig = Figure() # create a figure object
    ax = fig.add_subplot(111) # add an Axes to the figure

    ax.pie(stockSplitExp, labels=stockListExp,autopct='%0.2f%%')
    ax.legend()

    chart1 = FigureCanvasTkAgg(fig,frameChartsLT)
    chart1.get_tk_widget().pack()



def add_data():
    type_data=exptype.get()
    cost_data=int(cost_text.get())
    desc_data=desc_area.get('0.0',END).strip()
    date_data=str(cal.get_date())
    print(type_data)
    print(cost_data)
    print(desc_data)
    print(date_data)
    TYPE=[type_data]
    COST=[cost_data]
    DESC=[desc_data]
    DATE=[date_data]
    Practical9={
        'TYPE' : TYPE[randint(0, (len(TYPE)-1))],
        'COST' : COST[randint(0, (len(COST)-1))],
        'DESC' : DESC[randint(0, (len(DESC)-1))],
        'DATE' : DATE[randint(0, (len(DATE)-1))]
    }

    if(len(type_data)==0 or cost_data==0 or date_data==None or len(desc_data)==0):
        tkmsg.showwarning("WARNING", "All fields are compulsory")
        return
    elif len(desc_data)!=0:
        result=db.expense.insert_one(Practical9)
    else:
        tkmsg.showwarning("ERROR", "Unknown Error")
        return
    
    total_value.configure(state="normal")
    total_value.delete(0,END)
    total()
    total_value.insert(0,total_cost)
    total_value.configure(state="disabled")
    firstlvl.destroy()
    tkmsg.showinfo("Add Expense", "Expense Added")



def add_expense():
    global firstlvl
    firstlvl= customtkinter.CTkToplevel(root)
    firstlvl.geometry('400x400')
    firstlvl.title("Add Expense")
    type_label=customtkinter.CTkLabel(firstlvl,text="TYPE")
    type_label.place(x=20,y=50)
    global exptype
    exptype=customtkinter.CTkComboBox(firstlvl,values=["Food","Fuel","Gift","Others"])
    exptype.place(x=110,y=50)
    cost_label=customtkinter.CTkLabel(firstlvl,text="COST")
    cost_label.place(x=20,y=90)
    global cost_text
    cost_text=customtkinter.CTkEntry(firstlvl)
    cost_text.place(x=110,y=90)
    desc_label=customtkinter.CTkLabel(firstlvl,text="Desciption")
    desc_label.place(x=20,y=130)
    global desc_area
    desc_area=Text(firstlvl,width=20,height=5)
    desc_area.place(x=130,y=130)
    date_label=customtkinter.CTkLabel(firstlvl,text="DATE")
    date_label.place(x=20,y=250)
    global cal
    cal=DateEntry(firstlvl,selectmode='day')
    cal.place(x=130,y=250)
    sub_btn=customtkinter.CTkButton(firstlvl,text="Submit",command=add_data)
    sub_btn.place(x=130,y=300)

def del_data():
    def delete():
        type=exptype.get()
        desc=desc_area.get('0.0',END).strip()
        date=str(cal.get_date())
        if(len(type)==0 or len(desc)==0 or len(date)==0):
            tkmsg.showwarning("WARNING", "Enter all info")
            return
        if db.expense.count_documents({ 'DATE': date }, limit = 1)==0:
            tkmsg.showwarning("ERROR", "Data Does Not Exist")
            return
        else:
            my_query={'DATE':date,'TYPE':type,'DESC':desc}
            print(my_query)
            db.expense.delete_one(my_query)
        total_value.configure(state="normal")
        total_value.delete(0,END)
        total()
        total_value.insert(0,total_cost)
        total_value.configure(state="disabled")
        newwin.destroy()
        tkmsg.showinfo("Delete Student", "Student Deleted")
    newwin=customtkinter.CTkToplevel(root)
    newwin.geometry('400x350')
    newwin.title("Delete STUDENT")
    type_label=customtkinter.CTkLabel(newwin,text="TYPE")
    type_label.place(x=20,y=50)
    global exptype
    exptype=customtkinter.CTkComboBox(newwin,values=["Food","Fuel","Gift","Others"])
    exptype.place(x=110,y=50)
    desc_label=customtkinter.CTkLabel(newwin,text="Desciption")
    desc_label.place(x=20,y=130)
    global desc_area
    desc_area=Text(newwin,width=20,height=5)
    desc_area.place(x=130,y=130)
    date_label=customtkinter.CTkLabel(newwin,text="DATE")
    date_label.place(x=20,y=250)
    global cal
    cal=DateEntry(newwin,selectmode='day')
    cal.place(x=130,y=250)
    sub = customtkinter.CTkButton(newwin, text="Delete Entry", command=delete)
    sub.place(x=120, y=300)



def upd_data():
    def update():
        type1=exptype1.get()
        desc1=desc_area1.get('0.0',END).strip()
        date1=str(cal1.get_date())
        
        if(len(type1)==0 or len(desc1)==0 or len(date1)==0):
            tkmsg.showwarning("WARNING", "Enter all info")
            return
        if db.expense.count_documents({ 'DATE': date1 }, limit = 1)==0:
            tkmsg.showwarning("ERROR", "Data Does Not Exist")
            return
        else:
            def upd():
                print("in function")
                upd_type=exptype2.get()
                upd_desc=desc_area2.get('0.0',END).strip()
                upd_date=str(cal2.get_date())
                cost_data=int(cost_text2.get())

                if(len(upd_type)==0 or len(upd_desc)==0 or len(upd_date)==0 or cost_data==0):
                    tkmsg.showwarning("WARNING", "Enter all info")
                    return
                else:
                    new_query={'DATE':upd_date,'TYPE':upd_type,'DESC':upd_desc,'COST':cost_data}
                    print(new_query)
                    db.expense.update_one(my_query,{'$set':new_query})
                    mywin.destroy()
                    total_value.configure(state="normal")
                    total_value.delete(0,END)
                    total()
                    total_value.insert(0,total_cost)
                    total_value.configure(state="disabled")
                    newwin.destroy()
                    tkmsg.showinfo("update", "Update Data")


            my_query={'DATE':date1,'TYPE':type1,'DESC':desc1}
            print(my_query)
            mywin=customtkinter.CTkToplevel(newwin)
            mywin.geometry('400x350')
            mywin.title("Update Expense")
            type_label=customtkinter.CTkLabel(mywin,text="TYPE")
            type_label.place(x=20,y=50)
            exptype2=customtkinter.CTkComboBox(mywin,values=["Food","Fuel","Gift","Others"])
            exptype2.place(x=110,y=50)
            cost_label=customtkinter.CTkLabel(mywin,text="COST")
            cost_label.place(x=20,y=90)
            cost_text2=customtkinter.CTkEntry(mywin)
            cost_text2.place(x=110,y=90)
            desc_label=customtkinter.CTkLabel(mywin,text="Desciption")
            desc_label.place(x=20,y=130)
            desc_area2=Text(mywin,width=20,height=5)
            desc_area2.place(x=130,y=130)
            date_label=customtkinter.CTkLabel(mywin,text="DATE")
            date_label.place(x=20,y=250)
            cal2=DateEntry(mywin,selectmode='day')
            cal2.place(x=130,y=250)
            sub_btn1=customtkinter.CTkButton(mywin,text="Submit",command=upd)
            sub_btn1.place(x=130,y=300)
            print("Hello")


    newwin=customtkinter.CTkToplevel(root)
    newwin.geometry('400x350')
    newwin.title("Update Data")
    type_label=customtkinter.CTkLabel(newwin,text="TYPE")
    type_label.place(x=20,y=50)
    exptype1=customtkinter.CTkComboBox(newwin,values=["Food","Fuel","Gift","Others"])
    exptype1.place(x=110,y=50)
    desc_label=customtkinter.CTkLabel(newwin,text="Desciption")
    desc_label.place(x=20,y=130)
    desc_area1=Text(newwin,width=20,height=5)
    desc_area1.place(x=130,y=130)
    date_label=customtkinter.CTkLabel(newwin,text="DATE")
    date_label.place(x=20,y=250)
    cal1=DateEntry(newwin,selectmode='day')
    cal1.place(x=130,y=250)
    sub = customtkinter.CTkButton(newwin, text="Update Entry", command=update)
    sub.place(x=120, y=300)


def show_details():
    secondlvl= customtkinter.CTkToplevel(root)
    secondlvl.geometry('550x400')
    secondlvl.title("Expense Details")
    main_frame=customtkinter.CTkFrame(secondlvl)
    main_frame.pack(fill=BOTH,expand=1)
    my_canvas=customtkinter.CTkCanvas(main_frame)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    scrollbar=customtkinter.CTkScrollbar(main_frame,orientation=VERTICAL,command=my_canvas.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>',lambda E:my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    second_frame=customtkinter.CTkFrame(my_canvas)
    my_canvas.create_window((0,0),window=second_frame,anchor="nw")
    l1=customtkinter.CTkLabel(second_frame,text="DATE")
    l1.grid(row=0,column=0)
    l2=customtkinter.CTkLabel(second_frame,text="TYPE")
    l2.grid(row=0,column=2)
    l3=customtkinter.CTkLabel(second_frame,text="COST")
    l3.grid(row=0,column=4)
    l4=customtkinter.CTkLabel(second_frame,text="DESCRIPTION")
    l4.grid(row=0,column=6)
    i=1
    for x in db.expense.find():
        y=len(x)
        l1=customtkinter.CTkLabel(second_frame,text=x['DATE'])
        l1.grid(row=i,column=0)
        l2=customtkinter.CTkLabel(second_frame,text=x['TYPE'])
        l2.grid(row=i,column=2)
        l3=customtkinter.CTkLabel(second_frame,text=x['COST'])
        l3.grid(row=i,column=4)
        l4=customtkinter.CTkLabel(second_frame,text=x['DESC'])
        l4.grid(row=i,column=6)
        i+=1


#GUI
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
root=customtkinter.CTk()
root.geometry('400x400')
root.title("Expense Tracker")

head=customtkinter.CTkLabel(root,text="Expense Tracker",text_font=("Arial",20,"bold"))
head.place(x=95,y=20)

total_exp_label=customtkinter.CTkLabel(root,text="TOTAL EXPENSE")
total_exp_label.place(x=95,y=90)


total_value=customtkinter.CTkEntry(root,state=DISABLED,width=50)
total()
total_value.place(x=250,y=90)
total_value.configure(state="normal")
total_value.delete(0,END)
total_value.insert(0,total_cost)
total_value.configure(state="disabled")



add_exp=customtkinter.CTkButton(root,text="Add Expense",command=add_expense)
add_exp.place(x=95,y=155)

del_exp=customtkinter.CTkButton(root,text="Delete Expense",command=del_data)
del_exp.place(x=95,y=195)

upd_exp=customtkinter.CTkButton(root,text="Update Expense",command=upd_data)
upd_exp.place(x=95,y=235)

show_exp=customtkinter.CTkButton(root,text="Show Expense",command=show_details)
show_exp.place(x=95,y=275)

stats_exp=customtkinter.CTkButton(root,text="Statistic",command=stats)
stats_exp.place(x=95,y=315)

develop=customtkinter.CTkLabel(root,text="Developed by: Varun,Varunpreet & Raman ")
develop.place(x=95,y=360)
root.mainloop()