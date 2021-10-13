import os
import time
import smtplib
import pyttsx
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import cmd
from PIL import ImageTk, Image
import tkinter.messagebox as messagebox
from tkinter import *
from threading import *
from sys import platform


class Jarvis(cmd.CommandPrompt):

    print("Initializing Jarvis...")

    def __init__(self):
        super().__init__()
        self.engine = pyttsx.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)

    def change_label(self, text):
        listening_label.config(text=text)

        # function to listen in background
    def listen_background(self):
        '''
        Function listens in the background.
        '''
        self.change_label("Listening...")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            try:
                print("Recognizing...")
                self.change_label("Recognizing...")
                query = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("Could not understand audio")
                return "none"
            return query.lower()

    def speak(self, text):
        '''
        This function takes text in form of parameter and speaks
        it out. (Text-to-speech)

        voices[0]- David
        voices[1]- Zira
        '''
        self.engine.say(text)
        self.engine.runAndWait()

    def takeCommand(self):
        '''
        This function listens the voice commands and transforms
        it into text form. (Voice-to-text)

        '''

        jarvisui = JarvisUI()

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            self.change_label("Listening...")
            r.pause_threshold = 1.0
            audio = r.listen(source)

            try:
                print("Recognizing...")
                self.change_label("Recognizing...")
                query = r.recognize_google(audio)
                print(f"User : {query}\n")
                self.change_label(f"User : {query}\n")
            except Exception as e:
                self.speak("Some problem, please say that again.")
                return "none"
            return query.lower()

    def wishMe(self):
        hour = int(datetime.datetime.now().hour)
        text = ""
        if hour >= 0 and hour < 12:
            text = "Good Morning!"
        elif hour >= 12 and hour < 15:
            text = "Good Afternoon!"
        elif hour >= 15 and hour < 20:
            text = "Good Evening!"
        else:
            text = "Hello"
        self.speak(text)
        self.speak("I am Jarvis sir. How may I help you?")

    def youtube(self):
        self.speak('Do you want to search anything in youtube?')
        query = self.takeCommand()
        if 'yes' in query:
            self.speak('What you want to search?')
            query = self.takeCommand()
            result = query.replace(" ", "+")
            webbrowser.open_new_tab(
                f"www.youtube.com/results?search_query={result}")
        else:
            self.speak("Okay, Opening youtube.")
            webbrowser.open_new_tab(f"www.youtube.com")

    def google(self):
        self.speak("Do you want to search on Google? yes/no.")
        query = self.takeCommand()
        if 'yes' in query:
            # searching directly for google images
            self.speak("Do you want to search for an Image? Yes/No")
            image_query = self.takeCommand()
            if 'yes' in image_query:
                self.speak("Which images you want to search?") # say the keyword, example "New York"
                image_query = self.takeCommand()
                image_search = 'https://www.google.com/search?q='+image_query+'&rlz=1C5CHFA_enUS860US860&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjqg__ehr3qAhUZyjgGHbcJDrgQ_AUoAXoECAwQAw&biw=1440&bih=788'
                webbrowser.open_new_tab(image_search)
            else:
                self.speak("what you want to search?")
                query = self.takeCommand()
                result = query.replace(" ", "+")
                webbrowser.open_new_tab(f"www.google.com/search?q={result}")
        else:
            self.speak("Okay, Opening google.")
            webbrowser.open_new_tab("www.google.com")

    def wikipedia(self):
        self.speak('What you want to search in wikipedia?')
        query = self.takeCommand()
        try:
            result = wikipedia.summary(query, sentences=2)
        except wikipedia.exceptions.PageError as e:
            result = str(e)
        self.speak(f"According to Wikipedia {result}")
    
    def open_application(self):
        self.speak('Which application would you like to open?')
        query = self.takeCommand()
        try:
            if platform == "darwin":
                command = 'open -a "{}"'.format(str(query))
            elif platform == "linux" or platform == "linux2":
                command = query
            else: # platform == "win32"
                command = 'start {}'.format(str(query))
            os.system(command)
        except:
            self.speak("I was not able to locate your application. Make sure you are in Desktop")

    def time(self):
        strTime = datetime.datetime.now().strftime("%H:%M")
        if int(strTime.split(":")[0]) < 12:
            strTime = strTime + "am"
        else:
            strTime = strTime + "pm"
        self.speak(f"Current time is {strTime}")

    def date(self):
        strdate = datetime.datetime.now()
        month = ['january', 'february', 'march', 'april', 'may', 'june',
                 'july', 'august', 'september', 'october', 'november', 'december']
        postfix = ''
        date = ''
        if strdate.day % 10 == 1 and strdate.day != 11:
            postfix = 'st'
        elif strdate.day % 10 == 2 and strdate.day != 12:
            postfix = 'nd'
        elif strdate.day % 10 == 3 and strdate.day != 13:
            postfix = 'rd'
        else:
            postfix = 'th'

        date = str(strdate.day) + postfix + ' ' + \
            month[int(strdate.month)-1] + ' ' + str(strdate.year)

        self.speak(f"Today's date is {date}")

    def actions(self):
        query = self.takeCommand()
        if 'wikipedia' in query:
            self.wikipedia()
            return
        elif 'open youtube' in query:
            self.youtube()
            return
        elif ('google' or 'search') in query:
            self.google()
            return
        elif 'time' in query:
            self.time()
        elif 'date' in query:
            self.date()
        elif ('visual studio code'or'open code') in query:
            path = "C:\\Users\\Divyanshu Shekhar\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(path)
            return
        elif 'current directory' in query:
            (disk, directory) = self.cwd()
            self.speak(
                f"The current working directory is, {directory}, in disk, {disk}.")
        elif 'open application' in query:
            self.open_application()
        else:
            self.speak("Bye sir, Take care.")
            return

    def activate(self):
        self.wishMe()
        self.actions()


class JarvisUI(Jarvis):

    trigger = 'jarvis'

    def __init__(self):
        super().__init__()

    def about(self):
        messagebox.showinfo('ABOUT', 'Developed by Divyanshu Shekhar')

    def version(self):
        messagebox.showinfo('VERSION', 'Jarvis 1.0.0')

    def cmd_menu(self):
        messagebox.showinfo('Commands', '''
            Commands performed by Jarvis
            ----------------------------------------

        1. Make Google/Youtube/Wikipedia Search
        2. Current Time/Remainder/Notes
        3. Open Visual Studio Code
        4. AutoGit
        5. Run Cmd
        6. Open Applications
        7. Search for Images
        ''')

    def menubar(self):
        # MenuBar
        menubar = Menu(root)
        root.config(menu=menubar)

        # SubMenus
        submenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=submenu)
        submenu.add_command(label="Save")
        submenu.add_command(label="Reset")
        submenu.add_command(label="Exit", command=root.destroy)

        submenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=submenu)
        submenu.add_command(label="Commands", command=self.cmd_menu)
        submenu.add_command(label="Version", command=self.version)
        submenu.add_command(label="About", command=self.about)

    def statusbar(self):
        # Status Bar
        statusbar = Label(root, text="Developed by Divyanshu Shekhar.", bd=1, font=('Futura', 10),
                          relief=SUNKEN, anchor=W)
        statusbar.pack(side=BOTTOM, fill=X)

    def activate_UI(self):
        while True:
            query = self.listen_background()
            if JarvisUI.trigger in query:
                t1 = Thread(target=self.activate)
                t1.start()
                break


jarvisui = JarvisUI()

root = Tk()
root.title("Jarvis")
root.geometry('800x500')
# root.configure(background='black')
root.resizable(width=True, height=True)
root.iconbitmap("./img/jarvis-ark.ico")

''' Menu Bar '''

jarvisui.menubar()

''' Top Label '''

top_label = Label(root, text="A Voice Assistant :- Jarvis",
                  font=('Futura', 20))
top_label.pack(padx=10, pady=10)

''' Button '''

activate_btn = Button(root, text='Activate Jarvis', font=('Futura', 20),
                      command=jarvisui.activate_UI, padx=10, pady=10, relief=RIDGE)
activate_btn.pack(padx=10, pady=10,)

''' LRU Label '''

listening_label = Label(root, text="", font=('Futura', 20))
listening_label.pack(padx=10, pady=10)

''' Status Bar '''

jarvisui.statusbar()

root.mainloop()
