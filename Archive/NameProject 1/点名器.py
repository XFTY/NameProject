import random
import tkinter
import tkinter.ttk

# """
students_name = [
    "a",
    "b",
    "c",
    "d"
]
# """
'''
students_name = [
    "junker",
    "马化腾",
    "lemon"
]    
'''


class maingui(tkinter.Tk):
    def __init__(self):
        self.t = None
        self.randomIO = False
        super().__init__()
        self.title("四班专属点名器(NameProject 1.0 已修改) - Professional Edition")
        self.width = 600
        self.height = 350
        self.x_way = 10
        self.left = (self.winfo_screenwidth() - self.width) / 2
        self.top = (self.winfo_screenheight() - self.height) / 2
        self.geometry("{}x{}+{}+{}".format(int(self.width), int(self.height), int(self.left), int(self.top)))
        self.resizable(False, False)

        tkinter.Label(self, text="   ", font=("simhei", 20)).pack(side="top")
        tkinter.Label(self, text="点名器", font=("simhei", 30)).pack(side="top")

        tkinter.Label(self, text="   ", font=("simhei", 40)).pack(side="top")
        self.name = tkinter.Label(self, text="等待抽取 ...", font=("simhei", 45))
        self.name.pack(side="top")

        # tkinter.Label(self, text="注意，该版本的算法被篡改，请勿用于正式场合！", fg="red").pack(side="bottom")
        tkinter.Label(self, text="   ", font=("simhei", 20)).pack(side="bottom")
        self.button = tkinter.ttk.Button(self, text="[开始抽取]", command=self.effectRC)
        self.button.pack(side="bottom")

        self.mainloop()

    def effetBC(self):
        lit = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        random.shuffle(lit)
        print(lit)
        if lit[0] == 0:
            students_name_b = ['', '', ]  # 这里应该是写被针对同学的名单。(2024/10/5注)
            random.shuffle(students_name_b)
            self.name.config(text=students_name_b[0])
        else:
            self.name.config(text=students_name[random.randint(0, len(students_name) - 1)])

    def effectRC(self):
        self.name.config(text=students_name[random.randint(0, len(students_name) - 1)])


if __name__ == "__main__":
    maingui()
