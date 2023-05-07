from tkinter import *
import time
from tkinter import ttk, messagebox, filedialog
import pandas
import mysql.connector
from tkinter.ttk import *
import ttkthemes
from tkcalendar import DateEntry

con = mysql.connector.connect(host="localhost", user="root", passwd="")
mycursor = con.cursor()
query = 'use student_attendance'
mycursor.execute(query)


def page_exit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass


def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newList = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newList.append(datalist)
    table = pandas.DataFrame(newList, columns=['Name', 'Enrollment', 'Roll No', 'Subject', 'Status', 'Semester'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully')


def display_students():
    for label in root.grid_slaves(column=0):
        if int(label.grid_info()["row"]) >= 4:
            label.destroy()
    for checkbox in root.grid_slaves(column=1):
        if int(checkbox.grid_info()["row"]) >= 4:
            checkbox.destroy()

    mycursor.execute("SELECT student_name FROM students WHERE division = %s", (div_var.get(),))
    students = mycursor.fetchall()


    global checkbox_vars
    global checkboxes

    checkbox_vars = []
    checkboxes = []

    def on_checkbox_clicked(index):
        print(f"Checkbox {index} clicked")

    for i, student in enumerate(students):
        Label(root, text=student[0]).grid(row=i + 4, column=0)
        checkbox_var = BooleanVar()
        checkbox_vars.append(checkbox_var)
        checkbox = Checkbutton(root, variable=checkbox_var, command=lambda index=i: on_checkbox_clicked(index))
        checkbox.grid(row=i + 4, column=1)
        checkboxes.append(checkbox)
    # Set the global variables for checkbox variables and checkboxes
    checkbox_vars = checkbox_vars
    checkboxes = checkboxes


def top_data(title, command):
    global nameEntry, courseEntry, creditEntry, semEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=0, column=1, pady=15, padx=10)

    courseLabel = Label(screen, text='Course', font=('times new roman', 20, 'bold'))
    courseLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    courseEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    courseEntry.grid(row=1, column=1, pady=15, padx=10)

    if title == 'Add Subject':
        creditLabel = Label(screen, text='Credits', font=('times new roman', 20, 'bold'))
        creditLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
        creditEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
        creditEntry.grid(row=2, column=1, pady=15, padx=10)

    semLabel = Label(screen, text='Semester', font=('times new roman', 20, 'bold'))
    semLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    semEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    semEntry.grid(row=3, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text="Add", command=command)
    student_button.grid(row=4, columnspan=2, pady=15)


def addSubject():
    if nameEntry.get() == '' or courseEntry.get() == '' or creditEntry.get() == '' or semEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are required', parent=screen)
    else:
        try:
            query = 'insert into subject(name, course, credits, semester) values(%s,%s,%s,%s)'
            mycursor.execute(query, (nameEntry.get(), courseEntry.get(), creditEntry.get(), semEntry.get()))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the form?',
                                         parent=screen)
            if result:
                nameEntry.delete(0, END)
                courseEntry.delete(0, END)
                creditEntry.delete(0, END)
                semEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Error occurred\nPlease try again ', parent=screen)
            return


def addDivision():
    if nameEntry.get() == '' or courseEntry.get() == '' or semEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are required', parent=screen)
    else:
        try:
            query = 'insert into division(division, course, semester) values(%s,%s,%s)'
            mycursor.execute(query, (nameEntry.get(), courseEntry.get(), semEntry.get()))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the form?',
                                         parent=screen)
            if result:
                nameEntry.delete(0, END)
                courseEntry.delete(0, END)
                semEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Error occurred\nPlease try again ', parent=screen)
            return


def show():
    query = 'select enrollment, name, roll_no from student where division=%s and semester=%s'
    mycursor.execute(query, (div_var.get(), sem_var.get()))
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)
        print(studentTable)

    print("_____________\n" + studentTable)


attendList = []


def comit():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    enrollment = content['values'][1]  # retrieve the enrollment number
    attendList.insert(enrollment)

    messagebox.showinfo('Deleted', f'Id {enrollment} is deleted successfully')
    query = 'select enrollment, name, roll_no from student where enrollment in {}'.format(tuple(attendList))
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


count = 0
text = ''


def slider():
    global text, count

    if count == len(s):
        # hold the last slide instead of a blank space
        text = s
    else:
        text = text + s[count]

    sliderLabel.config(text=text)
    count += 1

    if count > len(s):
        # wait for some time and then start over
        count = 0
        text = ''
        root.after(2000, slider)
    else:
        # continue sliding
        sliderLabel.after(100, slider)


def clock():
    global date, currentTime
    date = time.strftime('%d/%m/%Y')
    currentTime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currentTime}')
    datetimeLabel.after(1000, clock)


def get_date():
    selected_date = cal.get_date()
    dateEntry.delete(0, END)
    dateEntry.insert(0, selected_date)


root = ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('radiance')

root.geometry('1174x680+0+0')
root.resizable(0, 0)
root.title('Student Management System')

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()
s = 'Attendance Management System'  # s[count]=t when count is 1
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=400, y=0)
slider()

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

take = 'Take Attendance'
TakeButton = ttk.Button(leftFrame, text=take, width=25, state=DISABLED,
                        command=show if take == 'Take Attendance' else comit)
TakeButton.grid(row=0, column=0, pady=15)

mycursor.execute('SELECT DISTINCT division.semester FROM division JOIN student ON division.semester = student.semester '
                 'JOIN subject ON student.semester = subject.semester')
semesters = mycursor.fetchall()
sem = [sem[0] for sem in semesters]

semesterLabel = ttk.Label(leftFrame, text='Semester', width=25)
semesterLabel.grid(row=1, column=0, pady=15)
sem_var = StringVar(root)
sem_cb = ttk.Combobox(root, textvariable=sem_var, values=sem)
sem_cb.set('Select Semester')
sem_cb.place(x=175, y=155)

mycursor.execute(
    'SELECT DISTINCT division.division FROM division JOIN student ON division.division = student.division',
    {'semester': sem_var.get()})
division = mycursor.fetchall()
div = [div[0] for div in division]

mycursor.execute('SELECT DISTINCT name FROM subject', {'semester': sem_var.get()})
subject = mycursor.fetchall()
sub = [sub[0] for sub in subject]

subjectLabel = ttk.Label(leftFrame, text='Subject', width=25)
subjectLabel.grid(row=3, column=0, pady=15)
sub_var = StringVar(root)
sub_cb = ttk.Combobox(root, textvariable=sub_var, values=sub)
sub_cb.set('Select Subject')
sub_cb.place(x=175, y=215)

lftFrame = Frame(root)
lftFrame.pack(side=LEFT)

dateLabel = ttk.Label(leftFrame, text='Date', width=25)
dateLabel.grid(row=4, column=0, pady=15)
dateEntry = Entry(leftFrame, width=20)
dateEntry.place(x=125, y=180)
cal = DateEntry(leftFrame, background='darkblue', foreground='white', borderwidth=2)
cal.grid(row=5, column=0, pady=15)
dateButton = ttk.Button(leftFrame, text='Select Date', width=5, command=get_date)
dateButton.place(x=175, y=225)

divisionLabel = ttk.Label(leftFrame, text='Division', width=25)
divisionLabel.grid(row=6, column=0, pady=15)
div_var = StringVar()
div_cb = ttk.Combobox(root, textvariable=div_var, values=div)
div_cb.set('Select Division')
div_cb.place(x=175, y=365)

graphButton = ttk.Button(leftFrame, text='Get Graph', width=25)
graphButton.grid(row=7, column=0, pady=15)

addButton = ttk.Button(leftFrame, text='Add Subject', width=25, command=lambda: top_data('Add Subject', addSubject))
addButton.grid(row=8, column=0, pady=15)

adddivButton = ttk.Button(leftFrame, text='Add Division', width=25,
                          command=lambda: top_data('Add Division', addDivision))
adddivButton.grid(row=9, column=0, pady=15)

exportstudentButton = ttk.Button(leftFrame, text='Export data', width=25, command=export_data)
exportstudentButton.grid(row=10, column=0, pady=15)

exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=page_exit)
exitButton.grid(row=11, column=0, pady=15)

if sem_var != '' and sub_var != '' and dateEntry != '' and div_var != '':
    TakeButton.config(state=NORMAL)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Enrollment No', 'Name', 'Roll No', 'Present'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(expand=1, fill=BOTH)

studentTable.heading('Enrollment No', text='Enrollment No')
studentTable.heading('Name', text='Name')
studentTable.heading('Roll No', text='Roll No')

studentTable.column('Enrollment No', width=200, anchor=CENTER)
studentTable.column('Name', width=150, anchor=CENTER)
studentTable.column('Roll No', width=50, anchor=CENTER)

style = ttk.Style()

style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), fieldbackground='white', background='white', )
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')
studentTable.config(show='headings')

root.mainloop()
