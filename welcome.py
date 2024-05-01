import json
import sys
import tkinter
from tkinter import messagebox
import traceback

from ttkbootstrap import Style
from ttkbootstrap.widgets import *

# 配置文件模板
# 请不要更改里面的内容，不然主程序会寄
configureFile = {
    "configVersion": 3.1,
    "version": "3.0.1",
    "eula": True,
    "geometry": "",
    "nameLabel": [],
    "other": {
        "doRandom": True,
        "showHello": True,
        "topMost": False
    },
    "uiBasicSittings": {
        "style": "superhero"  # 默认ttkbootstrap样式
    },
    "fontSize": {
        "maintitle": 45,
        "mainNameLabel": 55,
        "preNameLabel": 35,
        "afterNameLabel": 35,
        "mainButton": 13,
        "mainStopButton": 13
    },
    # 修改字体缩放大小
    "fontScaleSize": 0,
    "stopNow": True
}

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

class welcomeUI(tkinter.Tk):
    def __init__(self, **kwargs):
        global Style_all

        super().__init__()
        self.title("点名器设置")
        self.geometry("1200x600")

        self.globalConfigurePreFile = kwargs["modeConfigFile"]

        # print(self.globalConfigurePreFile["uiBasicSittings"]["style"])

        self.style = Style(theme="superhero")
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
            text="安装步骤",
            width=0,
            style=f'Custom.TLabel'
        )
        self.main_button = Button(self.tabs_container,
                                  text="主题和特色功能",
                                  # command=self.show_main_settings,
                                  width=0,  # 宽度自动填充  # 指定固定高度
                                  # Style_all=f'Custom.TButton'
                                  )  # 背景色与窗口背景色一致

        self.name_button = Button(self.tabs_container,
                                  text="点名器名单",
                                  # command=self.show_name_settings,
                                  width=0,  # 宽度自动填充 # 指定固定高度
                                  style=f'Custom.TButton')  # 背景色与窗口背景色一致

        self.display_button = Button(self.tabs_container,
                                     text="显示设置",
                                     # command=self.show_display_settings,
                                     width=0,  # 宽度自动填充 # 指定固定高度
                                     style=f'Custom.TButton',
                                     )

        # self.about_label = Label(self.tabs_container, text="关于NameProject", width=0)

        # self.about_button = Button(self.tabs_container,
        #                            text="关于NameProject",
        #                            command=self.show_about_settings,
        #                            width=0,  # 宽度自动填充 # 指定固定高度
        #                            style=f'Custom.TButton'
        #                            )

        # 需要在初始化样式时定义Custom.TButton的背景色
        self.style.configure('Custom.TButton', background=background_color)
        self.title_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.main_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.name_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.display_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        # self.about_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        # self.about_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.paned_window.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

        # 初始化显示系统设置
        self.show_hello_settings()

        self.mainloop()

    def show_hello_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        self.main_settings_0 = Frame(self.settings_container, padding=10)

        Label(self.main_settings_0, text="欢迎使用NameProject点名器！", font=("微软雅黑", 25)).pack(pady=10,
                                                                                                     anchor="center")
        Label(self.main_settings_0, text="点击'下一步'开始配置点名器", font=("微软雅黑", 12)).pack(pady=10, anchor="center")

        Button(self.main_settings_0, text="下一步", command=self.show_main_settings).pack(pady=10, anchor="e", side="bottom")

        Label(self.main_settings_0, text="注意注意！继续安装即表示您同意Apache Version 2.0开源许可证！", font=("微软雅黑", 12)).pack(pady=10, anchor="center", side="top")

        self.main_settings_0.pack(fill=tk.BOTH, expand=True)

        self.current_tab_content = self.main_settings_0

    def show_main_settings(self):

        globalConfigurePreFile = self.globalConfigurePreFile

        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        # 第一个Frame
        self.main_settings_1 = Frame(self.settings_container, padding=10)

        # Label(self.main_settings_1, text="主要设置", font=("微软雅黑", 20)).pack(pady=10, anchor="w")
        # Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(10, 5))

        Label(self.main_settings_1, text="主题设置", font=("微软雅黑", 20)).pack(pady=(10, 5), anchor="w")
        Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        Label(self.main_settings_1, text="在下方的列表中选择一个主题，你要不知道选啥，默认就行...", font=("微软雅黑", 10)).pack(pady=1, anchor="w")
        # Label(self.main_settings_1, text="由ttkbootstrap提供主题，", font=("微软雅黑", 10)).pack(pady=1, anchor="w")
        self.styleCombobox = Combobox(self.main_settings_1,
                                      values=["------浅色主题------", "cosmo", "flatly", "journal", "litera", "lumen",
                                              "minty", "pulse", "sandstone", "united", "yeti", "simplex",
                                              "------深色主题------", "solar", "superhero", "darkly", "cyborg"],
                                      font=("微软雅黑", 10), state="readonly")

        try:
            self.styleCombobox.current(Style_all["light"][globalConfigurePreFile["uiBasicSittings"]["style"]])
        except KeyError:
            self.styleCombobox.current(Style_all["dark"][globalConfigurePreFile["uiBasicSittings"]["style"]])

        self.styleCombobox.pack(pady=(5, 5), anchor="w")

        # Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(10, 5))

        Label(self.main_settings_1, text="特色功能设置", font=("微软雅黑", 20)).pack(pady=(10, 5), anchor="w")

        Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # 显示问候语
        setHelloFrame = Frame(self.main_settings_1)
        setHelloFrame.pack(pady=5, anchor="w", fill="x")

        # 创建读取变量
        self.setHelloBlVar = tkinter.BooleanVar()
        self.setHelloBlVar.set(self.globalConfigurePreFile["other"]["showHello"])

        Label(setHelloFrame, text="显示问候语", font=("微软雅黑", 15)).pack(side=tk.LEFT)
        setHelloButton = Checkbutton(setHelloFrame, bootstyle="success-round-toggle", variable=self.setHelloBlVar)
        Label(self.main_settings_1, text="在启动程序时向您展示结合网络热梗问候语").pack(anchor="w")

        setHelloButton.pack(side=tk.RIGHT)

        Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=3)

        # 添加随机事件
        setRandomEventFrame = Frame(self.main_settings_1)
        setRandomEventFrame.pack(pady=5, anchor="w", fill="x")

        self.setRandomEventBlVar = tkinter.BooleanVar()
        self.setRandomEventBlVar.set(self.globalConfigurePreFile["other"]["doRandom"])

        Label(setRandomEventFrame, text="添加随机事件", font=("微软雅黑", 15)).pack(side=tk.LEFT)

        setRandomEventButton = Checkbutton(setRandomEventFrame, bootstyle="success-round-toggle",
                                           variable=self.setRandomEventBlVar)
        setRandomEventButton.pack(side=tk.RIGHT)

        Label(self.main_settings_1, text="为您在点名过程中添加随机事件，提升您的课堂氛围").pack(anchor="w")

        Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=3)

        # 置顶窗口
        setTopFrame = Frame(self.main_settings_1)
        setTopFrame.pack(pady=5, anchor="w", fill="x")

        Label(setTopFrame, text="置顶窗口", font=("微软雅黑", 15)).pack(side=tk.LEFT)

        self.setTopBlVar = tkinter.BooleanVar()
        self.setTopBlVar.set(self.globalConfigurePreFile["other"]["topMost"])

        setTopButton = Checkbutton(setTopFrame, bootstyle="success-round-toggle", variable=self.setTopBlVar)
        setTopButton.pack(side=tk.RIGHT)

        Label(self.main_settings_1, text="在程序运行时，窗口置顶，方便您随时查看点名结果",
              font=("微软雅黑", 10)).pack(anchor="w")

        Separator(self.main_settings_1, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=3)

        # 立即停止抽取
        self.stopNowFrame = Frame(self.main_settings_1)
        self.stopNowFrame.pack(pady=5, anchor="w", fill="x")

        self.stopNowBlVar = tkinter.BooleanVar()
        self.stopNowBlVar.set(self.globalConfigurePreFile["stopNow"])

        Label(self.stopNowFrame, text="立即停止抽取", font=("微软雅黑", 15)).pack(side=tk.LEFT)

        self.stopNowButton = Checkbutton(self.stopNowFrame, bootstyle="success-round-toggle",
                                         variable=self.stopNowBlVar)
        self.stopNowButton.pack(side=tk.RIGHT)
        Label(self.main_settings_1, text="在用户按下“停止抽取”按钮后立即停止抽取，不依靠惯性滚动",
              font=("微软雅黑", 10)).pack(anchor="w")

        self.applyChangeButton = Button(self.main_settings_1, text="下一步", command=self.mainApplyChangeButtonFunc)
        self.applyChangeButton.pack(pady=5, anchor="e", side="bottom")

        self.main_settings_1.pack(fill='both', expand=True)
        self.current_tab_content = self.main_settings_1

        # 检查设置是否正确
        self.checkSittingsIsCurrect()

    def mainApplyChangeButtonFunc(self):
        # 备份全局配置文件

        if messagebox.askquestion("提示", "确定就这样了吗？") == "yes":
            # 应用用户更改
            self.globalConfigurePreFile["other"]["doRandom"] = self.setRandomEventBlVar.get()
            self.globalConfigurePreFile["other"]["showHello"] = self.setHelloBlVar.get()
            self.globalConfigurePreFile["other"]["topMost"] = self.setTopBlVar.get()
            self.globalConfigurePreFile["stopNow"] = self.stopNowBlVar.get()

            self.globalConfigurePreFile["uiBasicSittings"]["style"] = self.styleCombobox.get()

            self.main_button.configure(bootstyle="success", text="已完成！")
            self.show_name_settings()

        # try:
        #     self.change_json_file(globalConfigurePreFile)
        #     self.style = Style(theme=self.globalConfigurePreFile["uiBasicSittings"]["style"])
        #     messagebox.showinfo("成功", "更改已保存，重启软件以生效更改")
        # except:
        #     messagebox.showerror("错误", "无法保存更改，请检查文件是否被占用或者其他问题\n" + traceback.format_exc())

    def show_name_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        self.name_settings = Frame(self.settings_container, padding=10)

        # 使用默认字体
        Label(self.name_settings, text="设置点名器名单", font=("微软雅黑", 20)).pack(pady=10, anchor="w")
        Separator(self.name_settings, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(10, 5))
        Label(self.name_settings, text="点击下面的文本框，开始输入学生姓名[至少需要5位同学的姓名]。\n注意：一个学生姓名为一行", wraplength=400).pack(anchor="w",
                                                                                                             pady=5)

        # 设置Text控件的最大显示行数（例如10行）
        max_rows = 10
        self.nameTexter = tk.Text(self.name_settings, width=20, height=max_rows, font=("微软雅黑", 20))

        # for i in self.namelabel:
        #     self.nameTexter.insert("insert", i + "\n")

        # 添加滚动条并与Text控件紧密结合
        scrollbary = tk.Scrollbar(self.name_settings, orient=tk.VERTICAL, command=self.nameTexter.yview)
        self.nameTexter['yscrollcommand'] = scrollbary.set

        self.apply_change_button = Button(self.name_settings, text="下一步", command=self.apply_change_button_func)

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

        self.globalConfigurePreFile["nameLabel"].clear()
        for i in get:
            self.globalConfigurePreFile["nameLabel"].append(i)

        self.globalConfigurePreFile["nameLabel"] = list(filter(None, self.globalConfigurePreFile["nameLabel"]))

        if len(self.globalConfigurePreFile["nameLabel"]) < 5:
            messagebox.showerror("错误", "点名器名单至少需要5个学生，请检查输入")
            return
        else:
            if messagebox.askquestion("注意", "确认就是这些学生了吗？") == "yes":
                self.name_button.configure(bootstyle="success", text="又完成一个！")
                self.show_display_settings()

        print(self.globalConfigurePreFile["nameLabel"])


        # try:
        #     self.change_json_file(globalConfigFile)
        #     tkinter.messagebox.showinfo("成功", "点名器名称已被修改！")
        # except Exception as e:
        #     messagebox.showerror("我们在执行‘应用更改时’发生了错误",
        #                          "原因未知，你可以在下面的TraceBack中获取详情信息\n\n" + traceback.format_exc())

    def show_display_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        self.displaySittings = Frame(self.settings_container, padding=10)

        Label(self.displaySittings, text="字体设置", font=("微软雅黑", 20)).pack(pady=10, anchor="w")
        Separator(self.displaySittings, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 5))
        Label(self.displaySittings, text="请通过滑块调整需要增加的字体大小，上限为20，下限为-20").pack(pady=10,
                                                                                                     anchor="w")
        Label(self.displaySittings, text="如果你不确定怎么调整字体大小，默认即可，反正又不是只能设置一次").pack(pady=10,
                                                                                                     anchor="w")

        self.showWhere = Label(self.displaySittings, text="当前值为：{}".format("null"))
        self.showWhere.pack(pady=10, anchor="w")

        self.scale = Scale(self.displaySittings, from_=-20, to=20, orient=tk.HORIZONTAL)
        self.scale.set(self.globalConfigurePreFile["fontScaleSize"])
        self.scale.pack(fill=tk.X)

        Label(self.displaySittings, text="注意：‘设置’中的字体不受此处设置影响", foreground="red").pack(pady=10,
                                                                                                       anchor="w")

        self.displaySittings.pack(fill=tk.BOTH, expand=True)

        Button(self.displaySittings, text="完成设置", command=self.displayApplyChangeButtonFunc).pack(side="bottom",
                                                                                                      anchor="e")

        self.checkDisplaySittings()

        self.current_tab_content = self.displaySittings

    def displayApplyChangeButtonFunc(self):
        final = int(self.scale.get())
        if messagebox.askquestion("注意", "确认修改字体大小为：{}，确定了吗？".format(final)) == "yes":
            self.display_button.configure(bootstyle="success", text="准备就绪！")
            self.globalConfigurePreFile["fontScaleSize"] = final
            self.write_config_file()

    def write_config_file(self):
        try:
            with open("configure.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(self.globalConfigurePreFile, ensure_ascii=False))

            self.end_setup()

        except:
            messagebox.showerror("我们在执行‘应用更改时’发生了错误",
                                  "原因未知，你可以在下面的TraceBack中获取详情信息\n\n" + traceback.format_exc())

    def checkDisplaySittings(self):
        self.showWhere.configure(text="当前值为：{}".format(int(self.scale.get())))

        globalConfigurePreFile = self.globalConfigurePreFile

        self.after(100, self.checkDisplaySittings)
    def checkSittingsIsCurrect(self):
        if self.styleCombobox.get() == "------浅色主题------" or self.styleCombobox.get() == "------深色主题------":
            self.applyChangeButton.configure(state="disabled", text="不可用，因为主题选择错误")

        else:
            self.applyChangeButton.configure(state="normal", text="应用更改")

        self.after(100, self.checkSittingsIsCurrect)

    def end_setup(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()

        self.endSittingsFrame = Frame(self.settings_container, padding=10)

        Label(self.endSittingsFrame, text="一切准备就绪！", font=("微软雅黑", 20)).pack(pady=10, anchor="center")
        Separator(self.endSittingsFrame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(5, 5))
        Label(self.endSittingsFrame, text="软件设置完成！请点击完成按钮关闭此安装界面，\n请重新点击启动NameProject，让我用全新的姿态拥护你的体验！", font=("微软雅黑", 12)).pack(pady=10, anchor="center")

        Button(self.endSittingsFrame, text="完成", command=self.exit_window).pack(side="bottom", anchor="e")

        self.endSittingsFrame.pack(fill=tk.BOTH, expand=True)
        self.current_tab_content = self.endSittingsFrame

    def exit_window(self):
        self.destroy()

def openWelcomeUI():
    welcomeUI(modeConfigFile=configureFile)


if __name__ == '__main__':
    welcomeUI(modeConfigFile=configureFile)
