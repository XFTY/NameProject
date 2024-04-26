# -*- coding:utf-8 -*-
import subprocess
import tkinter
import ttkbootstrap
import threading
import tkinter.messagebox
import traceback

class startWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.checkTime = 5
        self.usedTime = 0

        self.title("NameProject 启动程序")
        self.attributes("-topmost", True)
        self.style = ttkbootstrap.Style(theme="cosmo")
        tkinter.Label(self, text="NameProject 启动程序", font=("微软雅黑", 20)).pack(side="top")
        self.activiteLabel = tkinter.Label(self, text="请在 {} 秒内点击你需要的启动程序，否则将启动默认程序".format(10), font=("微软雅黑", 15))
        self.activiteLabel.pack(side="top")

        mainButton = tkinter.Button(self, text="启动主程序(默认)", command=self.mainButtonFunc, font=("simhei", 15))
        mainButton.pack(side="top", fill="x", pady=5, ipady=10)

        sittingsButton = tkinter.Button(self, text="启动设置程序", font=("simhei", 15), command=self.sittingsButtonFunc)
        sittingsButton.pack(side="top", fill="x", pady=(5, 0), ipady=10)

        self.gotoWelcomeUI()

        self.center_window()
        self.autoRun()

        self.mainloop()

    def gotoWelcomeUI(self):
        try:
            with open("configure.json", "r", encoding="utf-8") as f: pass
            return
        except FileNotFoundError:
            subprocess.call("venv/Scripts/python.exe source.py", creationflags=subprocess.CREATE_NO_WINDOW)

        except:
            tkinter.messagebox.showerror("错误", traceback.format_exc())

    def autoRun(self):
        self.activiteLabel.configure(
            text="请在 {} 秒内点击你需要的启动程序，否则将启动默认程序".format(self.checkTime - self.usedTime))
        if self.usedTime == self.checkTime:
            self.mainButtonFunc()
        self.usedTime += 1
        self.after(1000, self.autoRun)


    def mainButtonFunc(self):
        self.destroy()
        def open():
            subprocess.call("venv/Scripts/python.exe source.py", creationflags=subprocess.CREATE_NO_WINDOW)

        t = threading.Thread(target=open)
        t.start()

    def sittingsButtonFunc(self):
        self.destroy()
        def open():
            subprocess.call("venv/Scripts/python.exe sittings.py", creationflags = subprocess.CREATE_NO_WINDOW)

        t = threading.Thread(target=open)
        t.start()

    def center_window(self):
        """
        将窗口居中显示在屏幕上。
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 获取窗口尺寸
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        # 计算居中位置坐标
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # 设置窗口位置
        self.geometry(f"+{x}+{y}")

startWindow()

# subprocess.call("venv\Scripts\python.exe source.py", creationflags=subprocess.CREATE_NO_WINDOW)
