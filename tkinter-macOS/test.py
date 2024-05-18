import main as macos
import tkinter as tk

t = macos.Window(width=370, height=400)
c = macos.Canvas(t, width=1024, height=768)
b = macos.Button(c, text="Button", style='primary')
bn = macos.Button(c, text="Button", style='normal', top=62)
bb = macos.BigButton(c, text="BigButton", left=100)
ch1 = macos.CheckBox(c, "Hello", top=62, left=87)
r1 = macos.RadioButton(c, "Hello", top=62, left=160)
ch2 = macos.CheckBox(c, "Hello", top=62, left=233, command=lambda _: print(666))
r2 = macos.RadioButton(c, "Hello", top=62, left=306, command=lambda _: print(666))
l = macos.List(c, text=["1", "2", "3", "4", "5", "6", "7", "8", "9", "1000"], top=104)
s1 = macos.Switch(c, top=104, left=210)
s2 = macos.Switch(c, top=104, left=256, status=macos.ON)
c.pack(fill='both')

# macos.Dialog(title="DialogTitle", text="DialogText", button="ButtonLabel", image="error").mainloop()
# macos.Notification(title="通知Title", message="通知文字", icon="warning").mainloop()
t.mainloop()
