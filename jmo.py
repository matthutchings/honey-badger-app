from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class SMApp(App):

    def build(self):
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

if __name__ == '__main__':
    SMApp().run()
