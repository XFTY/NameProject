import ttkbootstrap as ttk
from ttkbootstrap.toast import ToastNotification

app = ttk.Window()

toast = ToastNotification(
    title="警告",
    message="对NameProject v1.x\n的主流支持已终止，请尽快更新至v2.x！",
    duration=None,
    bootstyle="dark",
    alert=True
)
toast.show_toast()

app.mainloop()