#! /usr/bin/env python3
# --------------------------------------------------------------------------------------------------
# | 版权所有 XFTY，保留所有权利。
# | 代码遵循Apache 2.0开源协议，浏览在根目录的LICENSE文件以获取更多信息。
# |
# | Copyright (c) 2021-2022 XFTY, All Rights Reserved.
# | Licensed under the Apache License 2.0. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------------

from tkinter import Tk
import sys
if sys.version_info[0] < 3:
    raise Exception("Python 3 or later is required")
import clr
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Threading')
from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart

url = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>开源随机点名器 - 简洁高效、免费使用</title>
    <!-- 链入自定义CSS文件 -->
    <link rel="stylesheet" href="styles.css">

    <!-- 引入开源库或框架（例如Bootstrap）时需添加相应链接 -->
    <!-- ... -->

    <!-- 开源许可信息 -->
    <meta name="author" content="XFTY">
    <meta name="license" content="Apache-License">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <!-- 项目LOGO及标题区 -->
    <header class="header">
        <!--<div class="logo-container">
            <img src="open-source-logo.png" alt="开源随机点名器Logo">
        </div>-->
        <h1>NameProject 随机点名器</h1>
        <p>一个适用于班级、社区、公司点名的 公平高效 解决方案。</p>
        <div class="btn-container-padding">
        <div>
            <a href="https://github.com/XFTY/NameProject/releases" class="gradient-btn">下载最新版</a>
            <!--<a href="https://github.com/yourteam/random-name-picker/wiki" target="_blank" class="gradient-btn">用户手册与API文档</a>-->
        </div>
    </header>

    <section id="screenshots">
        <div class="feature-card">
            <h1>软件截图</h1>
            <div class="screenshot-container">
                <img src="web_image/index/319426818-46a8213f-840a-44af-8734-bc6987dd45c1.png" alt="Screenshot 1">
            </div>
           <!-- <div class="screenshot-container">
                <img src="web_image/index/319427066-2c124884-4a23-4360-9219-a34ffcc7d754.png" alt="Screenshot 2">
            </div> -->
        </div>
    </section>


    <!-- 项目介绍 -->
    <section id="features">
        <div class="feature-card">
            <h1>为什么选择NameProject？</h1>
            <div class="feature-item">
                <i class="fas fa-code"></i>
                <h2>软件开源</h2>
                <p>NameProject是开源的，使用python语言编写，任何人可以参考软件源代码。</p>
            </div>

            <div class="feature-item">
                <i class="fas fa-user-friends"></i>
                <h2>易用性强</h2>
                <p>简单直观的操作界面，支持一键导入名单进行随机点名。</p>
                <!--<img src="interface-screenshot.jpg" alt="用户界面截图">-->
            </div>

            <div class="feature-item">
                <i class="fas fa-globe-americas"></i>
                <h2>活跃氛围</h2>
                <p>通过设定好的一些随机事件，你可以以一种更加轻松愉悦的方式点名。</p>
            </div>

            <div class="feature-item">
                <i class="fas fa-globe-americas"></i>
                <h2>跨平台支持</h2>
                <p>支持Windows、MacOS、Linux三个主流电脑操作系统，如果你愿意，他甚至支持树莓派！</p>
            </div>
        </div>
    </section>

    <!-- 图片展示区 -->



    <!-- 使用指南与文档链接 -->
    <section id="docs" class="feature-card">
        <h2>开始使用</h2>
        <div class="btn-container">
            <a href="https://github.com/XFTY/NameProject/releases" class="gradient-btn">下载最新版</a>
            <!--<a href="https://github.com/yourteam/random-name-picker/wiki" target="_blank" class="gradient-btn">用户手册与API文档</a>-->
            <a href="https://github.com/XFTY/NameProject/issues" target="_blank" class="gradient-btn">提交问题与建议</a>
        </div>
    </section>

    <!-- 社区互动与贡献指南 -->
    <section id="community" class="feature-card">
        <h2>加入我们</h2>
        <p>欢迎加入我们的开源社区，一起讨论改进和分享经验：</p>
        <!-- 将链接改为按钮样式 -->
        <a href="https://github.com/XFTY/NameProject" class="gradient-btn" target="_blank">访问GitHub项目地址</a>
    </section>

    <!-- 底部版权声明与联系信息 -->
    <footer>
        <p>本项目遵循<a href="https://opensource.org/license/apache-2-0">Apache-License</a>开源许可协议。所有贡献者享有署名权。</p>
        <nav>
            <a href="http://github.com/XFTY/NameProject">关于项目</a>
            <a href="https://github.com/XFTY">联系我们</a>
        </nav>
    </footer>
    <script src="script.js"></script>
    </body>
</html>
"""

#范例
def main():
    if not have_runtime():#没有webview2 runtime
        install_runtime()
    root=Tk()
    root.title('pywebview for tkinter test')
    root.geometry('1200x600+5+5')

    frame2=WebView2(root,1920,1080)
    frame2.pack(side='left',padx=20,fill='both',expand=True)
    frame2.load_url("https://github.com/XFTY/NameProject/releases/latest")

    root.mainloop()

if __name__ == "__main__":
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()