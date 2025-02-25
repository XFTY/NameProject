#! /usr/bin/env python3
# --------------------------------------------------------------------------------------------------
# | 版权所有 XFTY，保留所有权利。
# | 代码遵循Apache 2.0开源协议，浏览在根目录的LICENSE文件以获取更多信息。
# |
# | Copyright (c) 2021-2022 XFTY, All Rights Reserved.
# | Licensed under the Apache License 2.0. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------------

import json
import ctypes
import sys
import tkinter
from tkinter import messagebox
import traceback

from ttkbootstrap import Style
from ttkbootstrap.widgets import *


Style_all = {
    # 这里存放着受Name Project支持的ttk bootstrap主题
    # 如果你不知道下面主题呈现效果怎么养，请参考文档：
    # 浅色主题文档：https://ttkbootstrap.readthedocs.io/en/latest/zh/themes/light/
    # 深色主题文档：https://ttkbootstrap.readthedocs.io/en/latest/zh/themes/dark/

    # 主题名称后面的数字是为了适应煞笔tkinter combobox的

    "light": {  # 浅色主题 en: light theme
        "cosmo": 1,
        "flatly": 2,
        "journal": 3,
        "litera": 4,
        "lumen": 5,
        "minty": 6,
        "pulse": 7,
        "sandstone": 8,
        "united": 9,
        "yeti": 10,
        "simplex": 11,
    },
    "dark": {  # 深色主题 en: dark theme
        "solar": 13,
        "superhero": 14,
        "darkly": 15,
        "cyborg": 16,
    }
}


class SettingsUI(tkinter.Tk):
    def __init__(self):
        global Style_all

        super().__init__()

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
        self.tk.call('tk', 'scaling', ScaleFactor / 75)

        self.title("NameProject 3 设置")
        self.geometry("1600x800")

        self.read_json_file()  # 该方法会生成self.globalConfigureFile变量可供读取

        # print(self.globalConfigureFile["uiBasicSittings"]["style"])

        self.style = Style(theme=self.globalConfigureFile["uiBasicSittings"]["style"])
        self.current_tab_content = None

        self.paned_window = PanedWindow(orient=tk.HORIZONTAL)
        self.paned_window.pack(fill='both', expand=True)

        self.tabs_container = Frame(self.paned_window, padding=10)
        self.settings_container = Frame(self.paned_window, padding=10)

        self.paned_window.add(self.tabs_container, weight=2)
        self.paned_window.add(self.settings_container, weight=4)  # 适当调整权重以满足布局需求

        background_color = self.style.lookup('TFrame', 'background')

        # 创建系统和应用按钮，宽充满左侧，高度不变，背景色与窗口背景色一致
        self.title_label = Label(
            self.tabs_container,
            text="所有设置",
            width=0,
            style=f'Custom.TLabel'
        )
        self.main_button = Button(self.tabs_container,
                                  text="主题和特色功能",
                                  command=self.show_main_settings,
                                  width=0,  # 宽度自动填充  # 指定固定高度
                                  # Style_all=f'Custom.TButton'
                                  )  # 背景色与窗口背景色一致

        self.name_button = Button(self.tabs_container,
                                  text="点名器名单",
                                  command=self.show_name_settings,
                                  width=0,  # 宽度自动填充 # 指定固定高度
                                  style=f'Custom.TButton')  # 背景色与窗口背景色一致

        self.display_button = Button(self.tabs_container,
                                     text="显示设置",
                                     command=self.show_display_settings,
                                     width=0,  # 宽度自动填充 # 指定固定高度
                                     style=f'Custom.TButton'

        )

        self.about_label = Label(self.tabs_container, text="关于NameProject", width=0)

        self.update_button = Button(self.tabs_container,
                                    text="检查更新[不可用]",
                                    command=self.show_update_settings,
                                    width=0,  # 宽度自动填充 # 指定固定高度
                                    bootstyle='error',
                                    )

        self.about_button = Button(self.tabs_container,
                                   text="关于NameProject",
                                   command=self.show_about_settings,
                                   width=0,  # 宽度自动填充 # 指定固定高度
                                   style=f'Custom.TButton'
                                   )

        # 需要在初始化样式时定义Custom.TButton的背景色
        self.style.configure('Custom.TButton', background=background_color)
        self.title_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.main_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.name_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.display_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.about_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.update_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.about_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.paned_window.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

        # 初始化显示系统设置
        self.show_hello_settings()

        self.mainloop()


    def show_hello_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        self.main_settings_0 = Frame(self.settings_container, padding=10)

        Label(self.main_settings_0, text="欢迎使用NameProject设置程序！", font=("微软雅黑", 25)).pack(pady=10, anchor="center")
        Label(self.main_settings_0, text="轻点左边的按钮开始设置", font=("微软雅黑", 12)).pack(pady=10, anchor="center")

        self.main_settings_0.pack(fill=tk.BOTH, expand=True)

        self.current_tab_content = self.main_settings_0

    def show_main_settings(self):

        globalConfigureFile = self.globalConfigureFile

        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        # 第一个Frame
        self.main_settings_1 = Frame(self.settings_container, padding=10)

        # Label(self.main_settings_1, text="主要设置", font=("微软雅黑", 20)).pack(pady=10, anchor="w")
        # Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(10, 5))

        Label(self.main_settings_1, text="主题", font=("微软雅黑", 20)).pack(pady=(10, 5), anchor="w")
        Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        Label(self.main_settings_1, text="在下方的列表中选择主题", font=("微软雅黑", 10)).pack(pady=1, anchor="w")
        # Label(self.main_settings_1, text="由ttkbootstrap提供主题，", font=("微软雅黑", 10)).pack(pady=1, anchor="w")
        self.styleCombobox = Combobox(self.main_settings_1, values=["------浅色主题------", "cosmo", "flatly", "journal", "litera", "lumen", "minty", "pulse", "sandstone", "united", "yeti", "simplex", "------深色主题------", "solar", "superhero", "darkly", "cyborg"], font=("微软雅黑", 10), state="readonly")

        try:
            self.styleCombobox.current(Style_all["light"][globalConfigureFile["uiBasicSittings"]["style"]])
        except KeyError:
            self.styleCombobox.current(Style_all["dark"][globalConfigureFile["uiBasicSittings"]["style"]])

        self.styleCombobox.pack(pady=(5, 5), anchor="w")

        # Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(10, 5))

        Label(self.main_settings_1, text="特色功能", font=("微软雅黑", 20)).pack(pady=(10, 5), anchor="w")

        Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # 显示问候语
        setHelloFrame = Frame(self.main_settings_1)
        setHelloFrame.pack(pady=5, anchor="w", fill="x")

        # 创建读取变量
        self.setHelloBlVar = tkinter.BooleanVar()
        self.setHelloBlVar.set(self.globalConfigureFile["other"]["showHello"])

        Label(setHelloFrame, text="显示问候语", font=("微软雅黑", 10)).pack(side=tk.LEFT)
        setHelloButton = Checkbutton(setHelloFrame, bootstyle="success-round-toggle", variable=self.setHelloBlVar)

        setHelloButton.pack(side=tk.RIGHT)

        # 添加随机事件
        setRandomEventFrame = Frame(self.main_settings_1)
        setRandomEventFrame.pack(pady=5, anchor="w", fill="x")

        self.setRandomEventBlVar = tkinter.BooleanVar()
        self.setRandomEventBlVar.set(self.globalConfigureFile["other"]["doRandom"])

        Label(setRandomEventFrame, text="添加随机事件", font=("微软雅黑", 10)).pack(side=tk.LEFT)

        setRandomEventButton = Checkbutton(setRandomEventFrame, bootstyle="success-round-toggle", variable=self.setRandomEventBlVar)
        setRandomEventButton.pack(side=tk.RIGHT)

        # 置顶窗口
        setTopFrame = Frame(self.main_settings_1)
        setTopFrame.pack(pady=5, anchor="w", fill="x")

        Label(setTopFrame, text="置顶窗口", font=("微软雅黑", 10)).pack(side=tk.LEFT)

        self.setTopBlVar = tkinter.BooleanVar()
        self.setTopBlVar.set(self.globalConfigureFile["other"]["topMost"])

        setTopButton = Checkbutton(setTopFrame, bootstyle="success-round-toggle", variable=self.setTopBlVar)
        setTopButton.pack(side=tk.RIGHT)

        # 立即停止抽取
        self.stopNowFrame = Frame(self.main_settings_1)
        self.stopNowFrame.pack(pady=5, anchor="w", fill="x")

        self.stopNowBlVar = tkinter.BooleanVar()
        self.stopNowBlVar.set(self.globalConfigureFile["stopNow"])

        Label(self.stopNowFrame, text="立即停止抽取", font=("微软雅黑", 10)).pack(side=tk.LEFT)

        self.stopNowButton = Checkbutton(self.stopNowFrame, bootstyle="success-round-toggle", variable=self.stopNowBlVar)
        self.stopNowButton.pack(side=tk.RIGHT)
        Label(self.main_settings_1, text="释义：在用户按下“停止抽取”按钮后立即停止抽取，不依靠惯性滚动", font=("微软雅黑", 10)).pack(anchor="w")


        self.applyChangeButton = Button(self.main_settings_1, text="保存更改", command=self.mainApplyChangeButtonFunc)
        self.applyChangeButton.pack(pady=5, anchor="e", side="bottom")

        self.main_settings_1.pack(fill='both', expand=True)
        self.current_tab_content = self.main_settings_1

        # 检查设置是否正确
        self.checkSittingsIsCurrect()

    def mainApplyChangeButtonFunc(self):
        # 备份全局配置文件
        globalConfigureFile = self.globalConfigureFile

        # 应用用户更改
        globalConfigureFile["other"]["doRandom"] = self.setRandomEventBlVar.get()
        globalConfigureFile["other"]["showHello"] = self.setHelloBlVar.get()
        globalConfigureFile["other"]["topMost"] = self.setTopBlVar.get()
        globalConfigureFile["stopNow"] = self.stopNowBlVar.get()

        globalConfigureFile["uiBasicSittings"]["style"] = self.styleCombobox.get()

        try:
            self.change_json_file(globalConfigureFile)
            self.style = Style(theme=self.globalConfigureFile["uiBasicSittings"]["style"])
            messagebox.showinfo("成功", "更改已保存，重启软件以生效更改")
        except:
            messagebox.showerror("错误", "无法保存更改，请检查文件是否被占用或者其他问题\n"+traceback.format_exc())

    def show_name_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        self.name_settings = Frame(self.settings_container, padding=10)

        # 使用默认字体
        Label(self.name_settings, text="点名器名单", font=("微软雅黑", 20)).pack(pady=10, anchor="w")
        Separator(self.name_settings, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(10, 5))
        Label(self.name_settings, text="在此处修改点名器名单\n注意：一个学生姓名为一行", wraplength=400).pack(anchor="w",
                                                                                                             pady=5)

        # 设置Text控件的最大显示行数（例如10行）
        max_rows = 10
        self.nameTexter = tk.Text(self.name_settings, width=20, height=max_rows, font=("微软雅黑", 20))

        for i in self.namelabel:
            self.nameTexter.insert("insert", i + "\n")

        # 添加滚动条并与Text控件紧密结合
        scrollbary = tk.Scrollbar(self.name_settings, orient=tk.VERTICAL, command=self.nameTexter.yview)
        self.nameTexter['yscrollcommand'] = scrollbary.set

        self.apply_change_button = Button(self.name_settings, text="应用更改", command=self.apply_change_button_func)

        self.apply_change_button.pack(side='bottom', pady=5, anchor="se")
        self.nameTexter.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbary.pack(side=tk.LEFT, fill=tk.Y)

        # 确保name_settings在主窗体中可见
        self.name_settings.pack(fill='both', expand=True)

        self.current_tab_content = self.name_settings


    def apply_change_button_func(self):
        get = self.nameTexter.get(0.0, "end")
        get = get.split("\n")

        print(get)

        # for i in range(len(get) - 1):
        #     print(i)
        #     if get[i] == "":
        #         del get[i]

        globalConfigFile = self.globalConfigureFile
        globalConfigFile["nameLabel"].clear()
        for i in get:
            globalConfigFile["nameLabel"].append(i)

        globalConfigFile["nameLabel"] = list(filter(None, globalConfigFile["nameLabel"]))

        print(globalConfigFile["nameLabel"])

        try:
            self.change_json_file(globalConfigFile)
            tkinter.messagebox.showinfo("成功", "点名器名称已被修改！")
        except Exception as e:
            messagebox.showerror("我们在执行‘应用更改时’发生了错误",
                                 "原因未知，你可以在下面的TraceBack中获取详情信息\n\n" + traceback.format_exc())

    def show_display_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        self.displaySittings = Frame(self.settings_container, padding=10)

        Label(self.displaySittings, text="字体设置", font=("微软雅黑", 20)).pack(pady=10, anchor="w")
        Separator(self.displaySittings, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 5))
        Label(self.displaySittings, text="请通过滑块调整需要增加的字体大小，上限为20，下限为-20").pack(pady=10, anchor="w")

        self.showWhere = Label(self.displaySittings, text="当前值为：{}".format("null"))
        self.showWhere.pack(pady=10, anchor="w")

        self.scale = Scale(self.displaySittings, from_=-20, to=20, orient=tk.HORIZONTAL)
        self.scale.set(self.globalConfigureFile["fontScaleSize"])
        self.scale.pack(fill=tk.X)

        Label(self.displaySittings, text="注意：‘设置’中的字体不受此处设置影响", foreground="red").pack(pady=10, anchor="w")

        self.displaySittings.pack(fill=tk.BOTH, expand=True)

        Button(self.displaySittings, text="应用更改", command=self.displayApplyChangeButtonFunc).pack(side="bottom", anchor="e")

        self.checkDisplaySittings()

        self.current_tab_content = self.displaySittings

    def displayApplyChangeButtonFunc(self):
        final = int(self.scale.get())
        globalConfigureFile = self.globalConfigureFile
        globalConfigureFile["fontScaleSize"] = final
        try:
            self.change_json_file(globalConfigureFile)
            messagebox.showinfo("成功", "更改已保存，重启软件以生效更改")
        except:
            messagebox.showerror("错误", "无法保存更改，请检查文件是否被占用或者其他问题\n"+traceback.format_exc())

    def checkDisplaySittings(self):
        self.showWhere.configure(text="当前值为：{}".format(int(self.scale.get())))

        globalConfigureFile = self.globalConfigureFile
        

        self.after(100, self.checkDisplaySittings)

    def show_update_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        self.updateSittings = Frame(self.settings_container, padding=10)

        Label(self.updateSittings, text="软件更新", font=("微软雅黑", 20)).pack(pady=10, anchor="w")
        Separator(self.updateSittings, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 5))
        Label(self.updateSittings, text="在此处显示软件的更新信息").pack(pady=10,
                                                                                                     anchor="w")

        self.updateSittings.pack(fill=tk.BOTH, expand=True)

        self.current_tab_content = self.updateSittings

    def show_about_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        self.aboutSittings = Frame(self.settings_container, padding=10)

        Label(self.aboutSittings, text="关于NameProject", font=("微软雅黑", 20)).pack(pady=10)
        Separator(self.aboutSittings, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 5))
        Label(self.aboutSittings, text="一个普普通通的点名器").pack(fill=tk.X)
        Label(self.aboutSittings, text="版本：{}".format(self.globalConfigureFile["version"]), font=("微软雅黑", 10)).pack(fill=tk.X)
        Label(self.aboutSittings, text="Python运行版本：{}".format(sys.version)).pack(fill=tk.X)
        Label(self.aboutSittings, text="感谢ttkbootstrap项目提供的主题！！！").pack(fill=tk.X)
        Label(self.aboutSittings, text="2024, XFTY, 遵循Apache Version 2.0 开源").pack(side=tk.BOTTOM)

        self.aboutSittings.pack(fill=tk.BOTH, expand=True)
        self.current_tab_content = self.aboutSittings

    def checkSittingsIsCurrect(self):
        if self.styleCombobox.get() == "------浅色主题------" or self.styleCombobox.get() == "------深色主题------":
            self.applyChangeButton.configure(state="disabled", text="不可用，因为主题选择错误")

        else:
            self.applyChangeButton.configure(state="normal", text="应用更改")

        self.after(100, self.checkSittingsIsCurrect)


    def read_json_file(self):
        isOpen = False
        try:
            with open("configure.json", "r", encoding="utf-8") as f:
                r = json.loads(f.read())
                self.globalConfigureFile = r
                self.namelabel = r["nameLabel"]
                isOpen = True

                try:
                    if self.globalConfigureFile["configVersion"] != 3.1:
                        tkinter.messagebox.showerror("配置文件版本错误",
                                                     "配置文件版本错误\n要求版本：3.1或者更高版本\n当前版本：" + str(
                                                         self.globalConfigureFile["configVersion"]) + "\n")
                        sys.exit()  # 退出程序防止程序无法读取配置文件
                except KeyError:
                    tkinter.messagebox.showerror("配置文件版本错误",
                                                 "配置文件版本错误\n要求版本：3.1或者更高版本\n当前版本：未找到\n是否删除了configVersion，或者配置版本过旧？")
                    sys.exit()  # 退出程序防止程序无法读取配置文件

        except FileNotFoundError:
            with open("configure.json", "w", encoding="utf-8") as f:
                f.write(json.dumps("", ensure_ascii=False))
            # messagebox.showerror("我们在执行‘读取配置文件时’发生了错误",
            #                      "您的配置文件似乎丢失或损坏\n\n详情信息：\n" + traceback.format_exc())

        except Exception:  # 用于处理未知异常
            messagebox.showerror("我们在执行‘读取配置文件时’发生了错误",
                                 "原因未知，你可以在下面的TraceBack中获取详情信息\n\n" + traceback.format_exc())

        finally:
            if not isOpen:  # 前面创建了isOpen变量用于判断文件是否打开，如果打开则会判定为True，否则为False
                sys.exit()  # 这里判断isOpen是否为True，就不执行这行代码，反则反之。

    def change_json_file(self, configFileJsonText):
        with open("configure.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(configFileJsonText, ensure_ascii=False))


if __name__ == "__main__":
    SettingsUI()
