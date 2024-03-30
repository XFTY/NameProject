import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from tkinter import *

# 先创建一个无边框窗口，以便取消原生标题栏
root = tk.Tk()
root.overrideredirect(True)  # 取消原生标题栏

# 创建一个函数来模拟原生标题栏的拖动功能
def on_configure(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')  # 根据鼠标位置移动窗口

# 创建自定义标题栏
custom_title_bar = Frame(root, bg='brown', relief='raised', bd=2)
custom_title_bar.pack(fill='x', side=tk.TOP)

# 在标题栏上添加窗口标题和关闭按钮
title_label = Label(custom_title_bar, text="点名器设置程序", font=('Arial', 14), bg='white')
title_label.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

close_button = ttk.Button(custom_title_bar, text="X", command=root.quit)
close_button.pack(side=tk.RIGHT)

# 绑定鼠标的左键按下事件，以便拖动窗口
custom_title_bar.bind('<ButtonPress-1>', lambda event: root.event_generate("<Configure>", x=event.x_root, y=event.y_root))
custom_title_bar.bind('<B1-Motion>', on_configure)

# ... (其他你的代码部分保持不变)

# 启动主循环
root.mainloop()