import tkinter
import tkinter.ttk
import tkinter.messagebox
import json

# 配置文件模板
# 请不要更改里面的内容，不然主程序会寄
configureFile = {
    "configVersion": "3.0",
    "eula": False,
    "geometry": "",
    "nameLabel": [],
    "other": {
        "doRandom": False,
        "showHello": False,
        "topMost": False
    },
    "uiBasicSittings": {
        "style": "cosmo"  # 默认ttkbootstrap样式
    },
    "fontSize": {
        "maintitle": 50,
        "mainNameLabel": 55,
        "preNameLabel": 35,
        "afterNameLabel": 35,
        "mainButton": 9,
        "mainStopButton": 9
    }
}


class setupUI_1(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("点名器安装和配置程序")
        # self.geometry(f"800x600+{int(self.winfo_screenwidth() / 2)}+{int(self.winfo_screenheight() / 2)}")
        tkinter.Label(self, text="欢迎使用NameProject安装和配置程序！", font=("simhei", 20)).pack()
        tkinter.Label(self, text="安装和配置程序将会为您引导您完成下一步的配置，").pack()
        tkinter.Label(self, text="请点击'下一步'继续").pack()

        tkinter.Button(self, text="下一步", relief=tkinter.GROOVE, command=self.nextStep).pack(side="bottom")

        self.mainloop()

    def nextStep(self):
        self.destroy()
        setupUI_2()


class setupUI_2(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("点名器安装和配置程序")
        tkinter.Label(self, text="开源软件用户许可和软件协议", font=("simhei", 20)).pack()
        tkinter.Label(self, text="请认真阅读以下文字，继续使用此软件即表示您同意此协议").pack()
        self.texter = tkinter.Text(self, width=80, height=10)
        self.texter.tag_configure("center", justify="center")
        with open("LICENSE", "r", encoding="utf-8") as f:
            self.texter.insert("0.0", f.read())
        self.texter.window_create(tkinter.INSERT,
                                  window=tkinter.Button(self.texter, text="我同意此用户协议", relief=tkinter.GROOVE,
                                                        command=self.nextSetup))
        self.texter.configure(state=tkinter.DISABLED)
        self.texter.pack()
        self.mainloop()

    def nextSetup(self):
        global configureFile
        configureFile["eula"] = True
        self.destroy()
        setupUI_3()


class setupUI_3(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("点名器安装和配置程序")
        tkinter.Label(self, text="导入学生/员工姓名", font=("simhei", 20)).pack()
        tkinter.Label(text="请在下面的文本框中输入学生/员工的姓名，以便完成接下来的设置").pack()
        tkinter.Label(text="注意：每一行为一个学生或员工姓名，设置完成后请点击'下一步'继续。").pack()

        self.nameTexter = tkinter.Text(self, width=25, height=12)
        self.nameTexter.configure(font=("simkai", 25))

        self.nameTexter.pack()
        tkinter.Button(self, text="下一步", command=self.nextStep, relief=tkinter.GROOVE).pack(side="bottom")
        self.mainloop()

    def nextStep(self):
        global configureFile
        showInName = self.nameTexter.get('0.0', tkinter.END).split("\n")
        showInMessageboxName = ""

        for i in range(len(showInName)):
            if showInName[i] == "":
                del showInName[i]
                continue

        for i in range(3):
            showInMessageboxName += showInName[i] + "\n"
        showInMessageboxName += "..."
        if tkinter.messagebox.askquestion("确认姓名？", showInMessageboxName + "\n等 {} 位学生/员工".format(
                len(showInName))) == 'yes':
            for i in showInName:
                configureFile["nameLabel"].append(i)
            print(configureFile)
            self.destroy()
            setupUI_4()


class setupUI_4(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("点名器安装和配置程序")
        tkinter.Label(self, text="功能性配置和其他设置", font=("simhei", 20)).pack()
        tkinter.Label(self, text="配置其他的功能和设置\n设置完成后，点击'完成配置'。\n").pack()

        self.setFun = tkinter.IntVar()
        self.setFun.set(1)
        tkinter.ttk.Checkbutton(self, text="增加随机事件", variable=self.setFun).pack(side="top")
        tkinter.Label(self,
                      text="'随机事件'可以在点名过程中随机触发一些特定事件，让您的课堂或者会议更加轻松愉快，不过需要演讲者有一定的准备。\n",
                      justify="left").pack(side="top")

        self.setHello = tkinter.IntVar()
        self.setHello.set(1)
        tkinter.ttk.Checkbutton(self, text="增加问候语", variable=self.setHello).pack(side="top")
        tkinter.Label(self, text="该功能开启后，会在打开此软件时显示问候语。\n").pack()

        self.setTop = tkinter.IntVar()
        tkinter.ttk.Checkbutton(self, text="置顶窗口", variable=self.setTop).pack(side="top")
        tkinter.Label(self, text="将窗口置顶在桌面，以方便在使用PPT等场景下无需切换程序使用。\n").pack()

        # tkinter.Label(self,
        #               text="设置完成后，请点击'开始测试'按钮，测试软件是否正常运行。\n您也可以更改窗口大小至合适的大小，程序会保存您的设置。").pack()
        # tkinter.Button(self, text="    开始测试    ", relief=tkinter.GROOVE, command=self.testAction).pack()
        tkinter.Label(self).pack()
        tkinter.Button(self, text="    完成配置    ", relief=tkinter.GROOVE, command=self.nextStep).pack(side="bottom")

        self.mainloop()

    # def testAction(self):
    #    source.maingui(studentName=configureFile["nameLabel"], debugMode=True)

    def nextStep(self):
        global configureFile
        config = []
        for i in [self.setFun.get(), self.setHello.get(), self.setTop.get()]:
            if i == 1:
                config.append(True)
            else:
                config.append(False)

        configureFile["other"]["doRandom"] = config[0]
        configureFile["other"]["showHello"] = config[1]
        configureFile["other"]["topMost"] = config[2]

        print(configureFile)
        print(config)

        with open("configure.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(configureFile, ensure_ascii=False))

        tkinter.messagebox.showinfo("完成！", "您已完成配置工作，再次运行此文件时即可使用主程序！")

        self.destroy()


if __name__ == '__main__':
    setupUI_1()
