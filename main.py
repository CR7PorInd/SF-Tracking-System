import datetime
import os
import threading
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import showwarning
from tkinter.filedialog import askdirectory, asksaveasfile
from typing import *
from shutil import copytree, rmtree

dirname = ''
backupDirname = ''
reportFile = None

isReportSent = False


def sendReport():
    global isReportSent
    if reportFile is None or isReportSent:
        return
    reportFile.write(f"""
    Somebody has been caught who deleted your files. Please look into it.
    Day: {datetime.datetime.now().strftime('%A')}
    Date: {datetime.datetime.now().strftime('%d/%m/%Y')}
    Time: {datetime.datetime.now().strftime('%H:%M')}
    \n\n\n
    """)
    reportFile.flush()
    isReportSent = True


def takeBackup():
    try:
        copytree(dirname, os.path.join(backupDirname, os.path.basename(dirname)))
    except FileNotFoundError:
        pass
    except FileExistsError:
        rmtree(os.path.join(backupDirname, os.path.basename(dirname)))
        try:
            copytree(dirname, os.path.join(backupDirname, os.path.basename(dirname)))
        except Exception:
            pass
    except PermissionError:
        pass


def chooseFile():
    global dirname
    dirname = askdirectory(mustexist=True, title='Please choose the directory to check.')
    entry1.configure(state=NORMAL)
    entry1.delete(0, END)
    entry1.insert(0, dirname)
    entry1.configure(state=DISABLED)
    print(dirname)


def chooseBackupFile():
    global backupDirname
    backupDirname = askdirectory(title='Please choose the directory to check.')
    entry3.configure(state=NORMAL)
    entry3.delete(0, END)
    entry3.insert(0, backupDirname)
    entry3.configure(state=DISABLED)
    print(backupDirname)


def chooseReportFile():
    global reportFile
    extensions = [('Text Document', '*.txt')]
    import io
    reportFile = asksaveasfile(
        title='Choose file',
        defaultextension=extensions,
        filetypes=extensions
    )
    entry4.delete(0, END)
    entry4.insert(0, reportFile.name)
    print(reportFile.name)


def fun():
    global isReportSent
    while True:
        try:
            if not os.path.exists(dirname):
                sendReport()
        except FileExistsError:
            isReportSent = False
        except FileNotFoundError:
            pass


thread = threading.Thread(target=fun, daemon=True)
thread.start()

window = Tk()
window.geometry("750x400")
window.title("SF File Tracking System")
window.wm_iconphoto(False, PhotoImage(file='img.png'))

label1 = Label(master=window, text="Choose the path of directory: ")
label1.grid(padx=10, pady=10, row=0, column=0)

entry1 = Entry(master=window)
entry1.config(state=DISABLED)
entry1.grid(padx=10, pady=10, row=0, column=1)

button1 = Button(master=window, text="Choose directory", command=chooseFile)
button1.grid(padx=10, pady=10, row=0, column=2)

label3 = Label(master=window, text="Choose the path of backup directory: ")
label3.grid(padx=10, pady=10, row=1, column=0)

entry3 = Entry(master=window)
entry3.config(state=DISABLED)
entry3.grid(padx=10, pady=10, row=1, column=1)

button2 = Button(master=window, text="Choose backup directory", command=chooseBackupFile)
button2.grid(padx=10, pady=10, row=1, column=2)

button3 = Button(master=window, text="Take Backup", command=takeBackup)
button3.grid(padx=10, pady=10, row=2, column=1)

label4 = Label(master=window, text="Choose report filename: ")
label4.grid(padx=10, pady=10, row=3, column=0)

entry4 = Entry(master=window)
entry4.config()
entry4.grid(padx=10, pady=10, row=3, column=1)

button4 = Button(master=window, text="Choose report filename", command=chooseReportFile)
button4.grid(padx=10, pady=10, row=3, column=2)

window.mainloop()

fun()
