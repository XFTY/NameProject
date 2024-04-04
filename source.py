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

nameProjectConfig = {
    # CN: NameProject项目配置文件，一般情况下不应该更改，除非你知道你在做什么。
    # US: NameProject project configuration file, usually should not be changed unless you know what you are doing.
    "name": "NameProject",
    "version": "3.0[Beta1]",
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


class WarningBeforeClose(tkinter.Toplevel):
    def __init__(self, parent, winfo_width, winfo_height, winfo_x, winfo_y, kill):
        super().__init__(parent)

        # 应用传入的参数
        # 这里需要传入maingui中的参数，而不是WarningBeforeClose自带的参数
        self.maingui_winfo_width = winfo_width
        self.maingui_winfo_height = winfo_height
        self.maingui_winfo_x = winfo_x
        self.maingui_winfo_y = winfo_y
        self.maingui_kill = kill

        # 窗口居中显示
        self.center_window()

        # 设置窗口大小，例如：宽100像素，高100像素
        self.geometry("400x320")

        # 创建一个提示消息和两个选项按钮（退出程序、进入设置）
        self.message_label = tkinter.Label(self, text="您确定要退出程序吗？\n请选择操作：",
                                           font=("Noto Sans CJK SC", 15))  # 更改为“Noto Sans CJK SC”
        self.quit_button = tkinter.Button(self, text="退出程序", font=("Noto Sans CJK SC", 15),
                                          command=self.on_close_request)
        self.settings_button = tkinter.Button(self, text="进入设置", font=("Noto Sans CJK SC", 15),
                                              command=self.open_settings)

        # 布局设置
        self.message_label.pack(pady=50)  # 增加顶部间距

        # 将设置按钮放在左下角
        # print(self.winfo_width(), self.winfo_height())
        self.settings_button.pack(side=tkinter.BOTTOM, padx=10, pady=10)

        # 将退出程序按钮放在右下角
        self.quit_button.pack(side=tkinter.BOTTOM, padx=10, pady=10)



    def on_close_request(self):
        """
        处理窗口关闭请求事件。
        弹出一个询问对话框，让用户选择是否确认退出。
        """
        result = tkinter.messagebox.askyesno("确认退出", "您真的要退出程序吗？")

        if result:
            with open("configure.json", "r", encoding="utf-8") as f:
                tempLoad = json.loads(f.read())
            tempLoad["geometry"] = "{}x{}+{}+{}".format(
                self.maingui_winfo_width,
                self.maingui_winfo_height,
                self.maingui_winfo_x,
                self.maingui_winfo_y
            )
            # print(tempLoad)
            with open("configure.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(tempLoad, ensure_ascii=False))
            self.maingui_kill()  # 关闭程序 # 确认则销毁主窗口并退出程序
        else:
            self.deiconify()  # 否则恢复窗口可见状态（如果之前被隐藏）

    def open_settings(self):
        """
        打开设置界面或执行相应的设置功能。
        这里仅作为示例，实际应用中请替换为您的具体设置逻辑。
        """
        # 实现打开设置界面或执行相应设置操作的代码

        # settings_ui = sittings.SettingsUI(parent=self)

        # tkinter.messagebox.showinfo("提示", "进入设置界面的功能尚未实现，请稍后完善！")

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
        self.geometry(f"+{x+100}+{y+100}")


class maingui(tkinter.Tk):
    def __init__(self, studentName: list, debugMode: bool, doRandom: bool, showHello: bool, topMost: bool,
                 geometry: str, style: str = Style_all["light"][0]):
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
        """
        # 全局继承
        super().__init__()

        self.style = style


        # 判断深浅主题
        if self.style in Style_all["light"]:
            self.styleTheme = "light"
        else:
            self.styleTheme = "dark"

        self.style = Style(theme=self.style)

        # 提高DPI值，适配高分屏
        self.debugMode = debugMode
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.tk.call('tk', 'scaling', ScaleFactor / 75)

        # 初始化基础变量
        self.preName = "***"
        if self.debugMode or not showHello:
            self.mainName = "欢迎使用！"
        else:
            self.mainName = showHelloAll[random.randint(0, len(showHelloAll) - 1)]
        self.afterName = "***"
        self.buttonStatus = False
        self.closeThread = False
        self.f = True  # 判断是否为第一次使用的变量
        self.ifExitAgain = False

        self.studentName = studentName
        self.debugMode = debugMode
        self.doRandom = doRandom

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
        if geometry != "":
            self.geometry(geometry)
        else:
            self.geometry("{}x{}+{}+{}".format(int(self.width), int(self.height), int(self.left), int(self.top)))
        # 禁止窗口大小调整
        # self.resizable(False, False)
        # 设置窗口关闭行为
        self.protocol("WM_DELETE_WINDOW", self.exit)
        if topMost:
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
                                       font=("Microsoft Yahei UI", 25))
        self.maintitle.pack(side="top", anchor="center", pady=(20, 10))

        # 添加水平分割线
        self.onlySep = tkinter.ttk.Separator(self.main_frame, orient="horizontal")
        self.onlySep.pack(side="top", fill='x')

        # 设置主名称显示
        self.mainNameLabel = tkinter.Label(self.main_frame, text=self.mainName, font=("Microsoft Yahei UI", 55),
                                           background="#EBDBD1")
        self.mainNameLabel.pack(side="top", pady=(0, 10), anchor="center")

        # 设置前置名称显示
        self.preNameLabel = tkinter.Label(self.main_frame, text=self.preName, font=("Microsoft Yahei UI", 35),
                                          foreground="gray")
        self.preNameLabel.pack(side="right", anchor="se")

        # 设置后置名称显示
        self.afterNameLabel = tkinter.Label(self.main_frame, text=self.afterName, font=("Microsoft Yahei UI", 35),
                                            foreground="gray")
        self.afterNameLabel.pack(side="left", anchor="sw")

        # 设置开始按钮
        self.mainButton = tkinter.Button(self.main_frame, text="开始抽取", relief=tkinter.GROOVE, width=15, height=2,
                                         command=self.flushUI, padx=5)
        self.mainButton.pack(side="bottom", anchor="e", pady=(10, 0))

        # 设置停止按钮（初始状态为禁用）
        self.mainStopButton = tkinter.Button(self.main_frame, text="停止抽取", relief=tkinter.GROOVE, width=15,
                                             height=2,
                                             state="disabled", command=self.stopRandom, padx=5)
        self.mainStopButton.pack(side="bottom", anchor="w", pady=(10, 0))

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
                if self.buttonStatus:
                    pass
                else:
                    o += 0.05  # 增加时间间隔
                    self.maintitle.configure(text="{}".format(stt))  # 更新标题
                    self.mainButton.configure(state="disabled")  # 禁用主按钮

                    # 当时间间隔超过x时，触发随机事件，并结束当前循环
                    if o > x:
                        self.handle_random_event()
                        break

            # 如果时间间隔超过x，退出循环
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
    - `style`: 界面风格，取自`Style_all["dark"][1]`，可在此处修改主题。详细主题列表及修改方式参见约第50行的`Style_all`变量定义。
    
    这些设置项在configure.json文件中进行修改。

    """

    try:
        with open("configure.json", "r", encoding="utf-8") as f:
            configure = json.loads(f.read())  # 从JSON文件中加载配置数据
        maingui(
            studentName=configure["nameLabel"],  # 学生姓名标签文本
            doRandom=configure["other"]["doRandom"],  # 随机功能开关
            showHello=configure["other"]["showHello"],  # 显示问候语开关
            topMost=configure["other"]["topMost"],  # 窗口总在最前开关
            debugMode=False,  # 调试模式（固定为False）
            geometry=configure["geometry"],  # 窗口布局几何信息
            style=Style_all["dark"][1]  # 主题选择（参考`Style_all`变量进行修改）
        )  # 初始化并展示主界面

    except FileNotFoundError:
        welcome.setupUI_1()  # 当"configure.json"文件未找到时，显示欢迎界面
