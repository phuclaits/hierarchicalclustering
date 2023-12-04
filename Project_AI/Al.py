import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import csv
import time
import ttkthemes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
count = 0
text =''
def slider():
    global text,count
    if count==len(s):
        count = 0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(700,slider)
def clock():
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)
    
filetypes=(
            ('csv files', '*.csv'),
            ('text files','*.txt'),
            ('All files', '*.*')
        )   
#connection db 
#db  = mysql.connector.connect(user='root',password='123456',host='localhost',db='test1')
#mycursor = db.cursor()
#_Channel,_Region,_Fresh,_Milk,_Grocery,_Frozen,_Detergents_Paper,_Delicassen

def remove_stropen(path):
  return path.replace("(", "").replace(")", "").replace("'", "").replace(":", ":").replace("/", "/").replace(",","")
def Analyst_data():
    url_open = filedialog.askopenfilenames(
        title='Open files',
        initialdir='/',
        filetypes=filetypes)
    
    link = remove_stropen(str(url_open))
    data = pd.read_csv(str(link))
    print(len(data))
    #the model might become biased towards the variables with a higher magnitude
    data_scaled = normalize(data)
    #Channel,Region,Fresh,Milk,Grocery,Frozen,Detergents_Paper,Delicassen
    data_scaled = pd.DataFrame(data_scaled, columns=data.columns)
    # print(data_scaled['Channel'][1])
    with open ("datascale.csv",mode="w") as csvfile:
        fieldnames = ["Channel","Region","Fresh","Milk","Grocery","Frozen","Detergents_Paper","Delicassen"]
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        i = 0
        for i in range(len(data)):
            writer.writerow({"Channel": data_scaled['Channel'][i],"Region": data_scaled['Region'][i], "Fresh": data_scaled['Fresh'][i], "Milk": data_scaled['Milk'][i],"Grocery": data_scaled['Grocery'][i],"Frozen": data_scaled['Frozen'][i],"Frozen": data_scaled['Frozen'][i],"Detergents_Paper": data_scaled['Detergents_Paper'][i],"Delicassen": data_scaled['Delicassen'][i] })
    #Dendrogram
    plt.figure(figsize=(10, 7))  
    plt.title("Dendrograms")
    z = shc.linkage(data_scaled, method='ward')

    dend = shc.dendrogram(z)
    plt.axhline(y=0.75, color='r', linestyle='--')
    cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    cluster.fit_predict(data_scaled)
    cluster.labels_
    plt.figure(figsize=(7, 7))  
    plt.scatter(data_scaled['Milk'], data_scaled['Grocery'], c=cluster.labels_)
    plt.figure(figsize=(7, 7))  
    plt.scatter(data['Milk'], data['Grocery'], c=cluster.labels_)
    plt.show()

def export_data():
    url=filedialog.asksaveasfilename(filetypes=filetypes,defaultextension='.csv')
    indexing = Element_table.get_children()
    newlist =[]
    for index in indexing:
        content = Element_table.item(index)
        datalist = content['values']
        newlist.append(datalist)
    
    table=pd.DataFrame(newlist,columns=['Channel','Region','Fresh','Milk','Grocery','Frozen','Detergents_Paper','Delicassen'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Sucess','Data is saved sucessfully')

def update_Element():
    def update_data():
        query = 'update overview set _Channel = (%s) , _Region = (%s) , _Fresh = (%s) , _Milk = (%s) , _Grocery = (%s) , _Frozen = (%s) , _Detergents_Paper =(%s) , _Delicassen = (%s) where _Channel = (%s) and _Region = (%s) and _Fresh = (%s) and _Milk = (%s) and _Grocery = (%s) and _Frozen = (%s) and _Detergents_Paper =(%s) and _Delicassen = (%s)'
        mycursor.execute(query,(channelEntry.get(),RegionEntry.get(),FreshEntry.get(),MilkEntry.get(),GroceryEntry.get(),FrozenEntry.get(),Detergents_PaperEntry.get(),DelicassenEntry.get(),str(listdata[0]),str(listdata[1]),str(listdata[2]),str(listdata[3]),str(listdata[4]),str(listdata[5]),str(listdata[6]),str(listdata[7])))
        con.commit()
        messagebox.showinfo('Success',f'This is modifield successfully!',parent=update_window)
        update_window.destroy()
        show_Element()
    
    
    update_window = Toplevel()
    update_window.title('Update Element')
    update_window.grab_set()
    update_window.resizable(False,False)
    
    channelLabel = Label(update_window,text='Channel',font=('time new roman',15,'bold'))
    channelLabel.grid(row = 0,column=0,padx=30,pady=15,sticky=W)
    channelEntry = Entry(update_window,font=('roman',15,'bold'),width=24)
    channelEntry.grid(row = 0, column=1,padx=15,pady=10)
    
    RegionLabel = Label(update_window,text='Region',font=('time new roman',15,'bold'))
    RegionLabel.grid(row = 1,column=0,padx=30,pady=15,sticky=W)
    RegionEntry = Entry(update_window,font=('roman',15,'bold'),width=24)
    RegionEntry.grid(row = 1, column=1,padx=15,pady=10)
    
    FreshLabel = Label(update_window,text='Fresh',font=('time new roman',15,'bold'))
    FreshLabel.grid(row = 2,column=0,padx=30,pady=15,sticky=W)
    FreshEntry = Entry(update_window,font=('roman',15,'bold'),width=24)
    FreshEntry.grid(row = 2, column=1,padx=15,pady=10)
    
    MilkLabel = Label(update_window,text='Milk',font=('time new roman',15,'bold'))
    MilkLabel.grid(row = 3,column=0,padx=30,pady=15,sticky=W)
    MilkEntry = Entry(update_window,font=('roman',15,'bold'),width=24)
    MilkEntry.grid(row = 3, column=1,padx=15,pady=10)
    
    GroceryLabel = Label(update_window,text='Grocery',font=('time new roman',15,'bold'))
    GroceryLabel.grid(row = 4,column=0,padx=30,pady=15,sticky=W)
    GroceryEntry = Entry(update_window,font=('roman',15,'bold'),width=24)
    GroceryEntry.grid(row = 4, column=1,padx=15,pady=10)
    
    FrozenLabel = Label(update_window,text='Frozen',font=('time new roman',15,'bold'))
    FrozenLabel.grid(row = 5,column=0,padx=30,pady=15,sticky=W)
    FrozenEntry = Entry(update_window,font=('roman',15,'bold'),width=24)
    FrozenEntry.grid(row = 5, column=1,padx=15,pady=10)
    
    Detergents_PaperLabel = Label(update_window,text='Detergents_PaperLabel',font=('time new roman',15,'bold'))
    Detergents_PaperLabel.grid(row = 6,column=0,padx=30,pady=15,sticky=W)
    Detergents_PaperEntry = Entry(update_window,font=('roman',15,'bold'),width=24)
    Detergents_PaperEntry.grid(row = 6, column=1,padx=15,pady=10)
    
    DelicassenLabel = Label(update_window,text='Delicassen',font=('time new roman',15,'bold'))
    DelicassenLabel.grid(row = 7,column=0,padx=30,pady=15,sticky=W)
    DelicassenEntry = Entry(update_window,font=('roman',15,'bold'),width=24)
    DelicassenEntry.grid(row = 7, column=1,padx=15,pady=10)
    
    update_element_button =ttk.Button(update_window,text='UPDATE ELEMENT',command=update_data)
    update_element_button.grid(row=8,columnspan=2,pady=15)

    indexing = Element_table.focus()
    content = Element_table.item(indexing)
    listdata = content['values']
    channelEntry.insert(0,listdata[0])
    RegionEntry.insert(0,listdata[1])
    FreshEntry.insert(0,listdata[2])
    MilkEntry.insert(0,listdata[3])
    GroceryEntry.insert(0,listdata[4])
    FrozenEntry.insert(0,listdata[5])
    Detergents_PaperEntry.insert(0,listdata[6])
    DelicassenEntry.insert(0,listdata[7])


def show_Element():
    query = 'select * from overview'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    Element_table.delete(*Element_table.get_children())
    for data in fetched_data:
        Element_table.insert('',END,values=data)


def delete_Element():
    indexing = Element_table.focus()
    content = Element_table.item(indexing)
    content_Channel = content['values'][0]
    content_Region = content['values'][1]
    content_Fresh = content['values'][2]
    content_Milk = content['values'][3]
    content_Grocery = content['values'][4]
    content_Frozen = content['values'][5]
    content_Detergents_Paper = content['values'][6]
    content_Delicassen = content['values'][7]
    
    query = 'delete from overview where _Channel = (%s) and _Region = (%s) and _Fresh = (%s) and _Milk = (%s) and _Grocery = (%s) and _Frozen = (%s) and _Detergents_Paper =(%s) and _Delicassen = (%s)'
    mycursor.execute(query,(content_Channel,content_Region,content_Fresh,content_Milk,content_Grocery,content_Frozen,content_Detergents_Paper,content_Delicassen))
    con.commit()
    messagebox.showinfo('Deleted',f'Delete Chanel: {content_Channel} and Region: {content_Region} and Fresh: {content_Fresh} and Milk: {content_Milk} and Grocery: {content_Grocery} and Frozen: {content_Frozen} and Detergents Paper: {content_Detergents_Paper} and Delicassen: {content_Delicassen} is Successfully! ')
    query = 'select * from overview'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    Element_table.delete(*Element_table.get_children())
    for data in fetched_data:
        Element_table.insert('',END,values=data)
    

def search_Element():
    def search_data():
        #getchannel = channelEntry.get() non-parameter
        query = 'select * from overview where _Channel = (%s) and _Region = (%s)'
        mycursor.execute(query,(channelEntry.get(),RegionEntry.get()))
        Element_table.delete(*Element_table.get_children())
        fetched_data = mycursor.fetchall()
        for data in fetched_data:
            Element_table.insert('',END,values=data)
            
    search_window = Toplevel()
    search_window.title('Search Element')
    search_window.grab_set()
    search_window.resizable(False,False)
    channelLabel = Label(search_window,text='Channel',font=('time new roman',20,'bold'))
    channelLabel.grid(row = 0,column=0,padx=30,pady=15,sticky=W)
    channelEntry = Entry(search_window,font=('roman',15,'bold'),width=24)
    channelEntry.grid(row = 0, column=1,padx=15,pady=10)
    
    RegionLabel = Label(search_window,text='Region',font=('time new roman',20,'bold'))
    RegionLabel.grid(row = 1,column=0,padx=30,pady=15,sticky=W)
    RegionEntry = Entry(search_window,font=('roman',15,'bold'),width=24)
    RegionEntry.grid(row = 1, column=1,padx=15,pady=10)
    
    search_element_button =ttk.Button(search_window,text='SEARCH ELEMENT',command=search_data)
    search_element_button.grid(row=7,columnspan=2,pady=15)



def add_element():
    def add_data():
        if channelEntry.get() =='' or RegionEntry.get() == '' or FreshEntry.get() == '' or MilkEntry.get() == '' or GroceryEntry.get() == '' or FrozenEntry.get() == '' or Detergents_PaperEntry.get() == '' or DelicassenEntry.get() == '':
            messagebox.showerror('Error','All Fields are required',parent=add_window)
        else:
            query = 'insert into overview values(%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(channelEntry.get(),RegionEntry.get(),FreshEntry.get(),MilkEntry.get(),GroceryEntry.get(),FrozenEntry.get(),Detergents_PaperEntry.get(),DelicassenEntry.get()))
            con.commit()
            result = messagebox.askyesno('Confirm','Data added successfully! Do you want to clean the form?',parent=add_window)
            if(result):
                channelEntry.delete(0,END)
                RegionEntry.delete(0,END)
                FreshEntry.delete(0,END)
                MilkEntry.delete(0,END)
                GroceryEntry.delete(0,END)
                FrozenEntry.delete(0,END)
                Detergents_PaperEntry.delete(0,END)
                DelicassenEntry.delete(0,END)
            else:
                pass    
            query = 'select * from overview'
            mycursor.execute(query)
            fetched_data =mycursor.fetchall()
            Element_table.delete(*Element_table.get_children())
            for data in fetched_data:
                Element_table.insert('',END,values=data)
            
    add_window = Toplevel()
    add_window.title('Add Element')
    add_window.grab_set()
    add_window.resizable(False,False)
    channelLabel = Label(add_window,text='Channel',font=('time new roman',20,'bold'))
    channelLabel.grid(row = 0,column=0,padx=30,pady=15,sticky=W)
    channelEntry = Entry(add_window,font=('roman',15,'bold'),width=24)
    channelEntry.grid(row = 0, column=1,padx=15,pady=10)
    
    RegionLabel = Label(add_window,text='Region',font=('time new roman',20,'bold'))
    RegionLabel.grid(row = 1,column=0,padx=30,pady=15,sticky=W)
    RegionEntry = Entry(add_window,font=('roman',15,'bold'),width=24)
    RegionEntry.grid(row = 1, column=1,padx=15,pady=10)
    
    FreshLabel = Label(add_window,text='Fresh',font=('time new roman',20,'bold'))
    FreshLabel.grid(row = 2,column=0,padx=30,pady=15,sticky=W)
    FreshEntry = Entry(add_window,font=('roman',15,'bold'),width=24)
    FreshEntry.grid(row = 2, column=1,padx=15,pady=10)
    
    MilkLabel = Label(add_window,text='Milk',font=('time new roman',20,'bold'))
    MilkLabel.grid(row = 3,column=0,padx=30,pady=15,sticky=W)
    MilkEntry = Entry(add_window,font=('roman',15,'bold'),width=24)
    MilkEntry.grid(row = 3, column=1,padx=15,pady=10)
    
    GroceryLabel = Label(add_window,text='Grocery',font=('time new roman',20,'bold'))
    GroceryLabel.grid(row = 4,column=0,padx=30,pady=15,sticky=W)
    GroceryEntry = Entry(add_window,font=('roman',15,'bold'),width=24)
    GroceryEntry.grid(row = 4, column=1,padx=15,pady=10)
    
    FrozenLabel = Label(add_window,text='Frozen',font=('time new roman',20,'bold'))
    FrozenLabel.grid(row = 5,column=0,padx=30,pady=15,sticky=W)
    FrozenEntry = Entry(add_window,font=('roman',15,'bold'),width=24)
    FrozenEntry.grid(row = 5, column=1,padx=15,pady=10)
    
    Detergents_PaperLabel = Label(add_window,text='Detergents_PaperLabel',font=('time new roman',20,'bold'))
    Detergents_PaperLabel.grid(row = 6,column=0,padx=30,pady=15,sticky=W)
    Detergents_PaperEntry = Entry(add_window,font=('roman',15,'bold'),width=24)
    Detergents_PaperEntry.grid(row = 6, column=1,padx=15,pady=10)
    
    DelicassenLabel = Label(add_window,text='Delicassen',font=('time new roman',20,'bold'))
    DelicassenLabel.grid(row = 7,column=0,padx=30,pady=15,sticky=W)
    DelicassenEntry = Entry(add_window,font=('roman',15,'bold'),width=24)
    DelicassenEntry.grid(row = 7, column=1,padx=15,pady=10)
    
    add_element_button =ttk.Button(add_window,text='ADD ELEMENT',command=add_data)
    add_element_button.grid(row=8,columnspan=2,pady=15)

def ConnectionMySQL():
    def connect():
        global mycursor,con
        try:
            con = mysql.connector.connect(host='localhost',user='root',password='123456')
            #con = mysql.connector.connect(host=hostEntry.get(),user=usernameEntry.get(),password=passwordEntry.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error','Invalid Details',parent=connectWindow)
            return
        try:
            query ='create database test1'
            mycursor.execute(query)
            query = 'use test1'
            mycursor.execute(query)
            query='create table overview(_Channel int not null,_Region int not null,_Freshint not null, _Milkint not null,_Grocery int not null,_Frozen int not null, _Detergents_Paper int not null, _Delicassen int not null,)'
            mycursor.execute(query)
        except:
            query='use test1'
            mycursor.execute(query)
        messagebox.showinfo('Success','Database Connection is successful!',parent=connectWindow)
        add_ele_Button.config(state=NORMAL)
        search_ele_Button.config(state=NORMAL)
        update_ele_Button.config(state=NORMAL)
        delete_ele_Button.config(state=NORMAL)
        Show_ele_Button.config(state=NORMAL)
        Analyst_ele_Button.config(state=NORMAL)
        Export_ele_Button.config(state=NORMAL)
        connectWindow.destroy()
        
    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Data base Connection')
    connectWindow.resizable(0,0)
    
    hostnameLavbel = Label(connectWindow,text='Host Name', font=('arial',20,'bold'))
    hostnameLavbel.grid(row=0,column=0,padx=20,)
    
    hostEntry = Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40, pady=20)
    
    usernameLavbel = Label(connectWindow,text='User Name', font=('arial',20,'bold'))
    usernameLavbel.grid(row=1,column=0,padx=20,)
    
    usernameEntry = Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    usernameEntry.grid(row=1,column=1,padx=40, pady=20)
    
    passwordLavbel = Label(connectWindow,text='Password', font=('arial',20,'bold'))
    passwordLavbel.grid(row=2,column=0,padx=20,)
    
    passwordEntry = Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    passwordEntry.grid(row=2,column=1,padx=40, pady=20)
    
    connectButton = ttk.Button(connectWindow,text='Connection',command=connect)
    connectButton.grid(row=3,columnspan=2)
    
class AI:
    def __init__(self,_Channel,_Region,_Fresh,_Milk,_Grocery,_Frozen,_Detergents_Paper,_Delicassen) :
        self.Channel = _Channel
        self.Region = _Region
        self.Fresh =_Fresh
        self.Milk = _Milk
        self.Grocery = _Grocery
        self.Frozen = _Frozen
        self.Detergent_Paper = _Detergents_Paper
        self.Delicassen = _Delicassen
    
    def getChannel(self,_Channel):
        self.Channel = _Channel

    def getRegion(self,_Region):
        self.Region = _Region
    
    def getFresh(self,_Fresh):
        self.Fresh = _Fresh
    
    def getMilk(self,_Milk):
        self.Milk = _Milk
        
    def getGrocery(self,_Grocery):
        self.Grocery = _Grocery
        
    def getFrozen(self,_Frozen):
        self.Frozen = _Frozen
        
    def getDetergents_Paper(self,_Detergents_Paper):
        self.Detergents_Paper = _Detergents_Paper
        
    def getDelicassen(self,_Delicassen):
        self.Delicassen = _Delicassen
       

def read_file(filename):
    with open(filename,'r') as file:
        reader = csv.reader(file)
        connection  = mysql.connector.connect(user='root',password='123456',host='localhost',db='test1')
        cursor = connection.cursor()
        for rows in reader:
            cursor.execute('INSERT INTO overview (_Channel,_Region ,_Fresh,_Milk,_Grocery,_Frozen,_Detergents_Paper,_Delicassen) VALUES(%s,%s,%s,%s,%s,%s,%s.%s)',rows)
        connection.commit()
    cursor.close()
    connection.close()
    print('Successfully!')


root = ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('radiance')

root.title('Hierarchical Clustering: By LA HOANG PHUC HUIT')
root.geometry("1174x680")


datetimeLabel = Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()

s = 'Hierarchical Clustering'

sliderLabel = Label(root,font=('arial',28, 'italic bold'),width=20)
sliderLabel.place(x=200,y=0)
slider()
connectButton = ttk.Button(root,text='Connect DataBase',command=ConnectionMySQL)
connectButton.place(x=980,y=0)

leftFrame =Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image = PhotoImage(file='analyst.png')
logo_Label = Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)

add_ele_Button = ttk.Button(leftFrame,text='Add Element',width=25, state=DISABLED,command=add_element)
add_ele_Button.grid(row=1,column=0,pady=20)

search_ele_Button = ttk.Button(leftFrame,text='Search Element',width=25, state=DISABLED,command=search_Element)
search_ele_Button.grid(row=2,column=0,pady=20)

delete_ele_Button = ttk.Button(leftFrame,text='Delete Element',width=25, state=DISABLED,command=delete_Element)
delete_ele_Button.grid(row=3,column=0,pady=20)

update_ele_Button = ttk.Button(leftFrame,text='Update Element',width=25, state=DISABLED, command=update_Element)
update_ele_Button.grid(row=4,column=0,pady=20)

Show_ele_Button = ttk.Button(leftFrame,text='Show List Element',width=25, state=DISABLED,command=show_Element)
Show_ele_Button.grid(row=5,column=0,pady=20)

Export_ele_Button = ttk.Button(leftFrame,text='Export Data',width=25, state=DISABLED, command=export_data)
Export_ele_Button.grid(row=6,column=0,pady=20)

Analyst_ele_Button = ttk.Button(leftFrame,text='Analyst',width=25, state=DISABLED, command=Analyst_data)
Analyst_ele_Button.grid(row=7,column=0,pady=20)




rightFrame =Frame(root)
rightFrame.place(x=350,y=80,width=820,height=600)

scrollBarX = Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame,orient=VERTICAL)


column = ('Channel','Region','Fresh','Milk','Grocery','Frozen','Detergents_Paper','Delicassen')

Element_table = ttk.Treeview(rightFrame,columns=(column),xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=Element_table.xview)
scrollBarY.config(command=Element_table.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

Element_table.pack(fill=BOTH,expand=1)
Element_table.config(show='headings')
for col in column:
    Element_table.heading(col,text=col,anchor=CENTER)
Element_table.column('Channel',width=130,anchor=CENTER)
Element_table.column('Region',width=130,anchor=CENTER)    
Element_table.column('Fresh',width=130,anchor=CENTER)
Element_table.column('Milk',width=130,anchor=CENTER)  
Element_table.column('Grocery',width=130,anchor=CENTER)
Element_table.column('Frozen',width=130,anchor=CENTER)  
Element_table.column('Detergents_Paper',width=200,anchor=CENTER)
Element_table.column('Delicassen',width=130,anchor=CENTER)  


style = ttk.Style()
style.configure('Treeview',rowheight=25,font=('arial',10,'bold'))

root.mainloop()


        