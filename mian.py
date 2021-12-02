# Python 3+
import tkinter
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(300, 100)
        self.button = ttk.Button(self, text="Call toplevel!", command=self.Create_Toplevel)
        self.button.pack(side="top")

    def Create_Toplevel(self):

        # THE CLUE
        self.wm_attributes("-disabled", True)

        # Creating the toplevel dialog
        self.toplevel_dialog = tk.Toplevel(self)
        self.toplevel_dialog.minsize(300, 100)

        # Tell the window manager, this is the child widget.
        # Interesting, if you want to let the child window
        # flash if user clicks onto parent
        self.toplevel_dialog.transient(self)



        # This is watching the window manager close button
        # and uses the same callback function as the other buttons
        # (you can use which ever you want, BUT REMEMBER TO ENABLE
        # THE PARENT WINDOW AGAIN)
        self.toplevel_dialog.protocol("WM_DELETE_WINDOW", self.Close_Toplevel)



        # self.toplevel_dialog_label = ttk.Label(self.toplevel_dialog, text='Do you want to enable my parent window again?')
        # self.toplevel_dialog_label.pack(side='top')

        im = Image.open(r"C:\Users\xudaz\Desktop\QR.png")
        im = im.resize((350, 350))
        img_png = ImageTk.PhotoImage(im)
        # label_img = tkinter.Label(root, image=img_png)

        self.toplevel_dialog_label = tkinter.Label(self.toplevel_dialog, image=img_png)
        self.toplevel_dialog_label.pack(side='top')

        self.toplevel_dialog_yes_button = ttk.Button(self.toplevel_dialog, text='Yes', command=self.Close_Toplevel)
        self.toplevel_dialog_yes_button.pack(side='left', fill='x', expand=True)

        self.toplevel_dialog_no_button = ttk.Button(self.toplevel_dialog, text='No')
        self.toplevel_dialog_no_button.pack(side='right', fill='x', expand=True)

    def Close_Toplevel(self):

        # IMPORTANT!
        self.wm_attributes("-disabled", False) # IMPORTANT!

        self.toplevel_dialog.destroy()

        # Possibly not needed, used to focus parent window again
        self.deiconify()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()