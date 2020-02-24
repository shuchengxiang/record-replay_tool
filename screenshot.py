import tkinter
import tkinter.filedialog
import os
from PIL import ImageGrab
import time


# 用来显示全屏幕截图并响应二次截图的窗口类
class MyCapture:
    def __init__(self, root, png):
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        # 屏幕尺寸
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()

        # 创建顶级组件容器
        self.top = tkinter.Toplevel(root, bg='black', width=screenWidth, height=screenHeight)
        # 使用窗口半透明会导致Canvas无法覆盖屏幕底部栏
        # self.top.attributes("-alpha", 0.8)
        # self.top.attributes("-topmost", 1)
        # 不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=screenWidth, height=screenHeight, bd=0)

        # 显示全屏截图，在全屏截图上进行区域截图
        self.image = tkinter.PhotoImage(file=png)
        self.canvas.create_image(screenWidth//2, screenHeight//2, image=self.image)
        # self.canvas.create_rectangle(0, 0, screenWidth, screenHeight, fill='black')
        self.canvas.configure(highlightthickness=0)

        # 鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            #开始截图
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)

        # 鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            if not self.sel:
                return
            global lastDraw
            try:
                # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='black')
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)

        # 获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            self.sel = False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            time.sleep(0.1)

            # 考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left+1, top+1, right, bottom))
            default_save_filename = 'screenshot' + time.strftime("%Y%m%d%H%M%S") + '.png'
            # 弹出保存截图对话框
            fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', initialfile=default_save_filename,filetypes=[('image', '*.jpg *.png')])
            if fileName:
                pic.save(fileName)
            # 关闭当前窗口
            self.top.destroy()

        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        # 让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

if __name__ == '__main__':
    # 启动消息主循环
    root.mainloop()
