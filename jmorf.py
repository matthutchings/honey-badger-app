from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import sqlite3
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

conn = sqlite3.connect('data.db')
conn.text_factory = str
curs = conn.cursor()

class SMApp(App):
    teamlist = []
    idvar = ""
    btnlist = []
    
    def popupfunc(self, event):
        
        """
        creates a popup asking if the user wishes to swap a character from team to subs
        then proceeds to allow user to choose who swaps
        """
    
        def subscroll(self):
            """
            opens scroll list of substitute characters in a popup
            """
            sublist = []
            curs.execute('SELECT * FROM Subs')
            for row in curs:
                sublist.append([row[0], row[2]])
                
            layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
            layout.bind(minimum_height=layout.setter('height'))
            for i in range(len(sublist)):
                btn = Button(text=str(sublist[i][0]), size_hint_y=None, height=40)
                layout.add_widget(btn)
                lbl = Label(text=str(sublist[i][1]), size_hinty=None, height=40)
                layout.add_widget(lbl)
            root = ScrollView(size_hint=(None, None), size=(400, 400))
            root.add_widget(layout)
            popup2 = Popup(content=root, size=(7, 10), size_hint=(0.55, 0.8), title="list of subs")
            popup2.open()
            
        box = BoxLayout()
        btn1 = Button(text='yeah ok')
        btn2 = Button(text='nope')
        popup1 = Popup(content=box, size=(10, 10), size_hint=(0.3, 0.3), title="add to team?")
        btn2.bind(on_press=popup1.dismiss)
        btn1.bind(on_press=subscroll)
        box.add_widget(btn1)
        box.add_widget(btn2)
        
        popup1.open()

    
    def build(self):
        
        curs.execute('SELECT * FROM Team')
        for row in curs:
            self.teamlist.append([row[0], row[2]])
            
        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(len(self.teamlist)):
            btn = Button(text=str(self.teamlist[i][0]), size_hint_y=None, height=40, id=str(i))
            btn.bind(on_press=self.popupfunc)
            self.btnlist.append(btn)
            layout.add_widget(btn)
            lbl = Label(text=str(self.teamlist[i][1]), size_hinty=None, height=40)
            layout.add_widget(lbl)
        for item in self.btnlist:
            print item.id
        root = ScrollView(size_hint=(None, None), size=(400, 400),
            pos_hint={'center_x':.5, 'center_y':.5})
        root.add_widget(layout)
        return root
    

    
    
if __name__ == '__main__':
    SMApp().run()

