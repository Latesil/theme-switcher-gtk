import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Theme Switcher")
        
        self.set_border_width(10)
        self.set_default_size(400, 200)
        
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Theme Switcher"
        self.set_titlebar(header_bar)
        
        self.box = Gtk.Box(spacing=6)
        self.add(self.box)
        
        #change to the grid for filechooser
        self.button1 = Gtk.Button(label="Hello")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.box.pack_start(self.button1, True, True, 0)

        self.button2 = Gtk.Button(label="Goodbye")
        self.button2.connect("clicked", self.on_button2_clicked)
        self.box.pack_start(self.button2, True, True, 0)

        

        button = Gtk.ToggleButton(label="Auto Switch")
        button.connect("toggled", self.on_button_clicked, "1")
        header_bar.pack_start(button)

    def on_button1_clicked(self, widget):
        print("Hello")

    def on_button2_clicked(self, widget):
        print("Goodbye")
                
    def on_button_clicked(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print("Button", name, "was turned", state)
