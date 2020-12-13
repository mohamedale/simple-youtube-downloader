"""
    Important Notices:-
    * Download all modules that we used before run this code
    * We need module (youtube_dl) so you must download it
    * This is my first project with python so maybe bugs exists
    * Cannot download more than one video in same time
    * This is the first version of this app so in the next all bugs will be fix and will be add useful features
    * This code not follow the best practices because it's first coding with python
    * This code will be in (oop) in the future
    * The file that downloaded will locate in the same path of this program
    * if you need to ask any question you can contact me
    Author Info:-
    Name: Mohamed Ali
    Mail: mohamed.abogabal.050@gmail.com
    Program Info:-
    Name: Youtube Simple Downloader
    Version: 1.0
    Released Date: 13-12-2020
"""

import os
from functools import partial
from random import random
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
from pafy import new
import re

# download progress dialog variable {will reset}
dnProgressDialog = None
dnLabelProcess = None
dnProgress = None
dnProcess = None


# show available qualities
def avQualities():
    # get media info
    try:
        # start fetching data
        result = new(linkEntry.get())
        # create parent dialog
        avQuaDialog = Toplevel(ytApp)
        # change title
        avQuaDialog.title('Choose Your Quality')
        # disable resizable
        avQuaDialog.resizable(False, False)
        # print the result
        Label(avQuaDialog, text="Download your favourite quality", font=('Arial', 15)).pack(pady=5, padx=40)
        Label(avQuaDialog, text="-" * 50).pack()
        Label(avQuaDialog, text=f"Title: {result.title}", font=('Arial', 13)).pack(pady=10)
        Label(avQuaDialog, text="-" * 50).pack()
        Label(avQuaDialog, text=f"Download Path: {os.getcwd()}", font=('Arial', 13)).pack(pady=10)
        Label(avQuaDialog, text="-" * 50).pack()
        for s in result.streams:
            quality = re.search(r"(x)([0-9]+)", str(s)).groups()[1]
            Label(avQuaDialog,
                  text=f"Quality: {quality}p, Size: {format(s.get_filesize() / 1024 / 1024, '.1f')}MB",
                  font=('Arial', 12)).pack()
            Button(avQuaDialog,
                   text="Download",
                   bg='#6ab04c',
                   fg='#fff',
                   font=('Arial', 12),
                   borderwidth=0,
                   command=partial(dnStream, s)).pack(pady=5)

    except ValueError as err:
        # show error message
        messagebox.showerror("Invalid Video Url", str(err).split('.')[0])  # get part of the exception
    except OSError as err:
        # show error message
        messagebox.showerror("Invalid Video Url", str(err))


# download stream
def dnStream(stream):
    # to use the global variables
    global dnProgressDialog, dnLabelProcess, dnProgress, dnProcess
    # create download dialog to show downloading details
    dnProgressDialog = Toplevel(height=300, width=450)
    # create some labels to show write details with it
    dnLabelProcess = Label(dnProgressDialog,
                           text="Downloading process Details",
                           font=('Arial', 13))
    dnLabelProcess.pack(pady=10)
    dnProgress = Progressbar(dnProgressDialog,
                             orient=HORIZONTAL,
                             length=400,
                             mode="determinate")
    dnProgress.pack(pady=20, padx=15)
    # start downloading process
    dnProcess = stream.download(
        filepath=f"{stream.title}-{int(random() * 100000)}.{stream.extension}",
        quiet=True,
        callback=dnProgressbarFn)


# download progress bar
def dnProgressbarFn(total, received, ratio, rate, eta):
    details = f"Total: {format(total / 1024 / 1024, '.1f')}MB \n" \
              f"Received: {format(received / 1024 / 1024, '.1f')}MB \n" \
              f"Download speed: {int(rate)}KB/S \n" \
              f"Time left: {eta}s, \n" \
              f"Ratio downloading: {format(ratio * 100, '.2f')}%"

    try:
        dnLabelProcess.config(text=details)
        dnLabelProcess.update()
        dnProgress.config(value=int(ratio * 100))
        dnProgress.update()

        if int(ratio * 100) == 100:
            messagebox.showinfo("Download Completed", f"The file was downloaded at this directory: {os.getcwd()}.")
            dnProgressDialog.destroy()
    except:  # will repair this exception in the next versions
        pass


# start create a new app
ytApp = Tk()
# change title
ytApp.title('Youtube Downloader, v1.0')
# change dimension
ytApp.geometry('500x150')
# disable resize
ytApp.resizable(False, False)
# create label
appTitleLabel = Label(ytApp, text='Put Your Link Here', font=('Arial', 13))
appTitleLabel.pack(pady=20)
# create entry input
linkVar = StringVar()
linkEntry = Entry(ytApp, textvariable=linkVar, width=50)
linkEntry.pack()
# create a button of the fetching
fetchBtn = Button(ytApp,
                  text='Start Fetching',
                  bg='#6ab04c',
                  fg='#fff',
                  font=('Arial', 12),
                  borderwidth=0,
                  width=13,
                  height=10,
                  command=avQualities)
fetchBtn.pack(pady=17)

# run the app
if __name__ == "__main__":
    ytApp.mainloop()
