from record import record_
from replay import replay_
from screenshot import MyCapture
import os
import time
from PIL import ImageGrab
from tkinter import messagebox, filedialog, Tk, Label, Button


# 开始截图
def buttonCaptureClick(event=None):
    # 最小化主窗口
    # root.state('icon')
    root.withdraw()
    time.sleep(0.2)
    filename = 'temp.png'
    # grab()方法默认对全屏幕进行截图
    im = ImageGrab.grab()
    im.save(filename)
    im.close()
    # 显示全屏幕截图
    w = MyCapture(root, filename)
    buttonCapture.wait_window(w.top)

    # 截图结束，恢复主窗口，并删除临时的全屏幕截图文件
    # root.state('normal')
    root.deiconify()
    os.remove(filename)


def button_record_click(event=None):
    # 最小化主窗口
    # root.state('icon')
    root.withdraw()
    im = ImageGrab.grab()
    f_list = record_()
    root.wm_attributes('-topmost', 1)
    messagebox.showinfo(title='提示', message='录制完成！')
    default_save_filename = 'record' + time.strftime("%Y%m%d%H%M%S") + '.txt'
    filename = filedialog.asksaveasfilename(title='保存录制脚本文件', initialfile=default_save_filename, filetypes=[("text", ".txt")])
    if filename:
        im.save(filename.split('.')[0] + '_录制开始时的截图.png')
        with open(filename, 'a') as f:
            f.writelines(f_list)
    # 恢复主窗口
    # root.state('normal')
    root.deiconify()

def button_record_p_r_click(event=None):
    # 最小化主窗口
    # root.state('icon')
    root.withdraw()
    filename = filedialog.askopenfilename(title='打开继续录制文件', filetypes=[('text', '*.txt'), ('All Files', '*')])
    if filename:
        # 屏蔽记录鼠标双击选择的第二下release
        time.sleep(0.1)
        file_list_resume = record_()
        with open(filename, 'a') as f:
            f.writelines(file_list_resume)
        root.wm_attributes('-topmost', 1)
        messagebox.showinfo(title='提示', message='录制完成！')
    root.wm_attributes('-topmost', 1)
    # 恢复主窗口
    # root.state('normal')
    root.deiconify()


def button_replay_click(event=None):
    # 最小化主窗口
    # root.state('icon')
    root.withdraw()
    filename = filedialog.askopenfilename(title='打开回放文件', filetypes=[('text', '*.txt'), ('All Files', '*')])
    if filename:
        result = replay_(filename)
        if result == 'replay_complete':
            root.wm_attributes('-topmost', 1)
            messagebox.showinfo(title='提示', message='回放完成！')
        else:
            root.wm_attributes('-topmost', 1)
            messagebox.showinfo(title='提示', message='回放中断！')
    root.wm_attributes('-topmost', 1)
    # 恢复主窗口
    # root.state('normal')
    root.deiconify()

if __name__ == '__main__':
    root = Tk()
    root.title('录制回放工具')
    # 设置窗口大小与位置
    root.geometry('500x120+400+300')
    # 设置窗口大小不可改变
    root.resizable(False, False)
    # root.attributes("-toolwindow", 1)
    # root.wm_attributes('-topmost', 1)
    label1 = Label(root, text="1、点击录制即可开始录制，期间记录所有鼠标点击和键盘操作，按Esc键退出录制", anchor="w")
    label1.place(x=10, y=20, width=500, height=20, anchor="w")
    label2 = Label(root, text="2、回放期间可以按Esc键中断", anchor="w")
    label2.place(x=10, y=40, width=200, height=20, anchor="w")
    label3 = Label(root, text="3、对应四个按钮的快捷键分别对应为ctrl+1,2,3,4", anchor="w")
    label3.place(x=10, y=60, width=300, height=20, anchor="w")
    button_record = Button(root, text='录制', command=button_record_click)
    button_record.place(x=10, y=80, width=100, height=20)
    button_record.bind_all('<Control-Key-1>', button_record_click)

    button_record_pr = Button(root, text='继续上一次录制', command=button_record_p_r_click)
    button_record_pr.place(x=130, y=80, width=100, height=20)
    button_record_pr.bind_all('<Control-Key-2>', button_record_p_r_click)

    button_replay = Button(root, text='回放', command=button_replay_click)
    button_replay.place(x=250, y=80, width=100, height=20)
    button_replay.bind_all('<Control-Key-3>', button_replay_click)

    buttonCapture = Button(root, text='截图', command=buttonCaptureClick)
    buttonCapture.place(x=370, y=80, width=100, height=20)
    buttonCapture.bind_all('<Control-Key-4>', buttonCaptureClick)

    # 启动消息主循环
    root.mainloop()
