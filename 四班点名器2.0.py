#! usr/bin/python3
# -*- coding:utf-8 -*-

# ----------------------------------
# 请注意，shi山代码！高血压人群勿看！！！！|
# ----------------------------------

import random
import os
import subprocess
import threading
import time
import tkinter
import tkinter.ttk
import tkinter.messagebox
import ctypes

# """
import webbrowser

students_name = [
    "张三",
    "李四",
    "王五",
    "老六"
]

# 开头展示的话语
an = [
    "不用急，我知道你很急",
    "我有神马值得期待的",
    "全体目光向我看齐！",
    "站后面去！",
    "原神，_____",
    "JNTM",
    "家人们，水桶啊",
    "遥遥领先",
    "泰裤辣",
    "你人还怪好嘞",
    "🚁 -> 24",
    ">>>>>>>>>>",
    "纯爱战神",
    "想你了，劳大！"
]

# 当“停止抽取”按钮触发时的话语
st = [
    "正在减速……",
    "正在刹车……",
    "STOPPING……",
    "原神正在启动……",
    "停下来，停下来！！！"
]


class maingui(tkinter.Tk):
    def __init__(self):
        # 全局继承
        super().__init__()

        # 提高DPI值
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.tk.call('tk', 'scaling', ScaleFactor / 75)

        # 基础变量
        self.preName = "***"
        self.mainName = an[random.randint(0, len(an) - 1)]
        self.afterName = "***"
        self.buttonStatus = False
        self.closeThread = False
        self.f = True  # 判断是否为第一次使用的变量
        self.ifExitAgain = False

        # UI基础设置
        self.title("四班专属点名器 - Professional Edition Version 2.10 [Release]")
        self.width = 2500
        self.height = 1200
        self.x_way = 10
        self.left = (self.winfo_screenwidth() - self.width) / 2 + self.width / 2
        self.top = (self.winfo_screenheight() - self.height) / 2 + self.height / 2
        self.geometry("{}x{}+{}+{}".format(int(self.width), int(self.height), int(self.left), int(self.top)))
        # self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.attributes("-topmost", "true")

        # 屏幕控件
        self.maintitle = tkinter.Label(self, text="点名器   姓名滚动方向 >>>>>>>>", font=("Microsoft Yahei UI", 25))
        self.maintitle.place(x=0, y=0)
        tkinter.Label(self,
                      text="-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",
                      font=("Microsoft Yahei UI", 10)).place(x=0, y=100)

        self.mainNameLabel = tkinter.Label(self, text=self.mainName, font=("Microsoft Yahei UI", 55),
                                           background="#EBDBD1")
        self.mainNameLabel.place(x=self.width / 2, y=self.height / 2, anchor="center")

        self.preNameLabel = tkinter.Label(self, text=self.preName, font=("Microsoft Yahei UI", 40), foreground="gray")
        self.preNameLabel.place(x=self.width - 20, y=self.height / 2, anchor="e")

        self.afterNameLabel = tkinter.Label(self, text=self.afterName, font=("Microsoft Yahei UI", 40),
                                            foreground="gray")
        self.afterNameLabel.place(x=0 + 20, y=self.height / 2, anchor="w")

        self.mainButton = tkinter.Button(self, text="开始抽取", relief=tkinter.GROOVE, width=15, height=2,
                                         command=self.flushUI)
        self.mainButton.place(x=self.width / 2, y=self.height - 80, anchor="e")

        self.mainStopButton = tkinter.Button(self, text="停止抽取", relief=tkinter.GROOVE, width=15, height=2,
                                             state="disabled", command=self.stopRandom)
        self.mainStopButton.place(x=self.width / 2, y=self.height - 80, anchor="w")

        tkinter.Label(self, text="Python project, version 2.10 [Release], Python Version 3.11, TCL/Tk Version 3.x",
                      font=("Microsoft Yahei UI", 9)).pack(side="bottom")

        # tkinter.Label(self,
        #               text="JavaFX Project, Java Version [openJDK17], JavaFX Version [openJFX17], develop by xfypowered.com",
        #               font=("Microsoft Yahei UI", 10)).pack(side="bottom")

        # 由于部分机型无法正确显示窗口内容，故采用此方法
        # self.updateWindow()
        self.updateWindowThread = threading.Thread(target=self.updateWindow, args=())
        self.updateWindowThread.start()

        self.mainloop()

    def updateWindow(self):
        while True:
            if self.winfo_width() != self.width or self.winfo_height() != self.height:
                self.width = self.winfo_width()
                self.height = self.winfo_height()

                self.mainNameLabel.place(x=self.width / 2, y=self.height / 2, anchor="center")
                self.preNameLabel.place(x=self.width - 20, y=self.height / 2, anchor="e")
                self.afterNameLabel.place(x=0 + 20, y=self.height / 2, anchor="w")
                self.mainButton.place(x=self.width / 2, y=self.height - 80, anchor="e")
                self.mainStopButton.place(x=self.width / 2, y=self.height - 80, anchor="w")

                t = threading.Thread(target=self.changeTitle, args=())
                t.start()

    def changeTitle(self):
        self.maintitle.configure(
            text="点名器   姓名滚动方向 >>>>>>>>   窗口变更！Width={}, Height={}".format(self.winfo_width(), self.winfo_height()))
        time.sleep(5)
        self.maintitle.configure(text="点名器   姓名滚动方向 >>>>>>>>")
        # time.sleep(0.01)

        # self.after(10, self.updateWindow)

    #    def changeWindow(self):
    #        while True:
    #            a = self.winfo_width()
    #            b = self.winfo_height()
    #
    #            if self.width != a or self.height != b:
    #                self.width = a
    #                self.height = b

    def __flushUI(self):
        # 打乱姓名列表
        random.shuffle(students_name)
        # 随机停下时间
        x = random.uniform(0.5, 1.0)
        # 姓名滚动时间隔时间
        o = 0.09
        # 随机标题扩充话语
        if self.f:
            stt = st[0]
            self.f = False
        else:
            stt = st[random.randint(0, len(st) - 1)]
        # 进入事件循环，随机抽取名单直到指定事件触发
        while True:
            if self.closeThread:
                self.exit()

            for i in range(1, len(students_name) - 1):
                self.preName = students_name[i - 1]
                self.mainName = students_name[i]
                self.afterName = students_name[i + 1]
                self.preNameLabel.configure(text=self.preName)
                self.mainNameLabel.configure(text=self.mainName)
                self.afterNameLabel.configure(text=self.afterName)
                time.sleep(o)

                if self.buttonStatus:
                    pass
                else:
                    o += 0.05
                    self.maintitle.configure(text="点名器   姓名滚动方向 >>>>>>>>   {}".format(stt))
                    self.mainButton.configure(state="disabled")

                    # 程序随机事件
                    if o > x:
                        if random.randint(0, 20) == 5:
                            self.maintitle.configure(text="点名器   姓名滚动方向 >>>>>>>>   站讲台上的那位！",
                                                     background="#7FFF00",
                                                     foreground="black")
                            self.preNameLabel.configure(text="***")
                            self.mainNameLabel.configure(text="站讲台上的那位！")
                            self.afterNameLabel.configure(text="***")
                            time.sleep(3 * 0.5)
                            self.maintitle.configure(text="点名器   姓名滚动方向 >>>>>>>>   站讲台上的那位！",
                                                     background="#f0f0f0",
                                                     foreground="black")
                            self.mainButton.configure(state="normal")

                        elif random.randint(0, 200) == 4:
                            self.maintitle.configure(text="点名器   姓名滚动方向 >>>>>>>>   原神，启动！",
                                                     background="#7FFF00",
                                                     foreground="black")
                            self.preNameLabel.configure(text="***")
                            self.mainNameLabel.configure(text="原神，启动！！")
                            self.afterNameLabel.configure(text="***")
                            time.sleep(3 * 0.5)
                            self.maintitle.configure(text="点名器   姓名滚动方向 >>>>>>>>   原神，启动！",
                                                     background="#f0f0f0",
                                                     foreground="black")
                            webbrowser.open_new(
                                "https://ys-api.mihoyo.com/event/download_porter/link/ys_cn/official/pc_default")
                            self.mainButton.configure(state="normal")

                        else:
                            self.maintitle.configure(text="点名器   姓名滚动方向 >>>>>>>>   就是你啦，{}!".format(self.mainName),
                                                     background="#7FFF00")  # , foreground="white")
                            time.sleep(0.5 * 3)
                            self.maintitle.configure(background="#f0f0f0",
                                                     foreground="black")
                            self.mainButton.configure(state="normal")

                        break

            if o > x:
                break

    def flushUI(self):
        self.buttonStatus = True
        self.mainButton.configure(state="disabled")
        self.mainStopButton.configure(state="normal")
        self.maintitle.configure(text="点名器   姓名滚动方向 >>>>>>>>")
        t = threading.Thread(target=self.__flushUI, args=())
        t.start()

    def stopRandom(self):
        # self.mainButton.configure(state="normal")
        self.mainStopButton.configure(state="disabled")
        self.buttonStatus = False

    def exit(self):
        if self.ifExitAgain:
            self.buttonStatus = False
            self.closeThread = True
            self.kill()

        elif tkinter.messagebox.askquestion("退出程序", "确定退出此程序？") == 'yes':
            # tkinter.messagebox.showinfo("退出程序", "让你退了吗？？？")
            self.buttonStatus = False
            self.closeThread = True
            self.kill()
            self.ifExitAgain = True

    def kill(self):
        pid = os.getpid()
        osname = os.name
        if osname == 'nt':
            cmd = "taskkill /pid " + str(pid) + " /f"
            try:
                subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                print(f"ERR: {e}")

        elif osname == "posix":
            cmd = 'kill ' + str(pid)
            try:
                subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                print(f"ERR: {e}")

        else:
            print("Cannot know os.name!")


if __name__ == '__main__':
    maingui()

# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 看牛魔你看！！！
# 牛逼！
