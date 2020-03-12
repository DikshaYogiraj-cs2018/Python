from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
from db import Database 

db=Database('shop.db')

def populate_list():
    parts.delete(0, END)
    for row in db.fetch():
        parts.insert(END, row)


def add_item():
    if part_text.get() == '' or customer_text.get() == '' or manufacture_text.get() == '' or price_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    db.insert(part_text.get(), customer_text.get(),
              manufacture_text.get(), price_text.get())
    parts.delete(0, END)
    parts.insert(END, (part_text.get(), customer_text.get(),
                            manufacture_text.get(), price_text.get()))
    clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = parts.curselection()[0]
        selected_item = parts.get(index)

        part_entry.delete(0, END)
        part_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        manufacture_entry.delete(0, END)
        manufacture_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate_list()


def update_item():
    db.update(selected_item[0], part_text.get(), customer_text.get(),
              manufacture_text.get(), price_text.get())
    populate_list()


def clear_text():
    part_entry.delete(0, END)
    customer_entry.delete(0, END)
    manufacture_entry.delete(0, END)
    price_entry.delete(0, END)


app=Tk()

#Background Image

load=Image.open("flower.jpg")
render=ImageTk.PhotoImage(load)
img=Label(app,image=render)
img.image=render
img.place(relwidth=1,relheight=1)

#Label

part_text = StringVar()
part_label = Label(app, text='Component', font=('Times New Roman', 16), pady=20)
part_label.grid(row=0, column=0, sticky=E)

customer_text = StringVar()
customer_label = Label(app, text='Customer', font=('Times New Roman', 16))
customer_label.grid(row=0, column=2)

manufacture_text = StringVar()
manufacture_label = Label(app, text='Manufactured', font=('Times New Roman', 16))
manufacture_label.grid(row=1, column=0)


price_text = StringVar()
price_label = Label(app, text='Price', font=('Times New Roman', 16))
price_label.grid(row=1, column=2)

#Entries

part_entry = Entry(app, textvariable=part_text,font=15)
part_entry.grid(row=0, column=1)

customer_entry = Entry(app, textvariable=customer_text,font=15)
customer_entry.grid(row=0, column=3)

manufacture_entry = Entry(app, textvariable=manufacture_text,font=15)
manufacture_entry.grid(row=1, column=1)

price_entry = Entry(app, textvariable=price_text,font=15)
price_entry.grid(row=1, column=3)

parts = Listbox(app, height=8, width=50, border=2,font=15)
parts.grid(row=2, column=1, columnspan=2, rowspan=4)

#Scrollbar

scrollbar = Scrollbar(app)
scrollbar.grid(row=2, column=2,columnspan=2,rowspan=6)

parts.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=parts.yview)

parts.bind('<<ListboxSelect>>', select_item)

#Button
add_btn = Button(app, text='Add Part', width=10, font=15,command=add_item)
add_btn.grid(row=2, column=3,pady=10)

remove_btn = Button(app, text='Remove', width=10,font=15,command=remove_item)
remove_btn.grid(row=3, column=3,pady=10)

update_btn = Button(app, text='Update', width=10,font=15,command=update_item)
update_btn.grid(row=4, column=3,pady=10)

clear_btn = Button(app, text='Clear All', width=10,font=15,command=clear_text)
clear_btn.grid(row=5, column=3,pady=10)

app.title("Electric Store")
app.geometry('800x350')
app.mainloop()
