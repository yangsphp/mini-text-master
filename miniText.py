# 记事本
__author__ = "Yang"

import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import hashlib
import time


''' 函数列表 '''


''' 点击触发新建 '''
def newBuild():
    global md5Str, nowOperateFilePath
    # 清空Text内容
    text.delete(index, tk.END)
    md5Str = md5("")
    nowOperateFilePath = ""
    # 设置窗口标题
    setWindowTitle()
    # 设置行列号
    setMarkPostion()


''' 将内容保存到文件'''
def saveFile(filePath):
    global nowOperateFilePath, isSaveStatus, md5Str
    # 去除Text文本内容最后的\n
    content = text.get(index, tk.END)[:-1]
    with open(filePath, "w+", encoding = "utf-8") as f:
        f.write(content)
        # 将内容保存为md5格式，用于对比内容是否发生改变
        md5Str = md5(content)
    # 保存当前操作的路径
    nowOperateFilePath = filePath
    # 设置当前文本已保存态
    isSaveStatus = True
    setWindowTitle(filePath)
    print("保存文件成功，路径：" + filePath)

''' 根据是否保存状态，返回一个字符'''
def returnTitle():
    global isSaveStatus
    if isSaveStatus is True:
        return ''
    return '*'

''' 设置窗口标题'''
def setWindowTitle(filePath = None):
    if filePath is None or filePath == '':
        window.title("无标题* - 记事本")
    else:
        fileName = os.path.basename(filePath)
        window.title("%s%s - 记事本" % (fileName, returnTitle()))

''' 保存文件 '''
def toSaveFile():
    global nowOperateFilePath
    if nowOperateFilePath == "":
        # 文件不存在，新建
        try: 
            filePath = tk.filedialog.asksaveasfilename(title = u"保存", filetypes = fileTypes, initialdir = initDir)
            if filePath is not None:
                saveFile(filePath)
            else:
                print("保存文件出错")
        except Exception  as e:
            print(e)
    else:
        # 文件存在，直接保存
        saveFile(nowOperateFilePath)
        
    
''' 打开文件 '''
def toOpenFile():
    global nowOperateFilePath, md5Str
    try:
        filePath = tk.filedialog.askopenfilename(title = u"打开", filetypes = fileTypes, initialdir = initDir)
        if filePath is not None:
           with open(filePath, "r", encoding = "utf-8") as f:
               newBuild()
               content = f.read()
               text.insert(tk.INSERT, content)
               md5Str = md5(content)
           print("打开文件成功，路径：" + filePath)
           nowOperateFilePath = filePath
           # 设置窗口标题
           setWindowTitle(filePath)
           setMarkPostion(None, tk.INSERT)
        else:
            print("打开文件出错")
    except Exception as e:
        print(e)

    
''' MD5加密'''
def md5(content):
    md5 = hashlib.md5()
    md5.update(str(content).encode("utf-8"))
    return md5.hexdigest()

''' 另存为 '''
def toSaveOtherFile():
    try:
        file = tk.filedialog.asksaveasfile(title = u"另存为", filetypes = fileTypes, initialdir = initDir)
        if file is not None:
            saveFile(file.name)
            print("完成另存为")
        else:
            print("另存为出错")
    except Exception as e:
        print(e)

''' 获取光标所在的行和列 '''
def getIndex(text, index):
    return tuple(map(int, str.split(text.index(index), ".")))

''' 关闭主窗口触发'''
def callCloseWindow():
    if isSaveStatus is False:
        # 弹窗提示
        okCancel = tk.messagebox.askokcancel("提示", "内容没有保存，是否直接关闭？")
        if okCancel is True:
            window.destroy()
        else:
            print("cancel")
    else:
        window.destroy()

''' 剪切'''
def toCut():
    text.event_generate("<<Cut>>")
    
''' 复制'''
def toCopy():
    text.event_generate("<<Copy>>")

''' 粘贴'''
def toPaste():
    text.event_generate("<<Paste>>")
    # 设置光标位置
    setMarkPostion()

''' 撤销'''
def toUndo():
    text.event_generate("<<Undo>>")

''' 恢复撤销'''
def toRedo():
    text.event_generate("<<Redo>>")

''' 关闭查找框回调'''
def callCloseFindDialog(findDialog):
    # 删除标签，关闭搜索窗口
    removeTag(index)
    findDialog.destroy()

''' 删除标签'''
def removeTag(startIndex, endIndex = tk.END, tagName = "find"):
    text.tag_remove(tagName, startIndex, endIndex)

''' 开始搜索'''
def findTextStr(strs):
    startIndex = 1.0
    # 删除标签
    removeTag(startIndex)
    if strs:
        # 记录找到的个数
        count = 0
        while True:
            startIndex = text.search(strs, startIndex, nocase = True, stopindex = tk.END)
            if not startIndex:
                break
            lastIndex = "%s+%sc" % (startIndex, len(strs))
            text.tag_add("find", startIndex, lastIndex)
            startIndex = lastIndex
            count += 1
        text.tag_config("find", background = "#0088A8", foreground = "#fff")
        if count == 0:
            tk.messagebox.showwarning(title = "提示", message = "没有找到内容")

''' 动态设置搜索按钮状态'''
def setBtnStatus(fBtn, strs):
    if not strs:
        fBtn.config(state = tk.DISABLED)
    else:
        fBtn.config(state = tk.NORMAL)
    
''' 查找弹出框'''
def toFind():
    findDialog = tk.Toplevel(padx = 10, pady = 10)
    findDialog.title("查找")
    findDialog.resizable(0, 0)
    fW = 300
    fH = 50
    fX = int((screen_width - fW) / 2)
    fY = int((screen_height - fW) / 2)
    findDialog.geometry("%sx%s+%s+%s" %(fW, fH, fX, fY))
    findDialog.attributes("-toolwindow", 2)
    
    tk.Label(findDialog, text = "查找：").grid(row = 0, column=0)
    fVar = tk.StringVar()
    # 输入框
    fEntry = tk.Entry(findDialog, textvariable = fVar, insertwidth = 1)
    fEntry.focus_set()
    fEntry.grid(row = 0, column=1)
    
    fBtn = tk.Button(findDialog, text = "查找所有", height = 1, state = tk.DISABLED, command = lambda : findTextStr(fVar.get()))
    fBtn.grid(row = 0, column = 3, ipadx = 8)
    
    fEntry.bind("<KeyRelease>", lambda event: setBtnStatus(fBtn, fVar.get()))
    
    tk.Label(findDialog, text = "  ").grid(row = 0, column=2)
   
    findDialog.attributes("-topmost", 1)
    findDialog.protocol("WM_DELETE_WINDOW", lambda : callCloseFindDialog(findDialog))
    findDialog.mainloop()


''' md5判断内容是否改变 '''
def textIsChange():
    content = text.get(index, tk.END)
    if md5(content[:-1]) == md5Str:
        return False
    return True

''' 动态设置光标所在行和列'''
def setMarkPostion(index = None, type_ = tk.CURRENT):
    if index is None:
        line_num = getIndex(text, text.index(type_))
        var.set(["第%s行" % line_num[0], "第%s列" % (line_num[1] + 1)])
    else:
        text.focus()
        text.mark_set(type_,index)

''' 键盘输入事件'''
def keyBoard():
    global isSaveStatus
    # 设置光标的行和列
    setMarkPostion(None, tk.INSERT)
    # 判断内容是否发生改变
    isChange = textIsChange()
    if isChange is True:
        # 内容发生改变
        isSaveStatus = False
    else:
        # 内容没有发生改变
        isSaveStatus = True
    # 设置窗口标题
    setWindowTitle(nowOperateFilePath)


''' 窗口初始化配置 '''
window = tk.Tk()
win_width = 600
win_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width - win_width) / 2)
y = int((screen_height - win_height) / 2)

window.title("无标题* - 记事本")
window.geometry("%sx%s+%s+%s" % (win_width, win_height, x, y))
# 最好用绝对路径
window.iconbitmap("G:/记事本/icon.ico")

''' 全局变量'''
# 保存文件类型
fileTypes = [('text files', '.txt'), ('all files', '.*')]
#当前操作的文件路径
nowOperateFilePath = ""
# 文件是否保存状态
isSaveStatus = True
# 当前文件路径
initDir = os.path.abspath("./")
# Text 1行1列
index = 1.0
# Text 字体大小
textFont = 13
''' md5加密后的内容, 初始化md5内容'''
md5Str = md5("")




''' 设置菜单 '''
menu_bar = tk.Menu(window)
window.config(menu = menu_bar)

file_bar = tk.Menu(menu_bar, tearoff = 0)
file_bar.add_command(label = "新建", accelerator = "Ctrl + N", command = newBuild)
file_bar.add_command(label = "打开", accelerator = "Ctrl + O", command = toOpenFile)
file_bar.add_command(label = "保存", accelerator = "Ctrl + S", command = toSaveFile)
file_bar.add_command(label = "另存为", command = toSaveOtherFile)
file_bar.add_separator()
file_bar.add_command(label = "退出", command = window.destroy)
menu_bar.add_cascade(label = "文件", menu = file_bar)

edit_bar = tk.Menu(menu_bar, tearoff = 0)
edit_bar.add_command(label="撤销", accelerator="Ctrl + Z", command = toUndo)
edit_bar.add_command(label="回复撤销", accelerator="Ctrl + Y", command = toRedo)
edit_bar.add_separator()
edit_bar.add_command(label = "剪切", accelerator = "Ctrl + X", command = toCut)
edit_bar.add_command(label = "复制", accelerator = "Ctrl + C", command = toCopy)
edit_bar.add_command(label = "粘贴", accelerator = "Ctrl + V", command = toPaste)
edit_bar.add_separator()
edit_bar.add_command(label="查找", accelerator="Ctrl + F", command = toFind)
menu_bar.add_cascade(label = "编辑", menu = edit_bar)

about_menu = tk.Menu(menu_bar, tearoff = 0)
about_menu.add_command(label = "版本", accelerator = "v1.0.0")
about_menu.add_command(label = "作者", accelerator = "样子")
menu_bar.add_cascade(label = "关于", menu = about_menu)

''' 设置纵向滚动条 '''
scroll_bar = tk.Scrollbar(window)
scroll_bar.pack(fill = "y", side = "right")


''' 设置Text '''
text = tk.Text(window, font = ("宋体", textFont), padx = 2, pady = 2, undo = True, yscrollcommand = scroll_bar.set)
text.insert("insert", "")
# 设置光标在首行
setMarkPostion(index, "start")
text.pack(expand = 1, fill = "both")
scroll_bar.config(command = text.yview)

text.bind("<Control-Key-X>", lambda event: toCut())
text.bind("<Control-Key-C>", lambda event: toCopy())
text.bind("<Control-Key-V>", lambda event: toPaste())
text.bind("<Control-Key-Z>", lambda event: toUndo())
text.bind("<Control-Key-Y>", lambda event: toRedo())
text.bind("<Control-Key-f>", lambda event: toFind())

text.bind("<Control-Key-n>", lambda event: newBuild())
text.bind("<Control-Key-N>", lambda event: newBuild())
text.bind("<Control-Key-s>", lambda event: toSaveFile())
text.bind("<Control-Key-S>", lambda event: toSaveFile())
text.bind("<Control-Key-o>", lambda event: toOpenFile())
text.bind("<Control-Key-O>", lambda event: toOpenFile())
text.bind("<KeyRelease>", lambda event: keyBoard())
text.bind("<ButtonRelease-1>", lambda event: setMarkPostion())

''' 设置显示当前行 '''
var = tk.StringVar()
label = tk.Label(window, text = "第 1 行", height = 1, pady = 10, font = ("宋体", 10), textvariable=var)
setMarkPostion()
label.pack(side = "bottom", anchor = "w")


# 监听window关闭
window.protocol("WM_DELETE_WINDOW", callCloseWindow)
window.mainloop()













