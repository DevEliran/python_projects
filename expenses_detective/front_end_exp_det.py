from tkinter import *
from exp_det import Database
from exp_det import Database_acc
import random
from tkinter import ttk
from tkinter import messagebox

cat_list=['groceries','shopping','bills','gym','electronics','car','hairstyle']
cat_list_new=['Auto','Entertainment','Groceries','Household','Investments','Misc','Utilities']
bank_names=['bankname1','bankname2','bankname3','bankname4','bankname5','bankname6']
account_options=['Credit card','Savings','Chequing']
db=Database()
db_acc=Database_acc()
#for i in range(5):
    #db_acc.insert(random.choice(bank_names),random.choice(account_options),random.randint(20,5000))

"""event triggered by clicking on a row in Combobox.
   lb is Listbox widget.
   selected_cat will store the selected category.
   db is the Database
"""
def get_selected_category(event):
    global selected_cat
    selected_cat=cat.get()
    lb.delete(0,END)
    for i in db.search_by_category(selected_cat):
        lb.insert(END,i)

"""event triggered by clicking on a row in Listbox.
   lb is Listbox widget.
   selected_tuple is a tuple which contains (id,category,cost)
"""
def get_selected_row(event):
        global selected_tuple
        #print(lb.curselection())
        index=lb.curselection()
        if index != ():
            selected_tuple=lb.get(index[0])
            print(selected_tuple)
            e1.delete(0,END)
            e1.insert(END,str(selected_tuple[3]))
            cat.delete(0,END)
            cat.insert(END,selected_tuple[1])
            e2.delete(0,END)
            e2.insert(END,selected_tuple[2])
            e3.configure(state=NORMAL)
            e3.delete(0,END)
            e3.insert(END,selected_tuple[4])
            e3.configure(state='readonly')

def add_command():
    db.insert(selected_cat,desc_entry.get(),cost_entry.get())
    lb.delete(0,END)
    for i in db.view():
        lb.insert(END,i)

def view_command():
    lb.delete(0,END)
    for i in db.view():
        lb.insert(END,i)

def delete_command():
    db.delete(selected_tuple[0])
    lb.delete(0,END)
    clear_entries()
    for i in db.search_by_category(selected_tuple[1]):
        lb.insert(END,i)

def update_command():
    db.update_cost_des(selected_tuple[0],desc_entry.get(),cost_entry.get())
    clear_entries()
    lb.delete(0,END)
    for i in db.search_by_category(selected_tuple[1]):
        lb.insert(END,i)

def get_selcted_row_tree(event):
    global selected_row_tree
    selected_row_tree= tree.identify_row(event.y)
    print(selected_row_tree)




def do_popup(event):
    global iid
    iid = tree.identify_row(event.y)
    try:
        if iid!='A' and iid!='B' and iid!='C' and iid!='D' and int(iid)>10:#popup(level2)
            tree.selection_set(iid)
            popup.post(event.x_root, event.y_root)
        else:#popup1(level1)
            tree.selection_set(iid)
            popup1.post(event.x_root, event.y_root)
    except ValueError:
        pass

def rename_window_creation():
    global rename_window
    rename_window=Tk()
    rename_window.iconbitmap(default="investor.ico")
    rename_window.minsize(250,50)
    rename_window.maxsize(250,50)
    rename_window.wm_title("Rename")
    rename_window.geometry("250x50")
    global renameVar
    renameVar=StringVar()
    rename_entry=ttk.Entry(rename_window,textvariable=renameVar)
    rename_entry.pack()
    save_button=ttk.Button(rename_window,text="Save",width=20,command=lambda:rename_bank(rename_entry.get(),selected_row_tree))
    save_button.pack()
    rename_window.mainloop()

def rename_bank(bank,iid):
    print(bank)
    print(iid)
    db_acc.cur.execute("UPDATE accounts SET bank=? WHERE iid=? ",(bank,iid))
    db_acc.con.commit()
    rename_window.destroy()
    tree.delete(*tree.get_children())
    build_tree()

def add_window_creation():
    global add_window
    add_window=Tk()
    add_window.iconbitmap(default="investor.ico")
    add_window.minsize(350,200)
    add_window.maxsize(350,200)
    add_window.wm_title("Add acount")
    add_window.geometry("350x200")

    account_entry=ttk.Entry(add_window)
    account_entry.pack()
    account_entry.delete(0,END)
    account_entry.configure(state=NORMAL)
    if iid=='A':
        account_entry.insert(END,'Cash')
    if iid=='B':
        account_entry.insert(END,'Chequing')
    if iid=='C':
        account_entry.insert(END,'Credit card')
    if iid=='D':
        account_entry.insert(END,'Savings')
    account_entry.configure(state='readonly')

    bank_nameVar=StringVar()
    l_bank_name=ttk.Label(add_window,text="Enter bank name : ")
    l_bank_name.pack()
    bank_name_entry=ttk.Entry(add_window,textvariable=bank_nameVar)
    bank_name_entry.pack()

    amountVar=StringVar()
    l_amount=ttk.Label(add_window,text="Enter amount : ")
    l_amount.pack()
    amount_entry=ttk.Entry(add_window,textvariable=amountVar)
    amount_entry.pack()

    save_button1=ttk.Button(add_window,text="Save",width=20,command=lambda:add_account(bank_name_entry.get(),amount_entry.get(),account_entry.get()))
    save_button1.pack()
    add_window.mainloop()

def add_account(bank,amount,account):
    db_acc.insert(bank,account,amount)
    add_window.destroy()
    tree.delete(*tree.get_children())
    build_tree()

def amount_window_creation():
    global update_window
    update_window=Tk()
    update_window.iconbitmap(default="investor.ico")
    update_window.minsize(250,50)
    update_window.maxsize(250,50)
    update_window.wm_title("Update amount")
    update_window.geometry("250x50")
    updateVar=StringVar()
    update_entry=ttk.Entry(update_window,textvariable=updateVar)
    update_entry.pack()
    print(selected_row_tree)
    print(update_entry.get())
    save_button2=ttk.Button(update_window,text="Save",width=20,command=lambda:update_amount(selected_row_tree,update_entry.get()))
    save_button2.pack()
    update_window.mainloop()

def get_selected_acc(event):
    global selected_acc
    selected_acc=accCombo.get()
    print(selected_acc)


def get_selected_bank(event):
    global selected_bank
    selected_bank=banks.get()
    print(selected_bank)



def transfer_cash(accFrom,accTo,bankFrom,bankTo,amount,radioChoice):
    msg=db_acc.transfer(accFrom,accTo,bankFrom,bankTo,amount,radioChoice)
    messagebox.showinfo(" ", msg)
    tree.delete(*tree.get_children())
    build_tree()

def update_amount(id,amount):
    db_acc.update_cash(id,amount)
    update_window.destroy()
    tree.delete(*tree.get_children())
    build_tree()

def delete_account():
    db_acc.delete_acc(iid)
    tree.delete(*tree.get_children())
    build_tree()

def clear_entries():
    e1.delete(0,END)
    e2.delete(0,END)
    e3.configure(state=NORMAL)
    e3.delete(0,END)
    e3.configure(state='readonly')

def clear_transfer_entries():
     transfer_from_entry_acc.delete(0,END)
     transfer_from_entry_bank.delete(0,END)
     transfer_to_entry_acc.delete(0,END)
     transfer_to_entry_bank.delete(0,END)
     amount_entry.delete(0,END)

def show_choice():
    print(radio_var.get())

def build_tree():
    #TREE LEVEL 1
    cash_folder=tree.insert('',1,'A',text="Cash",values=("$"+str(db_acc.get_cash_amount()),))
    cheq_folder=tree.insert('',2,'B',text="Chequing",values=("$"+str(db_acc.get_cheq_amount()),))
    credit_folder=tree.insert('',3,'C',text="Credit card",values=("$"+str(db_acc.get_credit_amount()),))
    savings_folder=tree.insert('',4,'D',text="Savings",values=("$"+str(db_acc.get_savings_amount()),))

    #TREE LEVEL 2
    print(db_acc.view_acc()[0][2])
    print(db_acc.get_number_of_rows())
    for i in range(db_acc.get_number_of_rows()):
        if str(db_acc.view_acc()[i][2]) == "Chequing":
            tree.insert(cheq_folder,1,"1"+str(i),text=db_acc.view_acc()[i][1],values=("$"+str(db_acc.view_acc()[i][3]),))
            id=db_acc.get_id(db_acc.view_acc()[i][1],db_acc.view_acc()[i][2],db_acc.view_acc()[i][3])
            db_acc.cur.execute("UPDATE accounts SET iid=? WHERE id=?",("1"+str(i),id[0][0]))
            db_acc.con.commit()

        if str(db_acc.view_acc()[i][2]) == "Credit card":
            tree.insert(credit_folder,2,"2"+str(i),text=db_acc.view_acc()[i][1],values=("$"+str(db_acc.view_acc()[i][3]),))
            id=db_acc.get_id(db_acc.view_acc()[i][1],db_acc.view_acc()[i][2],db_acc.view_acc()[i][3])
            db_acc.cur.execute("UPDATE accounts SET iid=? WHERE id=?",("2"+str(i),id[0][0]))
            db_acc.con.commit()

        if str(db_acc.view_acc()[i][2]) == "Savings":
            tree.insert(savings_folder,3,"3"+str(i),text=db_acc.view_acc()[i][1],values=("$"+str(db_acc.view_acc()[i][3]),))
            id=db_acc.get_id(db_acc.view_acc()[i][1],db_acc.view_acc()[i][2],db_acc.view_acc()[i][3])
            db_acc.cur.execute("UPDATE accounts SET iid=? WHERE id=?",("3"+str(i),id[0][0]))
            db_acc.con.commit()

        if str(db_acc.view_acc()[i][2]) == "Cash":
            tree.insert(cash_folder,3,"3"+str(i),text=db_acc.view_acc()[i][1],values=("$"+str(db_acc.view_acc()[i][3]),))
            id=db_acc.get_id(db_acc.view_acc()[i][1],db_acc.view_acc()[i][2],db_acc.view_acc()[i][3])
            db_acc.cur.execute("UPDATE accounts SET iid=? WHERE id=?",("3"+str(i),id[0][0]))
            db_acc.con.commit()


window=Tk()
window.iconbitmap(default="investor.ico")
window.minsize(600,500)
window.maxsize(600,500)
window.wm_title("Expenses Detective 1.0")
window.geometry("600x500")
#Adding tabs
tabControl=ttk.Notebook(window)
tabControl.place(x=0,y=0,width=600,height=500)

home_tab=ttk.Frame(tabControl)
tabControl.add(home_tab,text="Home")

acc_tab=ttk.Frame(tabControl)
tabControl.add(acc_tab,text="My Accounts")

db_tab=ttk.Frame(tabControl)
tabControl.add(db_tab,text=r"View\Update")

queries_tab=ttk.Frame(tabControl)
tabControl.add(queries_tab,text="Queries")

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#HOME TAB

l1=Label(home_tab,text="Expenses Detective",bg="grey",width=200,font=("Courier",32),relief=GROOVE)
l1.place(x=0,y=0,width=600,height=100)
text=Label(home_tab,text="Expenses Detective helps you keep track on your daily expenses. \n\n Under my accounts tab you can list your various bank accounts . \n\n Under Add or update tab you can list your day to day expenses \n\n Queries tab will provide you with graphs and charts regarding your data.",height=500,width=600,anchor=N,background="light grey")
text.place(x=0,y=100,width=600,height=500)
l_credit=Label(home_tab,text="Icon made by Eucalyp from www.flaticon.com")
l_credit.place(x=0,y=460,width=250,height=15)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#MY ACCOUNTS TAB
l_net_worth=ttk.Label(acc_tab,text="Total Net Worth = "+"$"+str(db_acc.get_net_worth()))
l_net_worth.place(x=0,y=253,width=150,height=20)

tree=ttk.Treeview(acc_tab)
tree.place(x=0,y=0,width=400,height=250)
tree["columns"]=("one")
tree.column("#0",width=270, minwidth=270, stretch=NO)
tree.column("one",width=270, minwidth=270, stretch=NO)
#tree.column("two",width=270, minwidth=270, stretch=tk.NO)

tree.heading("#0",text="Account",anchor=W)
tree.heading("one",text="Amount",anchor=W)

build_tree()
popup=Menu(acc_tab,tearoff=0)
popup.add_command(label="Rename",command=rename_window_creation)#for level 2
popup.add_command(label="Update amount",command=amount_window_creation)
popup.add_command(label="Delete account",command=delete_account)

popup1=Menu(acc_tab,tearoff=0)
popup1.add_command(label="Add account",command=add_window_creation)#for level 1

tree.bind("<Button-3>",do_popup)
tree.bind("<ButtonRelease-3>",get_selcted_row_tree)
tree.bind("<ButtonRelease-1>",get_selcted_row_tree)


transfer_label=ttk.Label(acc_tab,text="Transfer Money Between Accounts : ")
transfer_label.place(x=150, y=285,width=200,height=25)
from_header=ttk.Label(acc_tab,text="From :")
from_header.place(x=50,y=320,width=150,height=25)
to_header=ttk.Label(acc_tab,text="To :")
to_header.place(x=240,y=320,width=150,height=25)
#FROM SECTION
transfer_from_label_acc=ttk.Label(acc_tab,text="Account :")
transfer_from_label_acc.place(x=0 , y=350,width=150,height=25)
transfer_from_var_acc=StringVar()
transfer_from_entry_acc=ttk.Entry(acc_tab,textvariable=transfer_from_var_acc)
transfer_from_entry_acc.place(x=60,y=350,width=100,height=25)

transfer_from_label_bank=ttk.Label(acc_tab,text="Bank :")
transfer_from_label_bank.place(x=0 , y=380,width=150,height=25)
transfer_from_var_bank=StringVar()
transfer_from_entry_bank=ttk.Entry(acc_tab,textvariable=transfer_from_var_bank)
transfer_from_entry_bank.place(x=60,y=380,width=100,height=25)

#TO SECTION
transfer_to_label_acc=ttk.Label(acc_tab,text="Account :")
transfer_to_label_acc.place(x=180 , y=350,width=150,height=25)
transfer_to_var_acc=StringVar()
transfer_to_entry_acc=ttk.Entry(acc_tab,textvariable=transfer_to_var_acc)
transfer_to_entry_acc.place(x=240,y=350,width=100,height=25)

transfer_to_label_bank=ttk.Label(acc_tab,text="Bank :")
transfer_to_label_bank.place(x=180 , y=380,width=150,height=25)
transfer_to_var_bank=StringVar()
transfer_to_entry_bank=ttk.Entry(acc_tab,textvariable=transfer_to_var_bank)
transfer_to_entry_bank.place(x=240,y=380,width=100,height=25)

amount_label=ttk.Label(acc_tab,text="Amount :")
amount_label.place(x=360,y=365,width=100,height=25)
amount_var=StringVar()
amount_entry=ttk.Entry(acc_tab,textvariable=amount_var)
amount_entry.place(x=425,y=365,width=100,height=25)

commit_transfer=ttk.Button(acc_tab,text="Commit Transfer",command=lambda:transfer_cash(transfer_from_entry_acc.get(),transfer_to_entry_acc.get(),transfer_from_entry_bank.get(),transfer_to_entry_bank.get(),amount_entry.get(),radio_var.get()))
commit_transfer.place(x=330,y=425,width=100,height=25)
clear_transfer=ttk.Button(acc_tab,text="Clear Entries",command=clear_transfer_entries )
clear_transfer.place(x=225,y=425,width=100,height=25)
radio_var=IntVar()
radio_option1=ttk.Radiobutton(acc_tab,text="Allow negative amount",variable=radio_var,value=1,command=show_choice)
radio_option1.place(x=370,y=280,width=150,height=25)
radio_option2=ttk.Radiobutton(acc_tab,text="Don't Allow negative amount",variable=radio_var,value=2,command=show_choice)
radio_option2.place(x=370,y=310,width=190,height=25)
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#ADD\UPDATE TAB
lb=Listbox(db_tab,height=15,width=30,exportselection=False)
lb.place(x=0,y=0,width=250,height=450)
lb.bind('<<ListboxSelect>>',get_selected_row)

scroll=Scrollbar(db_tab)
scroll.place(x=255,y=150,width=15,height=200)

lb.configure(yscrollcommand=scroll.set)
scroll.configure(command=lb.yview)

b1=ttk.Button(db_tab,text="View All Expenses",width=20,command=view_command)
b1.place(x=300,y=250,width=140,height=25)

b2=ttk.Button(db_tab,text="Delete Row",width=12,command=delete_command)
b2.place(x=445 ,y=250,width=120,height=25 )

b3=ttk.Button(db_tab,text=r"Update Cost\Description",width=40,command=update_command)
b3.place(x=300 ,y=280,width=140,height=25 )

b4=ttk.Button(db_tab,text="Add Expense",width=12,command=add_command)
b4.place(x=445 ,y=280,width=120,height=25 )

l2=Label(db_tab,text="Choose a Category : ",width=60,font=("David",10))
l2.place(x=260,y=0,width=170,height=20)

categoryVar = StringVar()
cat = ttk.Combobox(db_tab, textvariable=categoryVar)
cat.bind('<<ComboboxSelected>>', get_selected_category)
cat['values']=('groceries','shopping','bills','gym','electronics','car','hairstyle')
cat.place(x=270,y=20,width=130,height=30)


cost_entry=StringVar()
l3=ttk.Label(db_tab,text= "Cost : ",width=60,font=('David',10))
l3.place(x=450,y=0,width=60,height=20)
l5=ttk.Label(db_tab,text="USD",width=60,font=('David',10))
l5.place(x=515,y=25,width=60,height=20)
e1=ttk.Entry(db_tab,textvariable=cost_entry)
e1.place(x=450,y=20,width=60,height=30)

desc_entry=StringVar()
l4=ttk.Label(db_tab,text=r"Description\Notes :", width= 150, font=('David',10))
l4.place(x=270 ,y=50,width=150,height=25)
e2=ttk.Entry(db_tab,textvariable=desc_entry)
e2.place(x=270,y=75,width=250,height=25)

time_stamp_entry=StringVar()
l4=ttk.Label(db_tab,text="Time stamp :", width= 150, font=('David',10))
l4.place(x=270 ,y=105,width=150,height=25)
e3=ttk.Entry(db_tab,state='readonly',textvariable=time_stamp_entry)
e3.place(x=270,y=130,width=150,height=25)

clear_entries_tab3=ttk.Button(db_tab,text="Clear Entries",command=clear_entries)
clear_entries_tab3.place(x=375,y=315,width=150,height=25)
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#QUERIES TAB


window.mainloop()
