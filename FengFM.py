import tkinter
import ctypes

root = tkinter.Tk()

root.configure(background='#000000')

root.geometry("1920x1080")

ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
root.tk.call('tk', 'scaling', ScaleFactor / 75)

tkinter.Label(root, text="NameProject 随机点名器", font=("微软雅黑", 70), bg="#000000", fg="#ffffff", pady=260).pack(side=tkinter.TOP)
tkinter.Label(root, text="基于Python、公平公正的随机点名器", font=("微软雅黑", 30), bg="#000000", fg="#ffffff").pack(side=tkinter.TOP)

tkinter.Label(root, text="话说你点开这个干啥？？？这里啥也没有！！！", font=("微软雅黑", 10), bg="#000000", fg="#ffffff").pack(side=tkinter.BOTTOM)

root.mainloop()