#! usr/bin/python3
# -*- coding:utf-8 -*-
import json
import random
import os
import subprocess
import threading
import time
import tkinter
import tkinter.ttk
import tkinter.messagebox
import ctypes
from ttkbootstrap import Style
import webbrowser

import welcome

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
    "停下来，停下来！！！"
]

Style_all = {
    # 这里存放着受Name Project支持的ttk bootstrap主题
    # 如果你不知道下面主题呈现效果怎么养，请参考文档：
    # 浅色主题文档：https://ttkbootstrap.readthedocs.io/en/latest/zh/themes/light/
    # 深色主题文档：https://ttkbootstrap.readthedocs.io/en/latest/zh/themes/dark/
    "light": [  # 浅色主题
        "cosmo",
        "flatly",
        "journal",
        "litera",
        "lumen",
        "minty",
        "pulse",
        "sandstone",
        "united",
        "yeti",
        "simplex",
    ],
    "dark": [  # 深色主题
        "solar",
        "superhero",
        "darkly",
        "cyborg",
    ]
}


class maingui(tkinter.Tk):
    def __init__(self, studentName: list, debugMode: bool, doRandom: bool, showHello: bool, topMost: bool,
                 geometry: str, style: str = Style_all["light"][0]):
        # 全局继承
        super().__init__()

        self.style = style

        # 判断深浅主题
        if self.style in Style_all["light"]:
            self.styleTheme = "light"
        else:
            self.styleTheme = "dark"

        self.style = Style(theme=self.style)


        # 提高DPI值
        self.debugMode = debugMode
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.tk.call('tk', 'scaling', ScaleFactor / 75)

        # 基础变量
        self.preName = "***"
        if self.debugMode or not showHello:
            self.mainName = "欢迎使用！"
        else:
            self.mainName = an[random.randint(0, len(an) - 1)]
        self.afterName = "***"
        self.buttonStatus = False
        self.closeThread = False
        self.f = True  # 判断是否为第一次使用的变量
        self.ifExitAgain = False

        self.studentName = studentName
        self.debugMode = debugMode
        self.doRandom = doRandom

        self.main_frame = tkinter.Frame(self)
        self.main_frame.pack(fill='both', expand=True)

        self.configure_layout()

        # UI基础设置
        self.title("NameProject - Professional Edition Version 2.11 [Release]")
        self.width = 2500
        self.height = 1200
        self.x_way = 10
        self.left = (self.winfo_screenwidth() - self.width) / 2 + self.width / 2
        self.top = (self.winfo_screenheight() - self.height) / 2 + self.height / 2
        if geometry != "":
            self.geometry(geometry)
        else:
            self.geometry("{}x{}+{}+{}".format(int(self.width), int(self.height), int(self.left), int(self.top)))
        # self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        if topMost:
            self.attributes("-topmost", "true")
        #
        # # 屏幕控件
        # self.maintitle = tkinter.Label(self, text="点名器   姓名滚动方向 >>>>>>>>", font=("Microsoft Yahei UI", 25),
        #                                pady=10)
        # self.maintitle.place(x=0, y=0)
        #
        # # self.onlySep = tkinter.ttk.Separator(self, orient="horizontal")
        # # self.onlySep.pack(fill="x", expand=True, side="top")
        #
        # self.onlySep = tkinter.Label(self,
        #                              text="-" * 343,
        #                              font=("Microsoft Yahei UI", 10))
        # self.onlySep.place(x=0, y=100)
        #
        # self.mainNameLabel = tkinter.Label(self, text=self.mainName, font=("Microsoft Yahei UI", 55),
        #                                    background="#EBDBD1")
        # self.mainNameLabel.place(x=self.width / 2, y=self.height / 2, anchor="center")
        #
        # self.preNameLabel = tkinter.Label(self, text=self.preName, font=("Microsoft Yahei UI", 40), foreground="gray")
        # self.preNameLabel.place(x=self.width - 20, y=self.height / 2, anchor="e")
        #
        # self.afterNameLabel = tkinter.Label(self, text=self.afterName, font=("Microsoft Yahei UI", 40),
        #                                     foreground="gray")
        # self.afterNameLabel.place(x=0 + 20, y=self.height / 2, anchor="w")
        #
        # self.mainButton = tkinter.Button(self, text="开始抽取", relief=tkinter.GROOVE, width=15, height=2,
        #                                  command=self.flushUI, padx=5)
        # self.mainButton.place(x=self.width / 2, y=self.height - 80, anchor="e")
        #
        # self.mainStopButton = tkinter.Button(self, text="停止抽取", relief=tkinter.GROOVE, width=15, height=2,
        #                                      state="disabled", command=self.stopRandom, padx=5)
        # self.mainStopButton.place(x=self.width / 2, y=self.height - 80, anchor="w")

        # tkinter.Label(self, text="Python project, version 2.11 [Release], Python Version 3.11, TCL/Tk Version 3.x",
        #               font=("Microsoft Yahei UI", 9)).pack(side="bottom")

        # tkinter.Label(self,
        #               text="JavaFX Project, Java Version [openJDK17], JavaFX Version [openJFX17], develop by xfypowered.com",
        #               font=("Microsoft Yahei UI", 10)).pack(side="bottom")

        # 由于部分机型无法正确显示窗口内容，故采用此方法
        self.updateWindow()
        # self.updateWindowThread = threading.Thread(target=self.updateWindow, args=())
        # self.updateWindowThread.start()

        self.mainloop()

    def configure_layout(self):
        # 屏幕控件
        self.maintitle = tkinter.Label(self.main_frame, text="NameProject",
                                       font=("Microsoft Yahei UI", 25))
        self.maintitle.pack(side="top", anchor="center", pady=(20, 10))

        # 模拟Separator
        self.onlySep = tkinter.ttk.Separator(self.main_frame, orient="horizontal")
        self.onlySep.pack(side="top", fill='x')
        # self.onlySep = tkinter.Label(self.main_frame,
        #                              text="-" * 343,
        #                              font=("Microsoft Yahei UI", 10), bg="#EBDBD1")  # 背景色可能需要调整以匹配
        # self.onlySep.pack(side="top", fill='x')

        self.mainNameLabel = tkinter.Label(self.main_frame, text=self.mainName, font=("Microsoft Yahei UI", 55),
                                           background="#EBDBD1")
        self.mainNameLabel.pack(side="top", pady=(0, 10), anchor="center")

        self.preNameLabel = tkinter.Label(self.main_frame, text=self.preName, font=("Microsoft Yahei UI", 35),
                                          foreground="gray")
        self.preNameLabel.pack(side="right", anchor="se")

        self.afterNameLabel = tkinter.Label(self.main_frame, text=self.afterName, font=("Microsoft Yahei UI", 35),
                                            foreground="gray")
        self.afterNameLabel.pack(side="left", anchor="sw")

        self.mainButton = tkinter.Button(self.main_frame, text="开始抽取", relief=tkinter.GROOVE, width=15, height=2,
                                         command=self.flushUI, padx=5)
        self.mainButton.pack(side="bottom", anchor="e", pady=(10, 0))

        self.mainStopButton = tkinter.Button(self.main_frame, text="停止抽取", relief=tkinter.GROOVE, width=15,
                                             height=2,
                                             state="disabled", command=self.stopRandom, padx=5)
        self.mainStopButton.pack(side="bottom", anchor="w", pady=(10, 0))

        # 确保所有控件都已配置好后更新窗口
        self.update_idletasks()

    def updateWindow(self):
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

        self.after(100, self.updateWindow)

    def changeTitle(self):
        self.maintitle.configure(
            text="窗口变更！Width={}, Height={}".format(self.winfo_width(),
                                                       self.winfo_height()))
        time.sleep(5)
        self.maintitle.configure(text="NameProject")
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
        random.shuffle(self.studentName)
        # 随机停下时间
        x = random.uniform(0.5, 1.0)
        # 姓名滚动时间隔时间
        o = 0.09
        # 随机标题扩充话语
        if self.f:
            stt = st[0]
            self.f = False
        else:
            if not self.doRandom:
                stt = st[0]
            else:
                stt = st[random.randint(0, len(st) - 1)]
        # 进入事件循环，随机抽取名单直到指定事件触发
        while True:
            if self.closeThread:
                self.exit()

            for i in range(1, len(self.studentName) - 1):
                self.preName = self.studentName[i - 1]
                self.mainName = self.studentName[i]
                self.afterName = self.studentName[i + 1]
                self.preNameLabel.configure(text=self.preName)
                self.mainNameLabel.configure(text=self.mainName)
                self.afterNameLabel.configure(text=self.afterName)
                time.sleep(o)

                if self.buttonStatus:
                    pass
                else:
                    o += 0.05
                    self.maintitle.configure(text="{}".format(stt))
                    self.mainButton.configure(state="disabled")

                    # 程序随机事件
                    if o > x:
                        self.handle_random_event()
                        break

            if o > x:
                break

    def handle_random_event(self):
        random_events = [
            {
                "condition": lambda: random.randint(0, 20) == 5,
                "action": self.handle_special_event_1,
            },
            {
                "condition": lambda: random.randint(0, 200) == 4,
                "action": self.handle_special_event_2,
            },
            # 更改默认条件为一个始终返回True的lambda函数
            {
                "condition": lambda: True,                "action": self.handle_normal_event,
            },
        ]

        for event in random_events:
            if event["condition"]():
                event["action"]()
                break

    def handle_special_event_1(self):
        self.maintitle.configure(text="站讲台上的那位！")
        self.preNameLabel.configure(text="***")
        self.mainNameLabel.configure(text="站讲台上的那位！")
        self.afterNameLabel.configure(text="***")
        self.maintitle.configure(foreground="green")
        time.sleep(3 * 0.5)
        self.reset_title_and_button()

    def handle_special_event_2(self):
        self.maintitle.configure(text="原神，启动！")
        self.preNameLabel.configure(text="***")
        self.mainNameLabel.configure(text="原神，启动！！")
        self.afterNameLabel.configure(text="***")
        self.maintitle.configure(foreground="green")
        time.sleep(3 * 0.5)
        webbrowser.open_new(
            "https://ys-api.mihoyo.com/event/download_porter/link/ys_cn/official/pc_default"
        )
        self.reset_title_and_button()

    def handle_normal_event(self):
        self.maintitle.configure(text="就是你啦，{}!".format(self.mainName))
        self.maintitle.configure(foreground="light green")
        time.sleep(0.5 * 3)
        self.reset_title_and_button()
        time.sleep(5)
        self.maintitle.configure(text="NameProject")

    def reset_title_and_button(self):
        if self.styleTheme == "light":
            self.maintitle.configure(foreground="black")
        else:
            self.maintitle.configure(foreground="white")
        self.mainButton.configure(state="normal")

    def flushUI(self):
        self.buttonStatus = True
        self.mainButton.configure(state="disabled")
        self.mainStopButton.configure(state="normal")
        self.maintitle.configure(text="姓名滚动方向 >>>>>>>>")
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
            # 屏幕初始信息保留
            with open("configure.json", "r", encoding="utf-8") as f:
                tempLoad = json.loads(f.read())
            tempLoad["geometry"] = "{}x{}+{}+{}".format(
                self.winfo_width(),
                self.winfo_height(),
                self.winfo_x(),
                self.winfo_y()
            )
            with open("configure.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(tempLoad, ensure_ascii=False))

            self.kill()

        elif tkinter.messagebox.askquestion("退出程序", "确定退出此程序？") == 'yes':
            # tkinter.messagebox.showinfo("退出程序", "让你退了吗？？？")
            self.buttonStatus = False
            self.closeThread = True
            # 屏幕初始信息保留
            with open("configure.json", "r", encoding="utf-8") as f:
                tempLoad = json.loads(f.read())
            tempLoad["geometry"] = "{}x{}+{}+{}".format(
                self.winfo_width(),
                self.winfo_height(),
                self.winfo_x(),
                self.winfo_y()
            )
            with open("configure.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(tempLoad, ensure_ascii=False))
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
    try:
        with open("configure.json", "r", encoding="utf-8") as f:
            configure = json.loads(f.read())
        maingui(
            studentName=configure["nameLabel"],
            doRandom=configure["other"]["doRandom"],
            showHello=configure["other"]["showHello"],
            topMost=configure["other"]["topMost"],
            debugMode=False,
            geometry=configure["geometry"],
            style=Style_all["dark"][1]  # 在这里修改主题！修改方式参见Style_all变量(在50行附近)
        )
    except FileNotFoundError:
        welcome.setupUI_1()
