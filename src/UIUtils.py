import tkinter as Tk

import CarMap as carMap


def _cnfmerge(cnf, defaultConf):
    for k, v in cnf.items():
        defaultConf[k] = cnf[k]


class Instance4ChangeBox:
    def __init__(self, root, configTemp):
        self.config = {
            "x": 1,
            "y": 1,
            "width": 10,
            "readonly": False
        }
        _cnfmerge(configTemp, self.config)
        Tk.Label(root, text="原车ID").place(x=self.config.get("x"), y=self.config.get("y"))
        self.originIdBox = InputBox(root, {"x": self.config.get("x") + 50, "y": self.config.get("y"), "width": 25,
                                           "readonly": self.config.get("readonly")})
        Tk.Label(root, text="  ==> ").place(x=self.config.get("x") + 230, y=self.config.get("y"))
        Tk.Label(root, text="目标车ID").place(x=self.config.get("x") + 270, y=self.config.get("y"))
        self.targetIdBox = InputBox(root, {"x": self.config.get("x") + 330, "y": self.config.get("y"), "width": 25,
                                           "readonly": self.config.get("readonly")})
        if not self.config.get("readonly"):
            selector4Input(root, self.originIdBox)
            selector4Input(root, self.targetIdBox)

    # 获取原车Id 以及目标车id
    def getValues(self):
        originId = self.originIdBox.valBox.get()
        targetId = self.targetIdBox.valBox.get()
        return {"originId": originId, "targetId": targetId}

    # 设置原车Id 以及目标车id
    def setValues(self, conf):
        self.originIdBox.valBox.set(conf.get("originId") if conf.__contains__("originId") else "")
        self.targetIdBox.valBox.set(conf.get("targetId") if conf.__contains__("targetId") else "")


class InputBox:
    def __init__(self, root, configTemp=None):
        self.config = {
            "x": 1,
            "y": 1,
            "width": 10,
            "readonly": False
        }
        _cnfmerge(configTemp, self.config)
        self.valBox = Tk.StringVar()
        self.entry = Tk.Entry(root, bd=6, width=self.config.get("width") or 10, textvariable=self.valBox,
                              state="readonly" if self.config.get("readonly") else "normal")
        self.entry.place(x=self.config.get("x") or 1, y=self.config.get("y") or 1)
        # root.mainloop()
        # sv2.trace("w", lambda name, index, : no_thing())


# 为某个输入框绑定代码搜索框
class selector4Input:

    def __init__(self, root, inputBox):
        self.root = root
        # 待选择车辆列表
        # Tk.Label(root, text="代码搜索").place(x=1, y=35)
        self.test_list = carMap.car_map.keys()
        self.inputBox = inputBox
        # entry = Tk.Entry(root)
        # entry.place(x=1, y=60)
        self.inputBox.entry.bind('<KeyRelease>', self.on_keyrelease)

        self.listbox = Tk.Listbox(root)
        # listbox.place(x=inputBox.config.get("x"), y=inputBox.config.get("y") + 30)
        # listbox.place_forget()
        # listbox.bind('<Double-Button-1>', on_select)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox_update(self.test_list)

        # 创建Scrollbar
        self.y_scrollbar = Tk.Scrollbar(self.listbox, command=self.listbox.yview)
        self.y_scrollbar.place(x=self.inputBox.config.get("width") * 7.5 - 20, y=1, height=180)
        # y_scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
        self.listbox.config(yscrollcommand=self.y_scrollbar.set)

        # 鼠标进入事件 使它获取焦点 然后混动条生效
        self.listbox.bind("<Enter>", lambda x: self.listbox.focus_set())

        self.listbox.bind("<Leave>", lambda x: self.root.focus_set())

        self._is_menuoptions_visible = False
        self.root.bind_all("<1>", self._on_click, "+")
        self.root.bind("<Escape>", lambda event: self.hide_picker())

    def checked(self, value):
        self.inputBox.valBox.set(value)

    def _on_click(self, event):
        str_widget = str(event.widget)
        if str_widget != str(self.inputBox.entry) and str_widget != str(self.listbox)\
                and str_widget != str(self.y_scrollbar):
            self.hide_picker()
        else:
            self.show_picker()

    def show_picker(self):
        if not self._is_menuoptions_visible:
            self.listbox.place(x=self.inputBox.config.get("x"), y=self.inputBox.config.get("y") + 32,
                               width=self.inputBox.config.get("width") * 7.5)
            self.listbox.tkraise()
        self._is_menuoptions_visible = True

    def hide_picker(self):
        if self._is_menuoptions_visible:
            self.listbox.place_forget()
        self._is_menuoptions_visible = False

    def on_keyrelease(self, event):
        # get text from entry
        value = event.widget.get()
        value = value.strip().lower()
        # get data from test_list
        if value == '':
            data = self.test_list
        else:
            data = []
            for item in self.test_list:
                temp = str(item) + '--' + carMap.car_map.get(item)
                if value in temp.lower():
                    data.append(item)
        # update data in listbox
        self.listbox_update(data)

    def listbox_update(self, data):
        # delete previous data
        self.listbox.delete(0, 'end')

        # sorting data
        data = sorted(data, reverse=True)

        # put new data
        for item in data:
            self.listbox.insert('end', str(item) + '--' + carMap.car_map.get(item))

    def on_select(self, event):
        # 找到value一样的 key 设置进输入框
        try:
            selected = event.widget.get(event.widget.curselection())
            self.checked(selected)
        except Tk.TclError:
            print("")
