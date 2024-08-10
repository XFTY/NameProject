#! /usr/bin/env python3
# --------------------------------------------------------------------------------------------------
# | 版权所有 XFTY，保留所有权利。
# | 代码遵循Apache 2.0开源协议，浏览在根目录的LICENSE文件以获取更多信息。
# |
# | Copyright (c) 2021-2022 XFTY, All Rights Reserved.
# | Licensed under the Apache License 2.0. See LICENSE in the project root for license information.
# --------------------------------------------------------------------------------------------------
# sourceQt.py 主要负责处理项目逻辑
import os

os.system("pip install -r requirements.txt")

import sys
import random
import json
import time
import threading
import webbrowser

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from BlurWindow.blurWindow import GlobalBlur

import basic

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


class sourceQt(QMainWindow):
    fade_finished = pyqtSignal()
    def __init__(self, parent=None):
        # 基本设置
        super(sourceQt, self).__init__(parent)
        self.ui = basic.Ui_MainWindow()
        self.ui.setupUi(self)
        GlobalBlur(self.winId(), Dark=True, QWidget=self)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        QMainWindow.setWindowOpacity(self, 0.0)


        # 通过读取windowShowing可以知道目前哪个widget在显示
        self.windowShowing = None

        #窗口大小
        self.resize(900, 550)

        # 窗口列表
        self.wedgitList = [
            self.ui.classicWidget,
            self.ui.TestWidget
        ]

        # 隐藏所有的窗口
        for i in self.wedgitList:
            i.hide()

        # 在不破坏按钮原有样式的基础上设置窗口背景
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgba(0, 0, 0, 0);
            }
            QMenuBar {
                background-color: rgba(0, 0, 0, 0);
                color: #FFFFFF;
            }
            QMenu {
                background-color: rgba(0, 0, 0, 0);
                color: #FFFFFF;
            }
            QMenu:hover {
                background-color: #444444;  /* 鼠标悬停时的背景颜色 */
            }
            QMenu:pressed {
                background-color: #222222;  /* 按下时的背景颜色 */
            }
            QPushButton {
                color: #FFFFFF;  /* 文本颜色 */
                background-color: rgba(0, 0, 0, 0);  /* 背景颜色 */
                border: 1px solid #555555;  /* 边框宽度和颜色 */
                border-radius: 8px;  /* 设置圆角半径，可以根据需要调整 */
                padding: 5px 10px;  /* 内边距，决定文字与边框的距离 */
                font-size: 14px;  /* 字体大小 */
                outline: none;  /* 去除焦点时的外边框 */
            }
            QPushButton:hover {
                background-color: #444444;  /* 鼠标悬停时的背景颜色 */
            }
            QPushButton:pressed {
                background-color: #222222;  /* 按下时的背景颜色 */
            }
            QPushButton:disabled {
                color: grey;
            }
            QLabel {
                color: #FFFFFF;
            }
        """)

        # 显示默认窗口
        # 手动触发showClassicalUi函数
        self.showClassicalUi()

        # 窗口居中显示
        self.center_on_screen()

        # 连接菜单槽函数
        self.ui.classicalMode.triggered.connect(self.showClassicalUi)
        self.ui.sittingMode.triggered.connect(self.showTestUi)
        # 按钮函数绑定
        self.ui.startButton.clicked.connect(self.onPreButtonClick)
        self.ui.endButton.clicked.connect(self.onEndButtonClick)
        self.ui.closeButton.clicked.connect(self.exit)
        self.ui.smallistButton.clicked.connect(self.showMaximizedWindow)


        # 禁用self.ui.endButton
        self.ui.endButton.setEnabled(False)

        # 读取json文件
        with open("configure.json", "r", encoding="utf-8") as f:
            self.configureFile = json.loads(f.read())

        # 设置要用到的变量
        self.studentName = self.configureFile["nameLabel"]
        self.doRandom = self.configureFile["other"]["doRandom"]
        self.stopNow = self.configureFile["stopNow"]

        # 第一次使用变量
        self.f = True

        # 淡入
        t = threading.Thread(target=self.throwIn, args=())
        t.start()

    def center_on_screen(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.frameGeometry()
        margin = QMargins(50, 50, 50, 50)  # 边缘留出50像素的空白
        x = int((screen.width() - size.width()) / 2) + margin.left()
        y = int((screen.height() - size.height()) / 2) + margin.top()
        self.move(x, y)

    def onPreButtonClick(self):
        self.ui.startButton.setEnabled(False)
        self.ui.endButton.setEnabled(True)
        self.buttonStatus = True
        t = threading.Thread(target=self.__flushUI, args=())
        t.start()

    def onEndButtonClick(self):
        self.ui.endButton.setEnabled(False)
        self.buttonStatus = False

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

        self.ui.Title.setText("姓名滚动方向>>>>>>")

        # 无限循环，直到触发特定事件才退出
        while True:
            # 检测是否需要退出程序
            # if self.closeThread:
            #     self.exit()

            # 遍历姓名列表，逐个显示姓名
            for i in range(1, len(self.studentName) - 1):
                self.preName = self.studentName[i - 1]
                self.mainName = self.studentName[i]
                self.afterName = self.studentName[i + 1]
                self.ui.preNameLabel.setText(self.preName)
                self.ui.centerNameLabel.setText(self.mainName)
                self.ui.afterNameLabel.setText(self.afterName)
                time.sleep(o)

                # 如果按钮处于激活状态，则不进行下面的操作
                if not self.buttonStatus:
                    if self.stopNow:
                        self.handle_random_event()
                        return 0
                    else:
                        o += 0.05  # 增加时间间隔
                        self.ui.Title.setText("{}".format(stt))  # 更新标题
                        # self.mainButton.configure(state="disabled")  # 禁用主按钮

                    # 当时间间隔超过x时，触发随机事件，并结束当前循环
                    # 话说为什么，注释掉下面6行代码程序会抽风？因为我的电脑？
                    if self.stopNow:
                        self.handle_random_event()
                        return 0
                    elif o > x:
                        self.handle_random_event()
                        return 0

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
        self.ui.Title.setText("站讲台上的那位！")
        self.ui.preNameLabel.setText("***")
        self.ui.centerNameLabel.setText("站讲台上的那位！")
        self.ui.afterNameLabel.setText("***")
        self.ui.Title.setStyleSheet("color: green;font: 25pt \"Microsoft YaHei UI\";")
        time.sleep(3 * 0.5)
        self.reset_title_and_button()

    def handle_special_event_2(self):
        self.ui.Title.setText(text="原神，启动！")
        self.ui.preNameLabel.setText(text="***")
        self.ui.centerNameLabel.setText(text="原神，启动！！")
        self.ui.afterNameLabel.setText(text="***")
        self.ui.Title.setStyleSheet("color: green;font: 25pt \"Microsoft YaHei UI\";")
        time.sleep(3 * 0.5)
        webbrowser.open_new(
            "https://ys-api.mihoyo.com/event/download_porter/link/ys_cn/official/pc_default"
        )
        self.reset_title_and_button()

    def handle_normal_event(self):
        self.ui.Title.setText("就是你啦，{}!".format(self.mainName))
        self.ui.Title.setStyleSheet("color: lightgreen;font: 25 20pt \"Microsoft YaHei UI\";")
        time.sleep(0.5 * 3)
        self.reset_title_and_button()
        if not self.buttonStatus:
            needSetText = False
        else:
            needSetText = True
        time.sleep(5)
        if needSetText or not self.buttonStatus:
            self.ui.Title.setText("NameProject")

    def reset_title_and_button(self):
        self.ui.startButton.setEnabled(True)
        self.ui.endButton.setEnabled(False)
        self.ui.Title.setStyleSheet("color: white;font: 25 20pt \"Microsoft YaHei UI\";")
        # self.mainButton.configure(state="normal")

    def exit(self):
        t = threading.Thread(target=self.throwOut, args=())
        t.start()

    def showMaximizedWindow(self):
        self.showMinimized()

    def throwOut(self):
        t = threading.Thread(target=self.fadeOut)
        t.start()

    def fadeOut(self):
        a = 1.0
        speed_factor = 1  # 初始化速度因子
        speed_increase_interval = 0.05  # 每隔多久加速一次的间隔（秒）
        current_time = 0  # 当前已过去的时间
        start_time = time.time()  # 记录开始时间

        while a > 0.0:
            QMainWindow.setWindowOpacity(self, a)
            # 根据当前时间和速度增加间隔来调整透明度减少的速度
            if current_time - start_time >= speed_increase_interval:
                speed_factor += 0.05  # 每隔一定时间增加速度因子
                start_time = time.time()  # 重置开始时间
            a -= 0.05 * speed_factor  # 透明度减小的量乘以速度因子
            time.sleep(0.05)
            current_time = time.time()  # 更新当前时间

        # 动画结束后发送信号
        self.fade_finished.emit()
        QApplication.quit()



    def windowCloseHandler(self):
        QApplication.quit()

    def throwIn(self):
        t = threading.Thread(target=self.fadeIn)
        t.start()

    def fadeIn(self):
        a = 0.0
        step_size = 0.1  # 初始递增步长
        min_step_size = 0.001  # 最小递增步长
        max_opacity = 0.95  # 设置一个较大的不透明度阈值，比如0.95，以确保完全不透明
        while a < max_opacity:
            QMainWindow.setWindowOpacity(self, a)
            if step_size > min_step_size:
                step_size *= 0.95  # 每次迭代后减小步长
            a += step_size
            time.sleep(min(step_size, 0.05))

    def windowClosed(self):
        QApplication.quit()


    def showClassicalUi(self):
        if self.windowShowing is not None:
            self.windowShowing.hide()

        self.ui.classicWidget.show()

        self.windowShowing = self.ui.classicWidget

    def showTestUi(self):
        if self.windowShowing is not None:
            self.windowShowing.hide()

        self.ui.TestWidget.show()

        self.windowShowing = self.ui.TestWidget

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = sourceQt()
    main.show()
    sys.exit(app.exec_())
