import tkinter
import ttkbootstrap
import ttkbootstrap.constants
import update

# 如果你正在试图通过Pycharm打开这个文件，你会发现下面的代码犹如shishan，请无视
import sys
if sys.version_info[0] < 3:
    raise Exception("Python 3 or later is required")
import clr
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')
from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart



class UpdateWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()

        # 调用update.py获取最新版
        self.response = update.getUpdateResponse()

        # 设置主题和窗口基本属性
        style = ttkbootstrap.Style(theme="darkly")
        self.title("有新的软件更新可用")
        self.geometry("1200x583")

        # 创建Panedwindow并设置其方向为垂直
        paned_window = ttkbootstrap.Panedwindow(self, orient=ttkbootstrap.constants.VERTICAL)
        paned_window.pack(fill=ttkbootstrap.constants.BOTH, expand=True)

        # 创建两个Frame并添加到Panedwindow中
        self.frame_top = ttkbootstrap.Frame(paned_window)
        # 调用updateTopFrame方法
        self.updateTopFrame()
        self.frame_bottom = ttkbootstrap.Frame(paned_window, padding=(10, 10))
        self.updateBottomeFrame()

        # 添加Frame至Panedwindow并设置各自占据的空间比例
        paned_window.add(self.frame_top, weight=80)  # 占90%
        paned_window.add(self.frame_bottom, weight=20)  # 占10%

        # 开启主循环
        self.mainloop()

    def updateTopFrame(self):
        tkinter.Label(self.frame_top, text="有新的软件更新可用：NameProject{}".format(update.getUpdateTagName(self.response)), font=("微软雅黑", 20), pady=20).pack(anchor="w")

        # text = ttkbootstrap.Text(self.frame_top, height=10, font=("微软雅黑", 13))
        # text.insert(tkinter.END, update.getUpdateInfo(self.response))
        # text.pack(fill=tkinter.X)

        self.webView2 = WebView2(self.frame_top, width=1200, height=300)
        self.webView2.load_url("https://github.com/XFTY/NameProject/releases/latest")
        self.webView2.pack()

        tkinter.Label(self.frame_top, text="点击更新按钮后，软件将自动安装更新，", font=("微软雅黑", 11), pady=10).pack(anchor="w")
        tkinter.Label(self.frame_top, text="这不需要太长的时间。", font=("微软雅黑", 11)).pack(
            anchor="w")

    def updateBottomeFrame(self):
        self.updateStatus = tkinter.Label(self.frame_bottom, text="等待用户响应", font=("微软雅黑", 11), pady=10)
        self.updateStatus.pack(pady=0, side="top", anchor="w")
        self.progressBar = ttkbootstrap.Progressbar(self.frame_bottom, bootstyle=ttkbootstrap.constants.INFO, length=500, value=100)
        self.progressBar.pack(side="top", fill="x")

        self.buttonFrame = ttkbootstrap.Frame(self.frame_bottom, padding=(0, 10, 0, 10))
        self.buttonFrame.pack(side="bottom", fill="x")

        self.updateButton = ttkbootstrap.Button(self.buttonFrame, text="现在更新", bootstyle=ttkbootstrap.constants.SUCCESS, command=self.updateButtonFunc)
        self.cancelButton = ttkbootstrap.Button(self.buttonFrame, text="取消更新", bootstyle=ttkbootstrap.constants.DANGER, command=self.destroy)
        self.updateButton.pack(side="left")
        self.cancelButton.pack(side="right")

    def updateButtonFunc(self):
        print(
            self.winfo_width(),
            self.winfo_height()
        )

if __name__ == "__main__":
    t = Thread(ThreadStart(UpdateWindow))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
