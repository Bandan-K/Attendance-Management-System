from tkinter import *
import time
from tkinter import ttk, messagebox, filedialog
import pandas
import mysql.connector
from tkinter.ttk import *
import ttkthemes


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

    table = pandas.DataFrame(newList,
                             columns=['Name', 'Enrollment', 'Roll No', 'Division', 'Semester', 'Email',
                                      'Mobile'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully')


def toplevel_data(title, button_text, command):
    global nameEntry, enrollEntry, rollEntry, divEntry, semEntry, emailEntry, mobileEntry, screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=0, column=1, pady=15, padx=10)

    enrollLabel = Label(screen, text='Enrollment', font=('times new roman', 20, 'bold'))
    enrollLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    enrollEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    enrollEntry.grid(row=1, column=1, pady=15, padx=10)

    rollLabel = Label(screen, text='Roll No', font=('times new roman', 20, 'bold'))
    rollLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    rollEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    rollEntry.grid(row=2, column=1, pady=15, padx=10)

    divLabel = Label(screen, text='Division', font=('times new roman', 20, 'bold'))
    divLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    divEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    divEntry.grid(row=3, column=1, pady=15, padx=10)

    semLabel = Label(screen, text='Semester', font=('times new roman', 20, 'bold'))
    semLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    semEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    semEntry.grid(row=4, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=5, column=1, pady=15, padx=10)

    mobileLabel = Label(screen, text='Mobile', font=('times new roman', 20, 'bold'))
    mobileLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    mobileEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    mobileEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)
    if title == 'Update Student':
        indexing = studentTable.focus()

        content = studentTable.item(indexing)
        listdata = content['values']
        nameEntry.insert(0, listdata[0])
        enrollEntry.insert(0, listdata[1])
        rollEntry.insert(0, listdata[2])
        divEntry.insert(0, listdata[3])
        semEntry.insert(0, listdata[4])
        emailEntry.insert(0, listdata[5])
        mobileEntry.insert(0, listdata[6])


def update_data():
    query = 'update student set name=%s,enrollment=%s,roll_no=%s,division=%s,semester=%s,email=%s,mobile=%s,date=%s,' \
            'time=%s where enrollment=%s'
    mycursor.execute(query, (nameEntry.get(), enrollEntry.get(), rollEntry.get(), divEntry.get(), semEntry.get(),
                             emailEntry.get(), mobileEntry.get(),
                             date, currentTime, enrollEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'Entry of {nameEntry.get()} is modified successfully', parent=screen)
    screen.destroy()
    show_student()


def show_student():
    query = 'select name, enrollment, roll_no, division, semester, email, mobile from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def delete_student():
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    enrollment = content['values'][1]  # retrieve the enrollment number
    query = 'DELETE FROM student WHERE enrollment = %s'
    mycursor.execute(query, (enrollment,))  # pass enrollment number as a tuple
    con.commit()

    messagebox.showinfo('Deleted', f'Id {enrollment} is deleted successfully')
    query = 'select name, enrollment, roll_no, division, semester, email, mobile from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def add_data():
    if nameEntry.get() == '' or enrollEntry.get() == '' or rollEntry.get() == '' or divEntry.get() == '' or \
            semEntry.get() == '' or emailEntry.get() == '' or mobileEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are required', parent=screen)


    else:
        try:
            query = 'insert into student(name, enrollment, roll_no, division, semester, email, mobile, date, time) ' \
                    'values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,
                             (nameEntry.get(), enrollEntry.get(), rollEntry.get(), divEntry.get(), semEntry.get(),
                              emailEntry.get(), mobileEntry.get(), date, currentTime))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the form?',
                                         parent=screen)
            if result:
                nameEntry.delete(0, END)
                enrollEntry.delete(0, END)
                rollEntry.delete(0, END)
                divEntry.delete(0, END)
                semEntry.delete(0, END)
                emailEntry.delete(0, END)
                mobileEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Id cannot be repeated', parent=screen)
            return

        query = 'select name, enrollment, roll_no, division, semester, email, mobile from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('', END, values=data)


def connect_database():
    # def connect():
    global mycursor, con
    try:
        con = mysql.connector.connect(host="localhost", user="root", passwd="")
        mycursor = con.cursor()
    except:
        messagebox.showerror('Error', 'Invalid Details', parent=root)
        return

    try:
        query = 'create database student_attendance'
        mycursor.execute(query)
        query = 'use student_attendance'
        mycursor.execute(query)
        query_stud = 'create table student(id int not null primary key auto_increment, name varchar(30), ' \
                     'enrollment varchar(20), roll_no int, division varchar(1), semester int, email varchar(30), ' \
                     'mobile varchar(10), date varchar(50), time varchar(50))'
        mycursor.execute(query_stud)
        query_sub = 'create table subject(id int not null primary key, name varchar(20), course varchar(10),' \
                    'credits int, semester int) '
        mycursor.execute(query_sub)
        query_att = 'create table attendance(id int not null primary key auto_increment, student_id int, ' \
                    'subject_id int,status smallint(1), date varchar(50), time varchar(50))'
        mycursor.execute(query_att)
        query_div = 'create table division(division varchar(5), course varchar(25),semester int)'
        mycursor.execute(query_div)

    except:
        query = 'use student_attendance'
        mycursor.execute(query)
    messagebox.showinfo('Success', 'Database Connection is successful', parent=root)
    addstudentButton.config(state=NORMAL)
    attendanceButton.config(state=NORMAL)
    updatestudentButton.config(state=NORMAL)
    showstudentButton.config(state=NORMAL)
    exportstudentButton.config(state=NORMAL)
    deletestudentButton.config(state=NORMAL)


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


def attend():
    root.destroy()
    import attendance


count = 0
text = ''

root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.resizable(0, 0)
root.title('Student Management System')

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()
s = 'Student Management System'  # s[count]=t when count is 1
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=350, y=0)
slider()

connectButton = ttk.Button(root, text='Connect database', command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='student.png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED,
                              command=lambda: toplevel_data('Add Student', 'Add', add_data))
addstudentButton.grid(row=1, column=0, pady=15)

attendanceButton = ttk.Button(leftFrame, text='Attendance', width=25, state=DISABLED, command=attend)
attendanceButton.grid(row=2, column=0, pady=15)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED, command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=15)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Update Student', 'Update', update_data))
updatestudentButton.grid(row=4, column=0, pady=15)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_student)
showstudentButton.grid(row=5, column=0, pady=15)

exportstudentButton = ttk.Button(leftFrame, text='Export data', width=25, state=DISABLED, command=export_data)
exportstudentButton.grid(row=6, column=0, pady=15)

exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=page_exit)
exitButton.grid(row=7, column=0, pady=15)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Name', 'Enrollment No', 'Roll No', 'Division', 'Semester', 'Email',
                                                 'Mobile'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(expand=1, fill=BOTH)

studentTable.heading('Name', text='Name')
studentTable.heading('Enrollment No', text='Enrollment No')
studentTable.heading('Roll No', text='Roll No')
studentTable.heading('Division', text='Division')
studentTable.heading('Semester', text='Semester')
studentTable.heading('Email', text='Email')
studentTable.heading('Mobile', text='Mobile')

studentTable.column('Name', width=200, anchor=CENTER)
studentTable.column('Enrollment No', width=300, anchor=CENTER)
studentTable.column('Roll No', width=200, anchor=CENTER)
studentTable.column('Division', width=200, anchor=CENTER)
studentTable.column('Semester', width=200, anchor=CENTER)
studentTable.column('Email', width=300, anchor=CENTER)
studentTable.column('Mobile', width=100, anchor=CENTER)

style = ttk.Style()

style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), fieldbackground='white', background='white', )
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')

studentTable.config(show='headings')

root.mainloop()