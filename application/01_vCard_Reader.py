#!/usr/bin/python
#######################################
# Program to read and show a phone book from AVM Fritz!Box XML export
# multiple entries for a phone category e.g. 'mobile' will not shown yet
# written by Hermann12, in Corona short time work
####### forecast ######################
# maybe some features will be implemented in future
# import xml from FritzFon Export
# export to csv and xml
# edit and add new contacts
# written in python 3.8.2 with thonny
#######################################

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter import Menu
from tkinter import filedialog
import xml.etree.ElementTree as ET
# from xml2csv import Vcard_xml2csv
from phonebook import PhoneBook


def _msgBox_error():
    msg.showerror('xml.etree.ElementTree Error','Your selected file cause a "ParseError"!, Select a valid xml file, please. ')

def _quit():
    win.quit()
    win.destroy()
    exit()

def _about_vCard():
    msg.showinfo('Info vCard','This is a prototyp version V0.1 (Corona): \nDate: June 2020 \nHermann12')
    
def fileParse(xml_file):
    # parse selected avm_file from fileDialog  
    while True:
        try:
            global tree, names
            tree = ET.ElementTree(file=xml_file)
            root = tree.getroot()
            print(root)
            no_count.set(len(root[0]))
            names = PhoneBook(tree).address()
            lbox.insert("end", *names[0].values())
            return tree
            break
        except ET.ParseError:
            _msgBox_error()
            print("Oops!  That was no valid XML.  Try another one ...")
            break
        
def select_xml(event):
    e_phone.delete(0,'end')
    e_mobile.delete(0,'end')
    e_business.delete(0,'end')
    e_fax.delete(0,'end')
    
    widget = event.widget
    selection = widget.curselection()
    indName = widget.get(selection[0])
    print(indName)
    print("selktierter Wert: {}".format(indName))
    dict2 = {indName:key for key, indName in names[0].items()} # names dict from phonbook
    print('dict2:', dict2[indName])
    cont_no=str(dict2[indName])
    uid_name.set(cont_no)
    realName.set(indName)
    
    for elm in names[1]:
        if cont_no in elm:
            for key, value in elm.items():
                print(key, value)
                if key == 'home':
                    phone_home.set(value)
                if key == 'mobile':
                    mobile.set(value)
                if key == 'work':
                    business.set(value)
                if key == 'fax':
                    fax.set(value)    
   
def fileDialog():
    # select xml-file exported phone book from Fritz!Box
    avm_file = filedialog.askopenfilename(filetypes = (("XML files","*.xml"),("all","*.*")))
    fileParse(avm_file)
    statustext.set(avm_file) # for status bar Info
    return statustext

# defining the callback function (observer) 
def my_callback(*args): 
    print (("Traced variable {}").format(name_search.get()))
    # realName.set(name_search.get())  #realName
    search_item = name_search.get()
    
    lbox.delete(0, 'end')
    for key, value in names[0].items():
        if search_item in value:
            lbox.insert("end", value)
    
    
def export_csv():  # still buggy 
    files = [('CSV Document', '*.csv'),  
             ('Text Document', '*.txt'), 
             ('All Files', '*.*')] 
    file = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
    con_file = Vcard_xml2csv(tree, file)
    text2save = str(con_file.get(1.0, 'end'))
    file.write(text2save)
    file.closed()
    
  

# Main App
win = tk.Tk()
win.iconbitmap('vCard.ico')
win.title('vCard')
win.geometry('1200x540+300+300')
win.resizable(True, True)

# Creating Menubar
menu_bar = Menu(win)
win.config(menu=menu_bar)


# Add File menu items
file_menu = Menu(menu_bar, tearoff=0)
sub_menu = Menu(file_menu,tearoff=0)

#sub_menu.add_command(label="xml2csv", command=export_csv)

file_menu.add_command(label="Open ...", command=fileDialog)
file_menu.add_cascade(label="Export ...", menu=sub_menu)

file_menu.add_separator()
file_menu.add_command(label="Exit", command=_quit, accelerator="Alt+F4")
menu_bar.add_cascade(label="File", menu=file_menu)


# Add Help Menu items
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About vCard", command=_about_vCard)
menu_bar.add_cascade(label="Help", menu=help_menu)


# Variables of entry

uid_name = tk.StringVar()
no_count = tk.StringVar()
phone_home =tk.StringVar()
mobile = tk.StringVar()
business = tk.StringVar()
fax = tk.StringVar()
name_search = tk.StringVar()
realName = tk.StringVar()

# LabelFrames Search, Phone Book Entry

name_search.trace_add('write', my_callback)

search_frame = ttk.LabelFrame(win, text = "Search")
search_frame.grid(row=0, column=0, padx = 20, pady=20, sticky='ne')
search_frame.columnconfigure(1, weight=1)

e_name_search = tk.Label(search_frame, text="Name: ").grid(row=0, column=0, padx=10, pady=5, sticky='E')
e_name_search = ttk.Entry(search_frame, width = 30, textvariable=name_search)
e_name_search.grid(row=0, column=1, padx=5, pady=5, sticky='W')
e_name_search.focus()


lbox = tk.Listbox(search_frame, width=30, height=6)
lbox.bind("<Double-Button-1>", select_xml) # Double click or
lbox.bind('<Return>', select_xml)          # return key select an item.
scrollbar = tk.Scrollbar(search_frame)
lbox.grid(row=1, column=1, rowspan=3, padx=10, pady=1)
lbox.config(yscrollcommand = scrollbar.set)
scrollbar.grid(row=1, column=2, rowspan=3, padx=1, pady=1, sticky='ns')
scrollbar.config(command=lbox.yview)

tk.Label(search_frame, text="Select and 'return' or 'double click'").grid(row=5, column=1, padx=10, pady=5, sticky='E')



no_contact = tk.Label(search_frame, text="Count: ")
no_contact.grid(row=6, column=0, padx=10, pady=5, sticky='E')
no_contact = ttk.Entry(search_frame, width = 4, textvariable=no_count, state='readonly')
no_contact.grid(row=6, column=1, padx=5, pady=5, sticky='W')



address_frame = ttk.LabelFrame(win, text = "Phone Book Entry")
address_frame.grid(row=0, column=1, padx = 20, pady=20, sticky='nw')

ttk.Label(address_frame, text="Indicated Name: ").grid(row=0, column=0, padx=10, pady=5, sticky='E')
ttk.Label(address_frame, text = "private: ").grid(row=1, column=0, padx=10, pady=5, sticky='E')
ttk.Label(address_frame, text= "mobile: ").grid(row=2, column=0, padx=10, pady=5, sticky='E')
ttk.Label(address_frame, text = "business: ").grid(row=3, column=0,padx=10, pady=5, sticky='E')
ttk.Label(address_frame, text = "fax: ").grid(row=4, column=0, padx=10, pady=5, sticky='E')
ttk.Label(address_frame, text = "uniqueid: ").grid(row=5, column=0, padx=10, pady=5, sticky='E')


e_name = ttk.Entry(address_frame, width = 30, textvariable=realName)
e_name.grid(row=0, column=1, padx=5, pady=5, sticky='WE')
e_phone = ttk.Entry(address_frame, width = 30, textvariable=phone_home)
e_phone.grid(row=1, column=1, padx=5, pady=5, sticky='WE')
e_mobile = ttk.Entry(address_frame, width = 30, textvariable=mobile)
e_mobile.grid(row=2, column=1, padx=5, pady=5,sticky='WE')
e_business = ttk.Entry(address_frame, width = 30, textvariable=business)
e_business.grid(row=3, column=1, padx=5, pady=5,sticky='WE')
e_fax = ttk.Entry(address_frame, width = 30, textvariable=fax)
e_fax.grid(row=4, column=1, padx=5, pady=5,sticky='WE')
e_uniqueid = ttk.Entry(address_frame, width = 4, textvariable=uid_name, state='readonly')
e_uniqueid.grid(row=5, column=1, padx=5, pady=5,sticky='W')


# Program here


# Status Bar at bottom_frame
status_frame = ttk.LabelFrame(win, text = " ")
status_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')


statustext = tk.StringVar()
statustext.set(' ... choose your avm_xml file') # will be changed from file dialoge
status = ttk.Label(status_frame, textvariable=statustext, borderwidth='10', relief=tk.SUNKEN, anchor=tk.W)
status.pack(side=tk.BOTTOM, fill=tk.X)

win.mainloop()




