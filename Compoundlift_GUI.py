from tkinter import * #GUI package
import sqlite3 as sq #For tables and database
import datetime

window = Tk()
window.title("Compound Tracker") 
window.geometry('800x600+0+0')
#window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight())) ##Setting the size of window
header = Label(window, text="Compound Tracker for Weightlifting", font=("arial",30,"bold"), fg="steelblue").pack()

con = sq.connect('Gym.db') #dB browser for sqlite needed
c = con.cursor() #SQLite command, to connect to db so 'execute' method can be called


L1 = Label(window, text = "Compound Lift", font=("arial", 18)).place(x=10,y=100)
L2 = Label(window, text = "Day (dd)", font=("arial",18)).place(x=10,y=150)
L3 = Label(window, text = "Month (mm)", font=("arial",18)).place(x=10,y=200)
L4 = Label(window, text = "Year (yyyy)", font=("arial",18)).place(x=10,y=250)
L5 = Label(window, text = "Max Weight (KG)", font=("arial",18)).place(x=10,y=300)
L6 = Label(window, text = "Reps", font=("arial",18)).place(x=10,y=350)

#Create variables for each list
comp = StringVar(window)#For 1st dd
comp.set('----') #Inital placeholder for field

compdb = StringVar(window)#2nd dropdown list
compdb.set('----')

day = StringVar(window)
month = StringVar(window)
year = StringVar(window)
weight = StringVar(window)
reps = StringVar(window)

#Dictionary for drop down list
compound = {'Bench', 'Squat', 'Deadlift','OVH'}

compd = OptionMenu(window, comp, *compound) #For 1st drop down list 
compd.place(x=220,y=105)

compdbase = OptionMenu(window, compdb, *compound)#For 2nd drop down list
compdbase.place(x=100,y=500)

#Entry for 'input' in GUI
dayT = Entry(window, textvariable=day)
dayT.place(x=220,y=155)

monthT = Entry(window, textvariable=month)
monthT.place(x=220,y=205)

yearT = Entry(window, textvariable=year)
yearT.place(x=220,y=255)

weightT = Entry(window, textvariable=weight)
weightT.place(x=220,y=305)

repT = Entry(window, textvariable=reps)
repT.place(x=220,y=355)

#get func to isolate the text entered in the entry boxes and submit to database
def get():
        print("You have submitted a record")
        
        c.execute('CREATE TABLE IF NOT EXISTS ' +comp.get()+ ' (Datestamp TEXT, MaxWeight INTEGER, Reps INTEGER)') #SQL syntax
        
        date = datetime.date(int(year.get()),int(month.get()), int(day.get())) #Date in format from 'import datetime'

        c.execute('INSERT INTO ' +comp.get()+ ' (Datestamp, MaxWeight, Reps) VALUES (?, ?, ?)',
                  (date, weight.get(), reps.get()))
        con.commit()

#Reset fields after submit
        comp.set('----')
        day.set('')
        month.set('')
        year.set('')
        weight.set('')
        reps.set('')

#Clear boxes when submit button is hit
def clear():
    comp.set('----')
    compdb.set('----')
    day.set('')
    month.set('')
    year.set('')
    weight.set('')
    reps.set('')
    
def record():
    c.execute('SELECT * FROM ' +compdb.get()) #Select from which ever compund lift is selected

    frame = Frame(window)
    frame.place(x= 400, y = 150)
    
    Lb = Listbox(frame, height = 8, width = 25,font=("arial", 12)) 
    Lb.pack(side = LEFT, fill = Y)
    
    scroll = Scrollbar(frame, orient = VERTICAL)
    scroll.config(command = Lb.yview)
    scroll.pack(side = RIGHT, fill = Y)
    Lb.config(yscrollcommand = scroll.set) 
    

    Lb.insert(0, 'Date, Max Weight, Reps') #first row in listbox
    
    data = c.fetchall()
    
    for row in data:
        Lb.insert(1,row)
        

    L7 = Label(window, text = compdb.get()+ '      ', 
               font=("arial", 16)).place(x=400,y=100)
    L8 = Label(window, text = "They are ordered from most recent", 
               font=("arial", 16)).place(x=400,y=350)
    con.commit()

button_1 = Button(window, text="Submit",command=get)
button_1.place(x=100,y=400)

button_2 = Button(window,text= "Clear",command=clear)
button_2.place(x=10,y=400)

button_3 = Button(window,text="Open DB",command=record)
button_3.place(x=10,y=500)


window.mainloop() #mainloop() -> make sure that window stays open
