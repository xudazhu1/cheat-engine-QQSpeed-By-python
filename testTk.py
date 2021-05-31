# coding=utf-8
import tkinter

win = tkinter.Tk()
win.title("鼠标光标进入事件")
win.geometry("800x600+600+100")

#<Enter> 鼠标光标进入控件触发事件
#<Leave> 鼠标光标进入控件触发事件


label=tkinter.Label(win,text="red orange yellow green cyan blue "
                             "violet鼠标进入打印",bg="blue")
labe2=tkinter.Label(win,text="red orange yellow green cyan blue "
                             "violet鼠标离开打印",bg="red")
label.pack()
labe2.pack()
def func(event):
    print(event.x,event.y)
label.bind("<Enter>",func)
labe2.bind("<Leave>",func)

win.mainloop()