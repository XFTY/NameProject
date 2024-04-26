#! usr/bin/python3
# -*- coding:utf-8 -*-
import ctypes
import json
# import logging
import os
import random
import subprocess
import sys
import threading
import time
import tkinter
import tkinter.messagebox
import tkinter.ttk
import webbrowser

import ttkbootstrap
import ttkbootstrap.tooltip
from ttkbootstrap import Style

import welcome

nameProjectConfig = {
    # CN: NameProject项目配置文件，一般情况下不应该更改，除非你知道你在做什么。
    # US: NameProject project configuration file, usually should not be changed unless you know what you are doing.
    "name": "NameProject",
    "version": "3.0[Preview2]",
    "license": "Apache License, Version 2.0"
}

# 这是个废物列表，没什么用，单纯测试时使用
# en: This is a waste list, nothing is useful, just for testing
students_name = [
    "张三",
    "李四",
    "王五",
    "老六"
]

# 开头展示的话语
showHelloAll = [
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
stopShow = [
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

    "light": [  # 浅色主题 en: light theme
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
    "dark": [  # 深色主题 en: dark theme
        "solar",
        "superhero",
        "darkly",
        "cyborg",
    ]
}

# logging.basicConfig(
#     filename="latest.log",
#     filemode="a",
#     format="[%(asctime)s/%(levelname)s] %(message)s",
#     level=logging.INFO,
#     datefmt="%Y-%m-%d %H:%M:%S"
# )
#
# logging.info("NameProject is running")


def logging(Func):
    pass
class maingui(tkinter.Tk):
    def __init__(self, **kwargs):
        """
        初始化窗口程序。

        参数:
        studentName: list, 学生姓名列表。
        debugMode: bool, 是否开启调试模式。
        doRandom: bool, 是否随机显示欢迎信息。
        showHello: bool, 是否显示欢迎信息。
        topMost: bool, 窗口是否始终保持在最顶层。
        geometry: str, 窗口的尺寸和位置。
        style: str, 程序的主题风格，默认为浅色风格。
        fontSize: str, 程序字体大小
        """
        # 全局继承
        super().__init__()

        self.style = kwargs["style"]
        self.fontSize = kwargs["fontSize"]
        self.fontScaleSize = kwargs["fontScaleSize"]

        # 判断深浅主题
        if self.style in Style_all["light"]:
            self.styleTheme = "light"
        else:
            self.styleTheme = "dark"

        self.style = Style(theme=self.style)

        # 提高DPI值，适配高分屏
        self.debugMode = kwargs["debugMode"]
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.tk.call('tk', 'scaling', ScaleFactor / 75)

        # 初始化基础变量
        self.preName = "***"
        if self.debugMode or not kwargs["showHello"]:
            self.mainName = "欢迎使用！"
        else:
            self.mainName = showHelloAll[random.randint(0, len(showHelloAll) - 1)]
        self.afterName = "***"
        self.buttonStatus = False
        self.closeThread = False
        self.f = True  # 判断是否为第一次使用的变量
        self.ifExitAgain = False

        self.studentName = kwargs["studentName"]
        self.debugMode = kwargs["debugMode"]
        self.doRandom = kwargs["doRandom"]
        self.stopNow = kwargs["stopNow"]

        # 创建主框架并设置布局
        self.main_frame = tkinter.Frame(self)
        self.main_frame.pack(fill='both', expand=True)

        self.configure_layout()

        # UI基础设置
        self.title("NameProject - Professional, Version: {}".format(nameProjectConfig["version"]))
        self.width = 2500
        self.height = 1200
        self.x_way = 10
        self.left = (self.winfo_screenwidth() - self.width) / 2 + self.width / 2
        self.top = (self.winfo_screenheight() - self.height) / 2 + self.height / 2
        if kwargs["geometry"] != "":
            self.geometry(kwargs["geometry"])
        else:
            self.geometry("{}x{}+{}+{}".format(int(self.width), int(self.height), int(self.left), int(self.top)))
        # 禁止窗口大小调整
        # self.resizable(False, False)
        # 设置窗口关闭行为
        self.protocol("WM_DELETE_WINDOW", self.exit)
        if kwargs["topMost"]:
            self.attributes("-topmost", "true")

        # 更新窗口显示，确保内容正确显示
        self.updateWindow()
        # 启动窗口更新线程
        # self.updateWindowThread = threading.Thread(target=self.updateWindow, args=())
        # self.updateWindowThread.start()

        # 进入主事件循环
        self.mainloop()

    def configure_layout(self):
        """
        配置窗口布局。
        该方法不接受参数，也不返回任何值。
        它主要用于设置窗口的各种控件，如标题、名字显示、按钮等，并通过pack方法将它们放置在窗口的适当位置。
        """
        # 设置主标题
        self.maintitle = tkinter.Label(self.main_frame, text="NameProject",
                                       font=("Microsoft Yahei UI", self.fontSize["maintitle"]+self.fontScaleSize))
        self.maintitle.pack(side="top", anchor="center", pady=(20, 10))

        # 添加水平分割线
        self.onlySep = tkinter.ttk.Separator(self.main_frame, orient="horizontal")
        self.onlySep.pack(side="top", fill='x')

        # 设置主名称显示
        self.mainNameLabel = tkinter.Label(self.main_frame, text=self.mainName, font=("Microsoft Yahei UI", self.fontSize["mainNameLabel"]+self.fontScaleSize),
                                           background="#EBDBD1")
        self.mainNameLabel.pack(side="top", pady=(0, 10), anchor="center")

        # 设置前置名称显示
        self.preNameLabel = tkinter.Label(self.main_frame, text=self.preName, font=("Microsoft Yahei UI", self.fontSize["preNameLabel"]+self.fontScaleSize),
                                          fg="gray")
        self.preNameLabel.pack(side="right", anchor="se")

        # 设置后置名称显示
        self.afterNameLabel = tkinter.Label(self.main_frame, text=self.afterName, font=("Microsoft Yahei UI", self.fontSize["afterNameLabel"]+self.fontScaleSize),
                                            foreground="gray")
        self.afterNameLabel.pack(side="left", anchor="sw")

        # 使用Tcl语言使按钮控件不变
        self.tk.call('font', 'create', 'buttongroupFont', '-family', 'Microsoft Yahei UI', '-size', 20)

        # 设置开始按钮
        self.mainButton = tkinter.Button(self.main_frame, text="开始抽取", relief=tkinter.GROOVE, width=15, height=2,
                                         command=self.flushUI, font=("Microsoft Yahei UI", self.fontSize["mainButton"]+self.fontScaleSize))
        self.mainButton.pack(side="bottom", anchor="e", pady=(10, 0))

        # 设置停止按钮（初始状态为禁用）
        self.mainStopButton = tkinter.Button(self.main_frame, text="停止抽取", relief=tkinter.GROOVE, width=15,
                                             height=2,
                                             state="disabled", command=self.stopRandom,
                                             font=("Microsoft Yahei UI", self.fontSize["mainStopButton"]+self.fontScaleSize))
        self.mainStopButton.pack(side="bottom", anchor="w")

        ttkbootstrap.tooltip.ToolTip(self.mainButton, text="按下按钮后，点名器名单将被打乱，并以每0.09秒一次的速度滚动")
        ttkbootstrap.tooltip.ToolTip(self.mainStopButton, text="按下按钮后，点名器将依靠惯性停止滚动，并显示当前点名结果")

        # 更新窗口以确保所有控件都已正确显示
        self.update_idletasks()

    def updateWindow(self):
        """
        更新窗口大小和位置，确保界面元素随着窗口大小的变化而正确调整位置。
        无参数
        无返回值
        """
        # 检查窗口当前大小是否与期望大小不同
        if self.winfo_width() != self.width or self.winfo_height() != self.height:
            # 更新窗口宽度和高度
            self.width = self.winfo_width()
            self.height = self.winfo_height()

            # 更新界面元素的位置以适应新的窗口大小
            self.mainNameLabel.place(x=self.width / 2, y=self.height / 2, anchor="center")
            self.preNameLabel.place(x=self.width - 20, y=self.height / 2, anchor="e")
            self.afterNameLabel.place(x=0 + 20, y=self.height / 2, anchor="w")
            self.mainButton.place(x=self.width / 2, y=self.height - 80, anchor="e")
            self.mainStopButton.place(x=self.width / 2, y=self.height - 80, anchor="w")

            # 在新线程中启动标题更改任务，以避免阻塞UI线程
            t = threading.Thread(target=self.changeTitle, args=())
            t.start()

        # 设置定时器，100毫秒后再次调用updateWindow，以持续更新窗口状态
        self.after(100, self.updateWindow)

    def changeTitle(self):
        pass
        # self.maintitle.configure(
        #     text="窗口变更！Width={}, Height={}".format(self.winfo_width(),
        #                                                self.winfo_height()))
        # time.sleep(5)
        # self.maintitle.configure(text="NameProject")

        # time.sleep(0.01)

        # self.after(10, self.updateWindow)

    def __flushUI(self):
        """
        私有方法，用于刷新用户界面UI。
        打乱姓名列表，并以随机顺序滚动显示姓名，同时可以随机停在某个姓名上显示特定时间。
        """

        # 打乱学生姓名列表，以实现随机滚动效果
        random.shuffle(self.studentName)
        # 随机确定停止显示的时间点
        x = random.uniform(0.5, 1.0)
        # 设置姓名滚动的时间间隔
        o = 0.09
        # 随机选择停止显示时的标题扩充语句
        if self.f:
            stt = stopShow[0]
            self.f = False
        else:
            if not self.doRandom:
                stt = stopShow[0]
            else:
                stt = stopShow[random.randint(0, len(stopShow) - 1)]

        # 无限循环，直到触发特定事件才退出
        while True:
            # 检测是否需要退出程序
            if self.closeThread:
                self.exit()

            # 遍历姓名列表，逐个显示姓名
            for i in range(1, len(self.studentName) - 1):
                self.preName = self.studentName[i - 1]
                self.mainName = self.studentName[i]
                self.afterName = self.studentName[i + 1]
                self.preNameLabel.configure(text=self.preName)
                self.mainNameLabel.configure(text=self.mainName)
                self.afterNameLabel.configure(text=self.afterName)
                time.sleep(o)

                # 如果按钮处于激活状态，则不进行下面的操作
                if not self.buttonStatus:
                    if self.stopNow:
                        self.handle_random_event()
                        return 0
                    else:
                        o += 0.05  # 增加时间间隔
                        self.maintitle.configure(text="{}".format(stt))  # 更新标题
                        self.mainButton.configure(state="disabled")  # 禁用主按钮

                    # 当时间间隔超过x时，触发随机事件，并结束当前循环
                    # 话说为什么，注释掉下面6行代码程序会抽风？因为我的电脑？
                    if self.stopNow:
                        self.handle_random_event()
                        return 0
                    elif o > x:
                        self.handle_random_event()
                        return 0

            # 如果时间间隔超过x，退出循环
            # if self.stopNow:
            #     self.handle_random_event()
            #     break
            # elif o > x:
            #     break

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
                "condition": lambda: True,
                "action": self.handle_normal_event,
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
        """
        刷新用户界面UI的函数。

        该函数旨在修改用户界面的某些元素状态，包括按钮和标题，并通过开启新线程来执行某些操作，
        以达到异步效果，不影响用户界面的响应性。

        参数:
        self - 对象本身的引用，允许访问类的属性和方法。

        返回值:
        无
        """
        self.buttonStatus = True  # 标记按钮状态为启用
        self.mainButton.configure(state="disabled")  # 禁用主按钮
        self.mainStopButton.configure(state="normal")  # 启用停止按钮
        self.maintitle.configure(text="姓名滚动方向 >>>>>>>>")  # 修改标题文本
        t = threading.Thread(target=self.__flushUI, args=())  # 创建并启动新线程，执行__flushUI方法
        t.start()  # 启动线程

    def stopRandom(self):
        # self.mainButton.configure(state="normal")
        self.mainStopButton.configure(state="disabled")
        self.buttonStatus = False

    def exit(self):
        """
        处理程序退出逻辑。
        若ifExitAgain为True，则直接退出程序，并更新配置文件中的窗口位置和大小信息；
        若ifExitAgain为False，则弹出确认对话框，若用户选择是，则进行退出操作。
        """
        if self.ifExitAgain:
            # 直接退出流程
            self.buttonStatus = False
            self.closeThread = True
            # 读取并更新配置文件中的窗口geometry信息
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

            self.kill()  # 关闭程序

        # elif True:
        #     WarningBeforeClose(
        #         parent=self,
        #         winfo_width=self.winfo_width(),
        #         winfo_height=self.winfo_height(),
        #         winfo_x=self.winfo_x(),
        #         winfo_y=self.winfo_y(),
        #         kill=self.kill
        #     )

        elif tkinter.messagebox.askquestion("退出程序", "确定退出此程序？") == 'yes':
            # 用户确认退出流程
            self.buttonStatus = False
            self.closeThread = True
            # 读取并更新配置文件中的窗口geometry信息
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
            self.kill()  # 关闭程序

    def kill(self):
        """
        终止当前进程。

        该方法根据操作系统的不同，使用不同的命令来终止当前进程。
        在Windows系统上，使用taskkill命令；在POSIX兼容系统上，使用kill命令。
        不接受任何参数。
        无返回值。
        """
        pid = os.getpid()  # 获取当前进程的PID
        osname = os.name  # 获取当前操作系统的名称

        if osname == 'nt':  # 检查是否在Windows系统上
            # 构造taskkill命令，并强制终止进程
            cmd = "taskkill /pid " + str(pid) + " /f"
            try:
                subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                print(f"ERR: {e}")

        elif osname == "posix":  # 检查是否在POSIX兼容系统上
            # 构造kill命令，终止进程
            cmd = 'kill ' + str(pid)
            try:
                subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                print(f"ERR: {e}")

        else:  # 处理无法识别的操作系统情况
            print("Cannot know os.name!")


if __name__ == '__main__':
    """
    主程序入口。

    本段代码负责初始化主界面（`maingui`）并传递配置参数。配置信息从"configure.json"文件中读取，
    若文件不存在则显示欢迎界面（`welcome.setupUI_1()`）。

    配置项包括：

    - `studentName`: 学生姓名标签文本
    - `doRandom`: 是否执行随机功能（布尔值）
    - `showHello`: 是否显示问候语（布尔值）
    - `topMost`: 窗口是否总在最前（布尔值）
    - `debugMode`: 调试模式开关（目前固定为False）
    - `geometry`: 窗口布局几何信息
    - `style`: 界面风格，取自`Style_all["dark"][1]`，可在此处修改主题。详细主题列表及修改方式参见约第60行的`Style_all`变量定义。
    
    这些设置项在configure.json文件中进行修改。

    """

    try:
        with open("configure.json", "r", encoding="utf-8") as f:
            configure = json.loads(f.read())  # 从JSON文件中加载配置数据

        if not configure["eula"]:
            eula = tkinter.messagebox.askquestion("使用许可协议",
                                                  "您在配置文件中未同意使用许可协议，选择‘是’同意许可协议，否则将退出程序。")
            if eula == "yes":
                configure["eula"] = True
            else:
                configure["eula"] = False
                exit()

        # 检测配置文件版本
        try:
            if configure["configVersion"] != 3.1:
                tkinter.messagebox.showerror("配置文件版本错误", "配置文件版本错误\n要求版本：3.1或者更高版本\n当前版本：" + str(configure["configVersion"]) + "\n")
                sys.exit()  # 退出程序防止程序无法读取配置文件
        except KeyError:
            tkinter.messagebox.showerror("配置文件版本错误", "配置文件版本错误\n要求版本：3.1或者更高版本\n当前版本：未找到\n是否删除了configVersion，或者配置版本过旧？")
            sys.exit()  # 退出程序防止程序无法读取配置文件

        maingui(
            studentName=configure["nameLabel"],  # 学生姓名标签文本
            doRandom=configure["other"]["doRandom"],  # 随机功能开关
            showHello=configure["other"]["showHello"],  # 显示问候语开关
            topMost=configure["other"]["topMost"],  # 窗口总在最前开关
            debugMode=False,  # 调试模式（固定为False）
            geometry=configure["geometry"],  # 窗口布局几何信息
            style=configure["uiBasicSittings"]["style"],  # 主题选择（参考`Style_all`变量进行修改）
            fontSize=configure["fontSize"],  # 字体大小
            fontScaleSize=configure["fontScaleSize"],  # 字体缩放比例
            stopNow=configure["stopNow"]
        )  # 初始化并展示主界面

    except:
        welcome.openWelcomeUI()  # 当"configure.json"文件未找到时，显示欢迎界面
