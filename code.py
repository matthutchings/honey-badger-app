import kivy
kivy.require("1.9.1")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.app import App
from kivy.uix.listview import ListView, ListItemButton
from kivy.base import runTouchApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.scrollview import ScrollView
import os

from connected import Connected


class FirstPage(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass


class Signup(Screen):
    """
    Sign-up screen code
    """
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

    def backpage(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'first'
        self.manager.get_screen('first')

class Login(Screen):
    """
    login screen code
    """
    def do_login(self, loginText, passwordText):
        app = App.get_running_app()

        app.username = loginText
        app.password = passwordText

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""

    def backpage(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'first'
        self.manager.get_screen('first')

    

class Connected(Screen):
    """
    disconnect button
    """
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

class MyScore(Screen):
        def backpage(self):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'connected'
            self.manager.get_screen('connected')

class Store(Screen):
    def backpage(self):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'connected'
            self.manager.get_screen('connected')

class MyTeam(Screen):
    def backpage(self):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'connected'
            self.manager.get_screen('connected')

class Leaderboards(Screen):
      def backpage(self):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'connected'
            self.manager.get_screen('connected')

class RestTeam(Screen):
    def backpage(self):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'connected'
            self.manager.get_screen('connected')

root_widget = Builder.load_string('''
MyScreenManager:
    FirstPage:
    Login:
    Connected:
    Signup:
    MyScore:
    Store:
    MyTeam:
    Leaderboards:
    RestTeam:

<Leaderboards>:
    name: 'leaderboards'
    BoxLayout:
        id: leaderboard_layout
        padding: [10,50,10,50]
        spacing: 50
        orientation: 'vertical'
        Label:
            text: 'look at this list of nerds!'
            font_size: 30
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Back'
                font_size: 25
                on_press: root.backpage()

<MyTeam>:
    name: 'myteam'
    BoxLayout:
        orientation: 'vertical'
        padding: [10,50,10,50]
        Label:
            text: 'look at your team!'
            font_size: 30
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'active'
                font_size: 15
                size_hint: (0.5, 0.1)
                on_press: root.manager.current = 'scrollscreen'
            Button:
                text: 'reserve'
                font_size: 15
                on_press: root.manager.current = 'rest'
                size_hint: (0.5, 0.1)
                orientation: 'vertical'
        Button:
            on_press: app.scroll()
        Button:
            text: 'Back'
            size_hint: (1, 0.001)
            font_size: 25
            on_press: root.backpage()

<RestTeam>:
    name: 'rest'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'look at all available characters'
            font_size: 30
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'active'
                font_size: 15
                on_press: root.manager.current = 'myteam'
                size_hint: (0.5, 0.1)
            Button:
                text: 'reserve'
                font_size: 15
                size_hint: (0.5, 0.1)
        GridLayout:
            rows: 3
            cols: 3
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Back'
                size_hint: (1, 0.001)
                font_size: 25
                on_press: root.backpage()

<Store>:
    name: 'store'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Buy characters!'
            font_size: 30
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Back'
                font_size: 25
                on_press: root.backpage()

<MyScore>:
    name: 'score'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Your current score is '
            font_size: 30
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Back'
                font_size: 25
                on_press: root.backpage()

<FirstPage>:
    name: 'first'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Login or sign-up to use'
            font_size: 30
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'Login'
                font_size: 25
                on_press: root.manager.current = 'login'
            Button:
                text: 'Sign-Up'
                font_size: 25
                on_press: root.manager.current = 'signup'

<Signup>:
    name: 'signup'
    BoxLayout
        id: sign-up_layout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'pick a user name and password'
            font_size: 32

        BoxLayout:
            orientation: 'vertical'

            Label:
                text: 'username'
                font_size: 18
                halign: 'center'
                text_size: root.width-20, 20

            TextInput:
                id: username
                multiline:False
                font_size: 10

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Password'
                halign: 'center'
                font_size: 18
                text_size: root.width-20, 20

            TextInput:
                id: passcode
                multiline:False
                password:True
                font_size: 10

            BoxLayout:
                orientation: 'vertical'
                spacing: 0

                Button:
                    text: 'Sign-Up with this username and password!'
                    font_size: 24

                    on_press: root.manager.current = 'login'


                Button:
                    text: 'Back'
                    font_size: 24

                    on_press: root.backpage()

<Login>:
    name: 'login'
    BoxLayout
        id: login_layout
        orientation: 'vertical'
        padding: [10,50,10,50]
        spacing: 50

        Label:
            text: 'Welcome'
            font_size: 32

        BoxLayout:
            orientation: 'vertical'

            Label:
                text: 'Login'
                font_size: 18
                halign: 'center'
                text_size: root.width-20, 20

            TextInput:
                id: login
                multiline:False
                font_size: 10

        BoxLayout:
            orientation: 'vertical'
            Label:
                text: 'Password'
                halign: 'center'
                font_size: 18
                text_size: root.width-20, 20

            TextInput:
                id: password
                multiline:False
                password:True
                font_size: 10

        BoxLayout:
            orientation: 'vertical'
            spacing: 0

            Button:
                text: 'Login'
                font_size: 24

                on_press: root.do_login(login.text, password.text)

            Button:
                text: 'Back'
                font_size: 24

                on_press: root.backpage()


<Connected>:
    name: 'connected'
    BoxLayout:
        orientation: 'vertical'

        Label:
            text: "Welcome back"
            font_size: 22

        BoxLayout:
            orientation: 'vertical'

            Button:
                text: 'My Team'
                font_size: 18
                on_press: root.manager.current = 'myteam'
            Button:
                text: 'Store'
                font_size: 18
                on_press: root.manager.current = 'store'
            Button:
                text: 'My Score'
                font_size: 18
                on_press: root.manager.current = 'score'
            Button:
                text: 'Leaderboards'
                font_size: 18
                on_press: root.manager.current = 'leaderboards'
        Button:
            text: "Disconnect"
            font_size: 24
            on_press: root.disconnect()

''')


class ScreenManagerApp(App):
    def build(self):
        return root_widget

    def scroll(self):
        
        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(156):
            if i in range(0, 156, 2):
                btn = Button(text=str(i), size_hint_y=None, height=40)
                layout.add_widget(btn)
            else:
                lbl = Label(text=str(i), size_hinty=None, height=40)
                layout.add_widget(lbl)
        root = ScrollView(size_hint=(None, None), size=(400, 400),
            pos_hint={'center_x':.5, 'center_y':.5})
        root.add_widget(layout)
        return root

ScreenManagerApp().run()



