#! /usr/bin/env python3
# --------------------------------------------------------------------------------------------------
# | 版权所有 XFTY，保留所有权利。
# | 代码遵循Apache 2.0开源协议，浏览在根目录的LICENSE文件以获取更多信息。
# |
# | Copyright (c) 2021-2022 XFTY, All Rights Reserved.
# | Licensed under the Apache License 2.0. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------------

# 通常情况下，只有开发人员测试时会把debugMode打开，一般情况下不要打开
debugMode = True

import json
import tkinter
import ttkbootstrap
import ttkbootstrap.constants
import traceback
import markdown
import requests
import time
import contextlib

# 在使用PyCharm浏览代码时，你会觉得下面的代码非常难受，建议直接跳过以免心跳过速
# 实际上，下面的代码是可以正常运行的。
import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 or later is required")
import clr
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')
from System.Windows.Forms import Control
from System.Threading import Thread, ApartmentState, ThreadStart


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
        tkinter.Label(self.frame_top,
                      text="有新的软件更新可用：NameProject{}".format(update.getUpdateTagName(self.response)),
                      font=("微软雅黑", 20), pady=20).pack(anchor="w")

        # text = ttkbootstrap.Text(self.frame_top, height=10, font=("微软雅黑", 13))
        # text.insert(tkinter.END, update.getUpdateInfo(self.response))
        # text.pack(fill=tkinter.X)
        try:
            self.webView2 = WebView2(self.frame_top, width=1200, height=300)
        except: pass

        if debugMode:
            # self.webView2.load_html(update.getUpdateInfo(self.response, True))
            try:
                self.webView2.load_url("https://xfty.github.io/NameProject/update")
                self.webView2.pack()
            except: pass
        else:
            try:
                self.webView2.load_url("https://xfty.github.io/NameProject/update")
                self.webView2.pack()
            except: pass


        tkinter.Label(self.frame_top, text="点击更新按钮后，软件将自动安装更新，", font=("微软雅黑", 11), pady=10).pack(
            anchor="w")
        tkinter.Label(self.frame_top, text="这不需要太长的时间。", font=("微软雅黑", 11)).pack(
            anchor="w")

    def updateBottomeFrame(self):
        self.updateStatus = tkinter.Label(self.frame_bottom, text="等待用户响应", font=("微软雅黑", 11), pady=10)
        self.updateStatus.pack(pady=0, side="top", anchor="w")
        self.progressBar = ttkbootstrap.Progressbar(self.frame_bottom, bootstyle=ttkbootstrap.constants.INFO,
                                                    length=500, value=100)
        self.progressBar.pack(side="top", fill="x")

        self.buttonFrame = ttkbootstrap.Frame(self.frame_bottom, padding=(0, 10, 0, 10))
        self.buttonFrame.pack(side="bottom", fill="x")

        self.updateButton = ttkbootstrap.Button(self.buttonFrame, text="现在更新",
                                                bootstyle=ttkbootstrap.constants.SUCCESS, command=self.updateButtonFunc)
        self.cancelButton = ttkbootstrap.Button(self.buttonFrame, text="取消更新",
                                                bootstyle=ttkbootstrap.constants.DANGER, command=self.destroy)
        self.updateButton.pack(side="left")
        self.cancelButton.pack(side="right")

    def updateButtonFunc(self):
        self.downloadFileWithAfter()

    def downloadFileWithAfter(self):
        t = Thread(target=self.downloadFile, args=(update.getUpdateDownloadUrl(self.response), "NameProject.7z"))
        t.start()

    def downloadFile(self, file_url, file_path):
        start_time = time.time()  # 文件开始下载时的时间
        with contextlib.closing(requests.get(file_url, stream=True, verify=False)) as response:
            chunk_size = 1024  # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 内容体总大小
            data_count = 0
            with open(file_path, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    data_count = data_count + len(data)
                    now_jd = (data_count / content_size) * 100
                    speed = data_count / 1024 / (time.time() - start_time)

                    self.updateStatus.configure(text="文件下载进度：{}%({}/{}) 文件下载速度：{}KB/s --{}".format(now_jd,data_count, content_size, speed, file_path))
                    self.progressBar.configure(value=now_jd)
                    # print("\r 文件下载进度：%d%%(%d/%d) 文件下载速度：%dKB/s - %s"
                    #       % (now_jd, data_count, content_size, speed, file_path), end=" ")

        return 0

class update:
    @staticmethod
    def getUpdateResponse():
        if debugMode:
            with open("testData/gitapi.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            try:
                url = "https://gitee.com/api/v5/repos/XFTYC/NameProject/releases/latest"
                response = requests.get(url)
                return response.json()
            except:
                print(traceback.format_exc())
                return None

    @staticmethod
    def checkUpdate(response, thisNameProjectVersion):
        if thisNameProjectVersion != response["tag_name"]:
            return True
        else:
            return False

    @staticmethod
    def getUpdateInfo(response, needmarkdown=False):
        if needmarkdown:
            body = response["body"].replace("\n", "")
            return markdown.markdown(body, extensions=['markdown.extensions.extra'])
        else:
            return response["body"]

    @staticmethod
    def getUpdateTagName(response):
        return response["tag_name"]

    @staticmethod
    def getUpdateDownloadUrl(response):
        return response["assets"][0]["browser_download_url"]


if __name__ == "__main__":
    t = Thread(ThreadStart(UpdateWindow))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()
