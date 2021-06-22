from tkinter import Label, Entry, Button, DISABLED, StringVar, filedialog, Frame, NORMAL


def enable_bt(bt):
    bt['state'] = NORMAL


def disable_bt(bt):
    bt['state'] = DISABLED


class FileEntry(Frame):
    def __init__(self, master, text: str, command, defval: str) -> None:
        super().__init__(master=master)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        self.rowconfigure(0, weight=0)

        self.command = command
        self.var = StringVar(master=self, value=defval)

        self.lbl = Label(master=self, text=text)
        self.inp = Entry(master=self, textvariable=self.var, state=DISABLED)
        self.btn = Button(master=self, text="Séléctionner",
                          command=self.btn_command)

        self.lbl.grid(row=0, column=0)
        self.inp.grid(row=0, column=1, sticky="EW")
        self.btn.grid(row=0, column=2)

    def btn_command(self):
        self.var.set(self.command())

    @property
    def filename(self):
        return self.var.get()


class OpenFileEntry(FileEntry):
    def __init__(self, master, text, exts, defaultext, defval: str) -> None:
        super().__init__(master, text, self.ofg_name, defval)
        self.exts = exts
        self.defaultext = defaultext

    def ofg_name(self):
        return filedialog.askopenfilename(filetypes=self.exts, defaultextension=self.defaultext)


class SaveFileEntry(FileEntry):
    def __init__(self, master, text, exts, defaultext, defval: str) -> None:
        super().__init__(master, text, self.ofg_save, defval)
        self.exts = exts
        self.defaultext = defaultext

    def ofg_save(self):
        return filedialog.asksaveasfilename(filetypes=self.exts, defaultextension=self.defaultext)
