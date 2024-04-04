import json
import sys
import tkinter
from tkinter import messagebox
import traceback
from ttkbootstrap import Style
from ttkbootstrap.widgets import *


class SettingsUI(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("点名器设置")
        self.geometry("1200x600")

        self.read_json_file()

        self.style = Style(theme='darkly')
        self.current_tab_content = None

        self.paned_window = PanedWindow(orient=tk.HORIZONTAL)
        self.paned_window.pack(fill='both', expand=True)

        self.tabs_container = Frame(self.paned_window, padding=10)
        self.settings_container = Frame(self.paned_window, padding=10)

        self.paned_window.add(self.tabs_container, weight=1)
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
                                  text="点名器基本设置",
                                  command=self.show_main_settings,
                                  width=0,  # 宽度自动填充  # 指定固定高度
                                  # Style_all=f'Custom.TButton'
                                  )  # 背景色与窗口背景色一致

        self.name_button = Button(self.tabs_container,
                                  text="点名器名单",
                                  command=self.show_name_settings,
                                  width=0,  # 宽度自动填充 # 指定固定高度
                                  style=f'Custom.TButton')  # 背景色与窗口背景色一致

        self.about_label = Label(self.tabs_container, text="关于NameProject", width=0)

        # 需要在初始化样式时定义Custom.TButton的背景色
        self.style.configure('Custom.TButton', background=background_color)

        self.title_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.main_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.name_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.about_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # 初始化显示系统设置
        self.show_main_settings()
        self.mainloop()


    def show_main_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()
        self.system_settings = Frame(self.settings_container, padding=10)
        Label(self.system_settings, text="主要设置", font=("simhei", 15)).pack(pady=10, anchor="w")
        Separator(self.system_settings, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(10, 5))
        self.system_settings.pack(fill='both', expand=True)
        self.current_tab_content = self.system_settings

    def show_name_settings(self):
        if self.current_tab_content is not None:
            self.current_tab_content.pack_forget()
        self.name_settings = Frame(self.settings_container, padding=10)

        # 使用默认字体
        Label(self.name_settings, text="点名器名单", font=("simhei", 15)).pack(pady=10, anchor="w")
        Separator(self.name_settings, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(10, 5))
        Label(self.name_settings, text="在此处修改点名器名单\n注意：一个学生姓名为一行", wraplength=400).pack(anchor="w",
                                                                                                             pady=5)

        # 设置Text控件的最大显示行数（例如10行）
        max_rows = 10
        self.nameTexter = tk.Text(self.name_settings, width=20, height=max_rows, font=("simhei", 20))

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

        print(globalConfigFile)

    def read_json_file(self):
        isOpen = False
        try:
            with open("configure.json", "r", encoding="utf-8") as f:
                r = json.loads(f.read())
                self.globalConfigureFile = r
                self.namelabel = r["nameLabel"]
                isOpen = True

        except FileNotFoundError:
            messagebox.showerror("我们在执行‘读取配置文件时’发生了错误",
                                 "您的配置文件似乎丢失或损坏\n\n详情信息：\n" + traceback.format_exc())

        except Exception:  # 用于处理未知异常
            messagebox.showerror("我们在执行‘读取配置文件时’发生了错误",
                                 "原因未知，你可以在下面的TraceBack中获取详情信息\n\n" + traceback.format_exc())

        finally:
            if not isOpen:  # 前面创建了isOpen变量用于判断文件是否打开，如果打开则会判定为True，否则为False
                sys.exit()  # 这里判断isOpen是否为True，是就不执行这行代码，反则反之。

    def change_json_file(self, configFileJsonText):
        with open("configure.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(configFileJsonText, ensure_ascii=False))


if __name__ == "__main__":
    SettingsUI()
