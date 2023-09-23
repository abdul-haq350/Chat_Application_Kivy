from email import message
from socket import socket
import kivy
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import  ScreenManager,Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import  ScreenManager,Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
import sys
import socket_client
from kivymd.app import MDApp
from kivymd.font_definitions import theme_font_styles
from kivymd.theming import ThemeManager
from kivymd.uix.label import MDLabel
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.button import MDFloatingActionButton,MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.color_definitions import colors
from kivymd.color_definitions import theme_colors


Window.size =  (350,600)

kv = """
FloatLayout:
    md_bg_color: 1,1,1,1
    Image:
        source: "logo.jpg"
        pos_hint:{"y": .25}
    MDLabel:
        text: "Epic Chat"
        pos_hint: {"center_x": .5, "center_y": .5}
        halign: "center"
        font_name: "Poppins-SemiBold.ttf"
        font_size: "40sp"
        theme_text_color:"Custom"
        text_color: 60/255,43/255,117/255,1
    FloatLayout:
        size_hint: .85, .08
        pos_hint: {"center_x": .5, "center_y": .38}
        canvas:
            Color:
                rgb:(238/255,238/255,238/255,1)
            RoundedRectangle:
                size:self.size
                pos:self.pos
                radius: [25]
        TextInput:
            id: Ip
            hint_text: "Ip"
            write_tab: False
            focus: True
            size_hint: 1, None
            pos_hint:{"center_x": .5, "center_y": .5}
            height: self.minimum_height
            multiline: False
            cursor_color: 96/255,74/255, 215/255, 1
            cursor_width:"2sp"
            cursor_blink: True
            foreground_color: 96/255,74/255, 215/255, 1
            background_color: 0,0,0,0
            padding: 15
            font_name: "Poppins-Regular.ttf"
            font_size: "18sp"
    FloatLayout:
        size_hint: .85, .08
        pos_hint: {"center_x": .5, "center_y": .28}
        canvas:
            Color:
                rgb:(238/255,238/255,238/255,1)
            RoundedRectangle:
                size:self.size
                pos:self.pos
                radius: [25]
        TextInput:
            id: Port
            hint_text: "Port"
            input_filter: "int"
            write_tab: False
            size_hint: 1, None
            pos_hint:{"center_x": .5, "center_y": .5}
            height: self.minimum_height
            multiline: False
            cursor_color: 96/255,74/255, 215/255, 1
            cursor_width:"2sp"
            cursor_blink: True
            foreground_colro: 96/255,74/255, 215/255, 1
            background_color: 0,0,0,0
            padding: 15
            font_name: "Poppins-Regular.ttf"
            font_size:"18sp"
    FloatLayout:
        size_hint: .85, .08
        pos_hint: {"center_x": .5, "center_y": .18}
        canvas:
            Color:
                rgb:(238/255,238/255,238/255,1)
            RoundedRectangle:
                size:self.size
                pos:self.pos
                radius: [25]
        TextInput:
            id: Username
            hint_text: "Username"
            write_tab: False
            size_hint: 1, None
            pos_hint:{"center_x": .5, "center_y": .5}
            height: self.minimum_height
            multiline: False
            cursor_color: 96/255,74/255, 215/255, 1
            cursor_width:"2sp"
            foreground_colro: 96/255,74/255, 215/255, 1
            background_color: 0,0,0,0
            padding: 15
            font_name: "Poppins-Regular.ttf"
            font_size:"18sp"
    MDFloatingActionButton:
        icon: "arrow-right"
        pos_hint: {'x':.75  ,'y': .01}
        on_release: app.join_button(Ip,Port,Username)
"""
class InfoPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols =1
        self.message = MDLabel(halign="center", valign="middle",
                               font_style=theme_font_styles[7], theme_text_color="Primary")
        self.message.bind(width= self.update_text_width)
        self.add_widget(self.message)
        self.username = ""
        
    def update_name(self,username):
        self.username = username
        
    def update_info(self,message):
        self.message.text = message +'\n'+ " Window Will close automatically"
        
    def update_text_width(self,*_):
        self.message.text_size = (self.message.width*0.9, None)
        
class ScrollabaleLabel(ScrollView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols =1, size_hint_y = None)
        self.add_widget(self.layout)
        
        self.chat_history = MDLabel(
            size_hint_y=None, markup=True, font_style=theme_font_styles[6], theme_text_color="Primary")
        self.scroll_to_point = MDLabel()
        
        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)
        
    def update_chat_history(self, message ):
        self.chat_history.text += '\n' + message
        
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.98, None)
        
        self.scroll_to(self.scroll_to_point)
        
    def update_chat_history_layout(self,_=None):
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width*0.98, None)

class ChatPage(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        self.padding = 10
        
        self.float_layout_theme = FloatLayout()
        self.toggle = ToggleButton(text ="Change Theme", pos_hint={'center_x':0.25,'center_y':.6}, size_hint = (0.5,1))
        self.toggle.bind(on_press = self.theme_change)
        self.float_layout_theme.add_widget(self.toggle)
        self.toggle1 = ToggleButton(text = "Logout", pos_hint={'center_x':0.75,'center_y':.6}, size_hint = (0.5,1))
        self.toggle1.bind(on_press = self.logout)
        self.float_layout_theme.add_widget(self.toggle1)

        #self.float_layout_theme.add_widget(MDLabel(text="Created By: Abdul Haq ",font_size='25sp' , font_name = "Poppins-SemiBold.ttf",halign = "center", pos_hint ={"center_y": .5},theme_text_color = "Custom"))
        self.add_widget(self.float_layout_theme) 
        
        self.history = ScrollabaleLabel(height = Window.size[1]*0.788, size_hint_y = None,)
        self.add_widget(self.history)
        
        self.new_message = MDTextField(size_hint_x=None, multiline=False, pos_hint={'center_x':0,'center_y':1})
        self.new_message.hint_text = "Type your message....."
        self.join = MDIconButton(icon="send", pos_hint={'center_x':0,'center_y':1},user_font_size ="30sp",theme_text_color = "Custom",text_color = (1,170/255,23/255,1))
        self.join.bind(on_press = self.send_message)
        
        bottom_line = GridLayout(cols = 2)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.join)
        self.add_widget(bottom_line)
        
        
        
        Window.bind(on_key_down = self.on_key_down)
        
        Clock.schedule_once(self.focus_text_input, 10)
        socket_client.start_listening(self.incoming_message, show_error)
        self.bind(size=self.adjust_fields)
    
    def theme_change(self, instance):
        if chat_app.theme_cls.theme_style == "Dark":
            chat_app.theme_cls.theme_style = "Light"
        else:
            chat_app.theme_cls.theme_style = "Dark"
        
    def logout(self, *_):
        if chat_app.theme_cls.theme_style == "Dark":
            chat_app.theme_cls.theme_style = "Light"
        message = 'end'
        socket_client.disconnect(message)
        chat_app.screen_manager.current = "Connect"
        
    
    def adjust_fields(self, *_):
        if Window.size[1] * 0.1 <70:
            new_height = Window.size[1] - 135
        else:
            new_height = Window.size[1] * 0.81
        self.history.height = new_height
        if Window.size[0] * 0.2 <160:
            new_width = Window.size[0] - 70
        else:
            new_width = Window.size[0] * 0.91
        
        self.new_message.width = new_width
        
        Clock.schedule_once(self.history.update_chat_history_layout,0.01)
    
    def on_key_down (self,instance, keyboard, keycode, text, modifiers):
        if keycode == 40:
            self.send_message(None)
        
    def send_message(self, _):
        message = self.new_message.text
        self.new_message.text = ""
        if message:
            self.history.update_chat_history(f"[color=dd2020]{chat_app.info_page.username}[/color]: {message}")
            socket_client.send(message)
            
        
    def focus_text_input(self, _):
        self.new_message.focus = True
        
    def incoming_message (self,username, message):
        self.history.update_chat_history(f"[color=20dd20]{username}[/color]: {message}")
    
    
class EpicApp(MDApp):
    def build(self):
        self.title = "Chat App"
        self.screen_manager = ScreenManager()
        screen = Screen(name = "Connect")
        self.connect_page = Builder.load_string(kv)
        #username = self.connect_page.Username
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)
        
        self.info_page = InfoPage()
        screen = Screen(name="Info")
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager
    
    def create_chat_page(self):
        
        screen = Screen(name = "Chat")
        
        self.chat_page = ChatPage()
        
        screen.add_widget(self.chat_page)
        
        self.screen_manager.add_widget(screen)
    
    def join_button(self,Ip,Port,Username):
        port = int(Port.text)
        ip = Ip.text
        username = Username.text
        
        print(f"attemting to join{ip}: {port} as {username}")
        
        info = f"Attempting to join{ip}: {port} as {username}"
        chat_app.info_page.update_info(info)
        chat_app.info_page.update_name(username)
        
        chat_app.screen_manager.current = "Info"
        if not socket_client.connect(ip, port, username, show_error):
            return
        chat_app.create_chat_page()
        chat_app.screen_manager.current = "Chat"

def show_error(message):
    chat_app.info_page.update_info(message)
    chat_app.screen_manager.current = "Info"
    Clock.schedule_once(sys.exit, 6)

if __name__ == "__main__":
    chat_app = EpicApp()
    chat_app.run()