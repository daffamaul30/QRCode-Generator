import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository.GdkPixbuf import Pixbuf

import qrcode
from PIL import Image

class Window(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Barcode Generator")
        self.set_default_size(400,600) #set window size
        self.set_icon_from_file('C:\Users\Daffa Maulana\Desktop/frinsa.png')

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        listt = [['ARABICA','www.javafrinsa.com'],['ROBUSTA','www.w3school.com']]
        name_store = Gtk.ListStore(str, str)
        
        self.img = None
    
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        lbl = Gtk.Label('Pilih Jenis Kopi')
        vbox.pack_start(lbl, False, False, 0)

        self.tmbh = Gtk.Button.new_with_label('Tambah Jenis Kopi')
        self.tmbh.set_tooltip_text('klik untuk menambahkan jenis kopi')
        #self.tmbh.connect("clicked", self.on_generate_clicked)
        vbox.pack_start(self.tmbh, False, False, 0)
        
        for ini in listt:
            name_store.append(ini)
        vbox.set_border_width(30)
        name_combo = Gtk.ComboBox.new_with_model(name_store)
        renderer_text = Gtk.CellRendererText()
        name_combo.connect("changed", self.on_name_combo_changed)
        name_combo.pack_start(renderer_text, True)
        name_combo.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(name_combo, False, False, 1)

        self.btn = Gtk.Button.new_with_label('Generate')
        self.btn.set_tooltip_text('klik untuk membuar QR Code')
        self.btn.connect("clicked", self.on_generate_clicked)
        vbox.pack_start(self.btn, False, True, 0)

        self.f = Gtk.Frame()
        vbox.pack_start(self.f, True, True, 0)

        self.btn1 = Gtk.Button.new_with_label('Copy')
        self.btn1.set_tooltip_text('klik untuk menyalin ke clipboard')
        self.btn.connect("clicked", self.copy_image)
        vbox.pack_start(self.btn1, False, True, 0)

        self.direktori = None
        self.btn2 = Gtk.Button.new_with_label('Choose directory')
        self.btn2.set_tooltip_text('klik untuk memilih direktori untuk menyimpan QR code')
        self.btn2.connect("clicked", self.choose_direct)
        vbox.pack_start(self.btn2, False, True, 0)

        self.btn3 = Gtk.Button.new_with_label('Save')
        self.btn3.set_tooltip_text('klik untuk menyimpan ke direktori')
        self.btn3.connect("clicked", self.save_image)
        vbox.pack_start(self.btn3, False, True, 0)

        self.add(vbox)

    def choose_direct(self, widget):
        direct = Gtk.FileChooserDialog("Select a file Hoss", self, Gtk.FileChooserAction.SELECT_FOLDER,
                                        ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Ok", Gtk.ResponseType.OK))
        response = direct.run()
        if response == Gtk.ResponseType.OK:
            self.direktori = direct.get_filename()
            print("Folder Selected : "+self.direktori)
            self.btn2.new_with_label(self.direktori)
        elif response == Gtk.ResponseType.CANCEL:
            print("User did not choose directory")
        direct.destroy()

    def copy_image(self, widget):
        if self.img.get_storage_type() == Gtk.ImageType.PIXBUF:
            self.clipboard.set_image(self.img.get_pixbuf())

    def save_image(self, widget):
        if (self.direktori is not None) and (self.img is not None):
            self.img.save(self.direktori+'/'+self.jenis+'.png')
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "QR Code Tersimpan di "+self.direktori)
            dialog.run()

            dialog.destroy()
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "Direktori Belum Dipilih atau \nQR Code Belum Digenerate !")
            dialog.run()

            dialog.destroy()

    
    def on_name_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.jenis, self.link = model[tree_iter][:2]
            print("Selected: Jenis=%s, Link=%s" % (self.jenis, self.link))

    def on_generate_clicked(self,widget):
        print(self.link)
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )

        self.dat = self.link
        qr.add_data(self.dat)
        qr.make()
        self.img = qr.make_image().convert('RGB')

        newsize = (60,60)
        self.pict1 = Image.open('C:\Users\Daffa Maulana\Desktop/frinsa.png')
        self.pict = self.pict1.resize(newsize)
        #pict.show()

        self.pos = ((self.img.size[0] - self.pict.size[0]) // 2, (self.img.size[1] - self.pict.size[1]) // 2)
        self.img.paste(self.pict, self.pos)
        #img.show()

    def on_button_clicked(self, widget):
        print("Hello World")

win = Window()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()