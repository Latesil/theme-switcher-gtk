import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.ApplicationWindow):

    def __init__(self):
        Gtk.Window.__init__(self, title="Theme Switcher")
        
        self.set_border_width(10)
        self.set_default_size(400, 200)
        
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Theme Switcher"
        self.set_titlebar(header_bar)
        
        self.box = Gtk.Box(spacing=6)
        self.box.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self.box)
        
        grid_left = Gtk.Grid()
        grid_left.set_column_homogeneous(True)
        grid_left.set_row_homogeneous(True)
        
        label_day = Gtk.Label("File for day:")
        grid_left.add(label_day)
        self.file_button_day = Gtk.Button("Choose Day Wallpaper")
        self.file_button_day.connect("clicked", self.on_day_wallpaper_choose)
        grid_left.attach_next_to(self.file_button_day, label_day, Gtk.PositionType.BOTTOM, 1, 1)
        
        label_night = Gtk.Label("File for night:")
        grid_left.attach_next_to(label_night, self.file_button_day, Gtk.PositionType.BOTTOM, 1, 1)
        self.file_button_night = Gtk.Button("Choose Night Wallpaper")
        self.file_button_night.connect("clicked", self.on_night_wallpaper_choose)
        grid_left.attach_next_to(self.file_button_night, label_night, Gtk.PositionType.BOTTOM, 1, 1)
        
        self.box.pack_start(grid_left, True, True, 0)

        grid_right = Gtk.Grid()
        grid_right.set_column_homogeneous(True)
        grid_right.set_row_homogeneous(True)
        time_label = Gtk.Label("Time Manage:")
        grid_right.add(time_label)
        
        daytime_box = Gtk.Box()
        daytime_box.set_homogeneous(True)
        daytime_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        day_label = Gtk.Label("Daytime: ")
        daytime_box.add(day_label)
        self.day_entry = Gtk.Entry()
        self.day_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.day_entry.set_text("6")
        daytime_box.add(self.day_entry)
        set_daytime_button = Gtk.Button("Set")
        set_daytime_button.connect("clicked", self.on_set_daytime_button_clicked)
        daytime_box.add(set_daytime_button)
        grid_right.attach_next_to(daytime_box, time_label, Gtk.PositionType.BOTTOM, 1, 1)
        
        nighttime_box = Gtk.Box()
        nighttime_box.set_homogeneous(True)
        nighttime_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        night_label = Gtk.Label("Night: ")
        nighttime_box.add(night_label)
        self.night_entry = Gtk.Entry()
        self.night_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.night_entry.set_text("23")
        nighttime_box.add(self.night_entry)
        set_nighttime_button = Gtk.Button("Set")
        set_nighttime_button.connect("clicked", self.on_set_nighttime_button_clicked)
        nighttime_box.add(set_nighttime_button)
        grid_right.attach_next_to(nighttime_box, daytime_box, Gtk.PositionType.BOTTOM, 1, 1)
        
        self.box.pack_start(grid_right, True, True, 0)

        header_box = Gtk.Box(spacing=6)
        header_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        header_bar.pack_start(header_box)
        
        header_label = Gtk.Label("Auto:")
        header_box.add(header_label)
        
        self.auto_button = Gtk.Switch()
        self.auto_button.connect("notify::active", self.on_auto_toggled)
        header_box.add(self.auto_button)
        
        self.init_settings()
        test_button = Gtk.Button(label="Debug")
        test_button.connect("clicked", self.on_test_button_clicked)
        header_bar.pack_end(test_button)
        
    def state_off(self):
        subprocess.call(['systemctl','stop','--user','theme-switcher-auto.timer'])
        subprocess.call(['systemctl','disable','--user','theme-switcher-auto.timer'])
        
    def state_on(self):
        subprocess.call(['systemctl','start','--user','theme-switcher-auto.timer'])
        subprocess.call(['systemctl','enable','--user','theme-switcher-auto.timer'])
        
    def on_day_wallpaper_choose(self, widget):
        dialog = Gtk.FileChooserDialog("Choose a file", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        self.add_filters(dialog)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.day_wallpaper =  dialog.get_filename()
            self.file_button_day.set_label(self.day_wallpaper.split("/")[-1])
                       
        dialog.destroy()
        
    def on_night_wallpaper_choose(self, widget):
        dialog = Gtk.FileChooserDialog("Choose a file", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        
        self.add_filters(dialog)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.night_wallpaper =  dialog.get_filename()
            self.file_button_night.set_label(self.night_wallpaper.split("/")[-1])
            
        dialog.destroy()
            
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("image/jpeg")
        filter_text.add_mime_type("image/png")
        dialog.add_filter(filter_text)
        
    def on_test_button_clicked(self, widget):
        print(self.daytime)
        print(self.nighttime)
        
    def on_set_daytime_button_clicked(self, button):
        entry_text = self.day_entry.get_text()
        try:
            entry_text = int(entry_text)
            if entry_text > 23:
                message_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.CANCEL, "Please enter a correct time")
                message_dialog.format_secondary_text("Please enter a number between 00 and 23.")
                message_dialog.run()

                message_dialog.destroy()
            else:
                self.daytime = entry_text
        except ValueError:
            message_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL, "Please enter a correct number")
            message_dialog.run()

            message_dialog.destroy()
        
    def on_set_nighttime_button_clicked(self, button):
        entry_text = self.night_entry.get_text()
        try:
            entry_text = int(entry_text)
            if entry_text > 23:
                message_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.CANCEL, "Please enter a correct time")
                message_dialog.format_secondary_text("Please enter a number between 00 and 23.")
                message_dialog.run()

                message_dialog.destroy()
            else:
                self.nighttime = entry_text
        except ValueError:
            message_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                Gtk.ButtonsType.CANCEL, "Please enter a correct number")
            message_dialog.run()

            message_dialog.destroy()
                
    def on_auto_toggled(self, auto_button, gparam):
        if self.auto_button.get_active():
            state = "on"
            self.state_on()
        else:
            state = "off"
            self.state_off()
            
    def init_settings(self):
        self.auto_button.set_active(True)
        self.day_wallpaper = ""
        self.night_wallpaper = ""
        state = "on"
        self.daytime = 6
        self.nighttime = 20
