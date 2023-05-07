# from tkinter import *
# from tkinter import ttk
# from tkcalendar import DateEntry
#
# def get_date():
#     selected_date = cal.get_date()
#     date_entry.delete(0, END)
#     date_entry.insert(0, selected_date)
#
# root = Tk()
#
# leftFrame = Frame(root)
# leftFrame.pack(side=LEFT, padx=20, pady=20)
#
# date_label = ttk.Label(leftFrame, text='Date:')
# date_label.grid(row=1, column=0, padx=5, pady=5)
#
# date_entry = ttk.Entry(leftFrame, width=20)
# date_entry.grid(row=1, column=1, padx=5, pady=5)
#
# cal = DateEntry(leftFrame, width=12, background='darkblue',
#                 foreground='white', borderwidth=2)
# cal.grid(row=2, column=0, padx=5, pady=5)
#
# dateButton = ttk.Button(leftFrame, text='Select Date', width=25,
#                         command=get_date)
# dateButton.grid(row=2, column=1, padx=5, pady=5)
#
# root.mainloop()
