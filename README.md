`python3 -m venv pygtk`

`source pygtk/bin/activate`

`pip install pycairo`

`pip install PyGObject`

`sudo dnf install gobject-introspection-devel cairo-devel pkg-config python3-devel`

`sudo cp org.theme-switcher.gschema.xml /usr/share/glib-2.0/schemas/`

`sudo glib-compile-schemas /usr/share/glib-2.0/schemas/`
