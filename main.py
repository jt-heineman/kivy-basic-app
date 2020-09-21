from kivy.app import App
from kivy.lang import Builder #how to connect with kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import *
import random

Builder.load_file('design.kv')

#needs to crate classes with same names of kv file
class LoginScreen(Screen): # need to inherit from a screen object
    def sign_up(self):
        #print("Button pressed")
        self.manager.current = "sign_up_screen"
        #self inherited from Screen, manager is a property
        #current is an attribute, will get the name of the screen to swith to

    def login(self, uname, pword):
        with open('users.json') as file:
            users = json.load(file)
            if uname in users and users[uname]['password']==pword:
                self.manager.current = "login_screen_success"
            else:
                self.ids.login_wrong.text = "Wrong username or password"

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        print(uname, pword)
        with open('users.json') as file:
            users = json.load(file) #dictionary format, user name is the key
        
        users[uname]={'username': uname, 'password': pword
            ,'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        print(users)

        with open('users.json', 'w') as file:
            json.dump(users, file) #overwriting the existing users with the new user

        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt") #function to list all file names
        print(feel)
        print(available_feelings)
        #list comprehension to get file names with no extension
        available_feelings = [Path(filename).stem 
                                for filename in available_feelings]
        print(available_feelings)
        print(f"quotes/{feel}.txt")
        if feel in available_feelings:
            #string manipulation
            with open(f"quotes/{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            print(quotes)
            self.ids.quote.text = random.choice(quotes)
        else:
             self.ids.quote.text = "Try another feeling"

class RootWidget(ScreenManager): #second in hierarchy
    pass

class ImageButton(ButtonBehavior, HoverBehavior, Image): #order in hierarchy
    pass

class MainApp(App): #highest in hierarchy
    def build(self): # build is already a method of App
        return RootWidget() # use bracket to return the object, not the class

#call the MainApp class

if __name__ == "__main__":
    MainApp().run() # create an instance of the main app and then run method
