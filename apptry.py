import kivy
kivy.require("1.9.1")
from kivy.uix.popup import Popup
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
import sqlite3
from kivy.uix.togglebutton import ToggleButton
from connected import Connected
import random
conn = sqlite3.connect('realdata.db')
conn.text_factory = str
curs = conn.cursor()

insertRow = 'INSERT INTO %s SELECT * FROM CharList WHERE Name = (?)'
deleteRow = 'DELETE FROM %s WHERE Name = (?)'


def add(name, table):
    curs.execute(insertRow % table, (name,))
    conn.commit()

def remove(name, table):
    curs.execute(deleteRow % table, (name,))
    conn.commit()
    
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

    def generateTeam(self):
        data1 = []
        data2 = []
        team = []
        curs.execute('SELECT * FROM CharList WHERE Tier = 1')
        for row in curs:
            data1.append([row[0], row[2]])
        nums = random.sample(range(0, len(data1)), 3)
        for num in nums:
            team.append(data1[num])
            add(data1[num][0], 'Team')
        curs.execute('SELECT * FROM CharList WHERE Tier = 2')
        for row in curs:
            data2.append([row[0], row[2]])
        nums = random.sample(range(0, len(data2)), 7)
        for num in nums:
            team.append(data2[num])
            add(data2[num][0], 'Team')

    def generateSubs(self):
        data1 = []
        data2 = []
        subs = []
        curs.execute('SELECT * FROM CharList WHERE Tier = 1')
        for row in curs:
            data1.append([row[0], row[2]])
        nums = random.sample(range(0, len(data1)), 2)
        for num in nums:
            subs.append(data1[num])
            add(data1[num][0], 'Subs')
        curs.execute('SELECT * FROM CharList WHERE Tier = 2')
        for row in curs:
            data2.append([row[0], row[2]])
        nums = random.sample(range(0, len(data2)), 3)
        for num in nums:
            subs.append(data2[num])
            add(data2[num][0], 'Subs')    
        
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

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

class MyScore(Screen):
        def backpage(self):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'connected'
            self.manager.get_screen('connected')
            self.remove_widget(self.lbl)
        def scoreprint(self):
            totalscore = 0
            curs.execute('SELECT * FROM Team')
            for row in curs:
                totalscore += row[2]
            self.lbl = Label(text=str(totalscore), size=(10,10), font_size=(200), size_hint=(0.3,0.3), pos_hint={'center_x': .5, 'center_y': .5})
            self.add_widget(self.lbl)
        
class Store(Screen):

    def backpage(self):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'connected'
            self.manager.get_screen('connected')
            root1.clear_widgets()
            self.remove_widget(root1)
            self.remove_widget(self.lbl1)

    def getLabelText(self):
        curs.execute('SELECT * FROM PlayerData')
        row = curs.fetchall()[0]
        lbltext = row[1]
        self.lbl1 = Label(text='                                                                      Transfers Left: ' + str(lbltext), size_hint=(0.1, 0.1))
        self.add_widget(self.lbl1)

    def generateMarket(self):
        curs.execute('DELETE FROM Roster')
        curs.execute('DELETE FROM Market')
        curs.execute('INSERT INTO Roster SELECT * FROM Team')
        curs.execute('INSERT INTO Roster SELECT * FROM Subs')
        curs.execute('INSERT INTO Market SELECT * FROM CharList WHERE Name NOT IN (SELECT Name FROM Roster)')
    
    def popupfunc(self, event):
        """
        creates a popup asking if the user wishes to swap a character from team to subs
        then proceeds to allow user to choose who swaps
        """


        def subscroll(self):
            """
            opens scroll list of substitute characters in a popup
            """
            for btn in SMApp.marketlist:
                if btn.state == 'down':
                    SMApp.nameOff = btn
                    btn.state = 'normal'

      
            curs.execute('SELECT * FROM Subs')
            layout2 = GridLayout(cols=2, spacing=10, size_hint_y=None)
            layout2.bind(minimum_height=layout2.setter('height'))
            for row in curs:
                btn = ToggleButton(text=str(row[0]), size_hint_y=None, height=40)
                if row[1] == 1:
                    btn.background_color = (0.5, 1, 0.9, 1)
                layout2.add_widget(btn)
                btn.bind(on_press=subChar)
                SMApp.sublist.append(btn)
                lbl = Label(text=str(row[2]), size_hinty=None, height=40)
                layout2.add_widget(lbl)
            root = ScrollView(size_hint=(None, None), size=(400, 400))
            root.add_widget(layout2)
            SMApp.popup2 = Popup(content=root, size=(7, 10), size_hint=(0.55, 0.8), title="list of subs")

            SMApp.popup2.open()

        def DismissPopup1(self):
            popup1.dismiss()
            for btn in SMApp.marketlist:
                if btn.state == 'down':
                    btn.state = 'normal'
        curs.execute('SELECT * FROM PlayerData')
        row = curs.fetchall()[0]
        transfersleft = row[1]
        if transfersleft != 0:
            box = BoxLayout()
            btn1 = Button(text='yeah ok')
            btn2 = Button(text='nope')
            popup1 = Popup(content=box, size=(10, 10), size_hint=(0.3, 0.3), title="swap for a sub?")
            btn2.bind(on_press=DismissPopup1)
            btn1.bind(on_press=subscroll)
            box.add_widget(btn1)
            box.add_widget(btn2)
            popup1.open()
        else:
            popupelse = Popup(title="no transfers left this season!", size=(10,10), size_hint=(0.3,0.3))
            popupelse.open()
            for btn in SMApp.marketlist:
                if btn.state == 'down':
                    btn.state = 'normal'
      
            
        def subChar(self):
            for btn in SMApp.sublist:
                if btn.state == 'down':
                    if btn.background_color == SMApp.nameOff.background_color:
                        SMApp.nameOn = btn.text
                        btn.state = 'normal'
                        add(SMApp.nameOn, 'Market')
                        remove(SMApp.nameOn, 'Subs') 
                        add(SMApp.nameOff.text, 'Subs')
                        remove(SMApp.nameOff.text, 'Market')
                        popup1.dismiss()
                        SMApp.popup2.dismiss()
                        curs.execute('SELECT * FROM PlayerData')
                        row = curs.fetchall()[0]
                        curs.execute('UPDATE PlayerData SET TransfersLeft = (?)', (row[1] - 1,))
                        conn.commit()
                    else:
                        btn.state = 'normal'
                        popupNO = Popup(title='you cannot swap characters of different tiers!', size_hint=(0.3, 0.3))
                        popupNO.open()
                        SMApp.popup2.dismiss()
                        popup1.dismiss()
                    
    def load(self):
        curs.execute('SELECT * FROM Market')
        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for row in curs:
            btn = ToggleButton(text=str(row[0]), size_hint_y=None, height=40)
            btn.bind(on_press=self.popupfunc)
            if row[1] == 1:
                btn.background_color = (0.5, 1, 0.9, 1)
            SMApp.marketlist.append(btn)
            layout.add_widget(btn)
            lbl = Label(text=str(row[2]), size_hinty=None, height=40)
            layout.add_widget(lbl)
        root1.add_widget(layout)
        self.add_widget(root1)

root1 = ScrollView(size_hint=(None, None), size=(400, 400),
        pos_hint={'center_x':.5, 'center_y':.5})



class Team(Screen):
     def backpage(self):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'connected'
            self.manager.get_screen('connected')
            root1.clear_widgets()
            self.remove_widget(root1)
            
     def popupfunc(self, event):
        """
        creates a popup asking if the user wishes to swap a character from team to subs
        then proceeds to allow user to choose who swaps
        """


        def subscroll(self):
            """
            opens scroll list of substitute characters in a popup
            """
            for btn in SMApp.teamlist:
                if btn.state == 'down':
                    SMApp.nameOff = btn
                    btn.state = 'normal'

      
            curs.execute('SELECT * FROM Subs')
            layout2 = GridLayout(cols=2, spacing=10, size_hint_y=None)
            layout2.bind(minimum_height=layout2.setter('height'))
            for row in curs:
                btn = ToggleButton(text=str(row[0]), size_hint_y=None, height=40)
                if row[1] == 1:
                    btn.background_color = (0.5, 1, 0.9, 1)
                layout2.add_widget(btn)
                btn.bind(on_press=subChar)
                SMApp.sublist.append(btn)
                lbl = Label(text=str(row[2]), size_hinty=None, height=40)
                layout2.add_widget(lbl)
            root = ScrollView(size_hint=(None, None), size=(400, 400))
            root.add_widget(layout2)
            SMApp.popup2 = Popup(content=root, size=(7, 10), size_hint=(0.55, 0.8), title="list of subs")

            SMApp.popup2.open()

        def DismissPopup1(self):
            popup1.dismiss()
            for btn in SMApp.teamlist:
                if btn.state == 'down':
                    btn.state = 'normal'
                    
        box = BoxLayout()
        btn1 = Button(text='yeah ok')
        btn2 = Button(text='nope')
        popup1 = Popup(content=box, size=(10, 10), size_hint=(0.3, 0.3), title="substitute from team?")
        btn2.bind(on_press=DismissPopup1)
        btn1.bind(on_press=subscroll)
        box.add_widget(btn1)
        box.add_widget(btn2)
        
        popup1.open()
        
      
            
        def subChar(self):
            for btn in SMApp.sublist:
                if btn.state == 'down':
                    if btn.background_color == SMApp.nameOff.background_color:
                        SMApp.nameOn = btn.text
                        btn.state = 'normal'
                        add(SMApp.nameOn, 'Team')
                        remove(SMApp.nameOn, 'Subs') 
                        add(SMApp.nameOff.text, 'Subs')
                        remove(SMApp.nameOff.text, 'Team')
                        popup1.dismiss()
                        SMApp.popup2.dismiss()
                    else:
                        btn.state = 'normal'
                        popupNO = Popup(title='you cannot swap characters of different tiers!', size_hint=(0.3, 0.3))
                        popupNO.open()
                        SMApp.popup2.dismiss()
                        popup1.dismiss()
                    
     def load(self):
        curs.execute('SELECT * FROM Team')
        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for row in curs:
            btn = ToggleButton(text=str(row[0]), size_hint_y=None, height=40)
            btn.bind(on_press=self.popupfunc)
            if row[1] == 1:
                btn.background_color = (0.5, 1, 0.9, 1)
            SMApp.teamlist.append(btn)
            layout.add_widget(btn)
            lbl = Label(text=str(row[2]), size_hinty=None, height=40)
            layout.add_widget(lbl)
        root1.add_widget(layout)
        self.add_widget(root1)


class Leaderboards(Screen):
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
    Leaderboards:
    Team:

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


<Team>:
    name: 'team'
    on_pre_enter: self.load()
    BoxLayout:
        orientation: 'horizontal'
        Button:
            text: 'back'
            on_press: root.backpage()
            size_hint: (0.1, 0.1)

<Store>:
    name: 'store'
    on_pre_enter:
        self.generateMarket()
        self.load()
        self.getLabelText()
    BoxLayout:
        orientation: 'horizontal'
        Button:
            text: 'Back'
            size_hint: (0.1, 0.1)
            front_size: 25
            on_press: root.backpage()

<MyScore>:
    on_pre_enter:
        self.scoreprint()
    name: 'score'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Your current score is '
            font_size: 30
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Back'
                size_hint: (0.3, 0.3)
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

                    on_press:
                        root.generateTeam()
                        root.generateSubs()
                        root.manager.current = 'login'


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
                on_press: root.manager.current = 'team'
            Button:
                text: 'Store'
                font_size: 18
                on_press:
                    root.manager.current = 'store'
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


class SMApp(App):
    teamlist = []
    sublist = []
    marketlist = []
    nameOff = ""
    nameOn = ""
    popup2 = Popup()
    def build(self):
        return root_widget

SMApp().run()
