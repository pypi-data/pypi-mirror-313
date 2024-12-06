# encoding:utf8
import json
import os
import tkinter
import tkinter.font
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog
from typing import List, Any, Union

from tooly.types import Literal

"""
此文件能实现通过简单的函数调用，实现基本的参数设置。
参数的类型支持：SingleChoiceParam（单选）、MultiChoiceParam（多选）、FileParam（文件）、TextParam（文本类型）以及ask_option(弹窗）
具体使用方法见代码中__main__
"""


class Param:

    def __init__(self, label: str, defaultVal: Any, validator, escapeCache):
        self.label = label  # 变量的名称
        self.defaultVal = defaultVal
        self.var = None
        self.validator = validator
        self.escapeCache = escapeCache

    def put_items(self, root, row):
        """
        :param root: 父容器（采用的是grid布局）
        :param row: 行号
        """
        raise NotImplementedError()

    def value(self):
        # 返回变量对应的value
        raise NotImplementedError()

    def valid(self) -> str:
        # get_args调用当前函数检查参数是否合法
        raise NotImplementedError()


class SingleChoiceParam(Param):
    def put_items(self, root, row):
        label = tkinter.Label(root, text=self.label + ":")
        label.grid(row=row, column=0, sticky='E')

        frame = tkinter.ttk.Frame(root)
        frame.grid(row=row, column=1, sticky='W')

        self.var = tkinter.IntVar()

        if self.defaultVal:
            self.var.set(self.options.index(self.defaultVal))
        else:
            self.var.set(0)
        for idx, option in enumerate(self.options):
            tmp = tkinter.Radiobutton(frame, text=option, variable=self.var, value=idx)
            tmp.grid(row=0, column=idx, sticky='W')

    def value(self):
        return self.options[self.var.get()]

    def valid(self) -> str:
        pass

    def __init__(self, label, options: List[str], defaultVal=None, escapeCache=False):
        if defaultVal is None:
            defaultVal = []
        super().__init__(label, defaultVal, None, escapeCache)
        self.options = options


class MultiChoiceParam(Param):
    def __init__(self, label: str, options: List[str], defaultVal: List[str] = None, notEmpty=False, escapeCache=False):
        if defaultVal is None:
            defaultVal = []
        super().__init__(label, defaultVal, None, escapeCache)
        self.options = options
        self.notEmpty = notEmpty

    def put_items(self, root, row):

        label = tkinter.Label(root, text=self.label + ":")
        label.grid(row=row, column=0, sticky='E')

        frame = tkinter.ttk.Frame(root)
        frame.grid(row=row, column=1, sticky='W')

        self.var = []

        for idx, option in enumerate(self.options):
            val = tkinter.IntVar()
            if option in self.defaultVal:
                val.set(1)
            self.var.append(val)
            w = tkinter.Checkbutton(frame, text=option, variable=val, onvalue=1, offvalue=0)
            w.grid(row=0, column=idx, sticky='W')

    def value(self):
        return [self.options[idx] for idx, i in enumerate(self.var) if i.get()]

    def valid(self) -> str:
        if self.notEmpty:
            if len(self.value()) == 0:
                return "不能为空"


class FileParam(Param):
    def valid(self) -> str:
        var = self.var.get()
        if self.required and not var:
            return "不能为空"

    def put_items(self, root, row):
        # 标签，父级元素为root
        label = tkinter.Label(root, text=self.label + ":")
        # 输入框绑定到的一个变量
        self.var = tkinter.StringVar(value=self.defaultVal)
        # 输入框
        text = tkinter.Entry(root, textvariable=self.var, state='disabled')
        dialog_type = self.dialog_type

        def fdialog():
            t = getattr(tkinter.filedialog, dialog_type)()
            self.var.set(t)

        btn = tkinter.ttk.Button(root, text="…", command=fdialog, width=2)

        # 标签通过grid方式布放，row为上层传递过来的，靠左
        label.grid(row=row, column=0, sticky="E", padx=5, pady=3)
        # 输入框靠右放
        text.grid(row=row, column=1, sticky="E")
        btn.grid(row=row, column=2, sticky='E', padx=3)

    def value(self):
        return self.var.get()

    def __init__(self, label, defaultVal='', required=True,
                 dialogType: Literal['askopenfilename', 'asksaveasfilename', 'askdirectory'] = 'askopenfilename',
                 escapeCache=False):
        super().__init__(label, str(defaultVal), None, escapeCache)
        self.dialog_type = dialogType
        self.required = required


class TextParam(Param):

    def __init__(self, label, defaultVal: Union[str, int] = "", validator=None, notBlank=False, isNumber=False,
                 escapeCache=False):
        super().__init__(label, str(defaultVal), validator, escapeCache)
        self.not_blank = notBlank
        self.require_number = isNumber

    def put_items(self, root, row):
        # 标签，父级元素为root
        label = tkinter.Label(root, text=self.label + ":")
        # 输入框绑定到的一个变量
        self.var = tkinter.StringVar(value=self.defaultVal)
        # 输入框
        text = tkinter.Entry(root, textvariable=self.var)

        # 标签通过grid方式布放，row为上层传递过来的，靠左
        label.grid(row=row, column=0, sticky="E", padx=5, pady=3)
        # 输入框靠右放
        text.grid(row=row, column=1, sticky="W")

    def value(self):
        if self.require_number:
            return int(self.var.get())
        return self.var.get()

    def valid(self):
        if self.validator:
            tmp = self.validator(self.var.get())
            if tmp:
                return tmp
        if self.not_blank and (len(self.var.get()) <= 0):
            return "不能为空"
        if self.require_number:
            try:
                int(self.var.get())
            except:
                return "需要为数字"


def __set_center(root):
    # 将弹框的位置设置到正中心
    root.update()
    curWidth = root.winfo_width()
    curHight = root.winfo_height()
    scn_w, scn_h = root.maxsize()
    # 计算中心坐标
    cen_x = (scn_w - curWidth) / 2
    cen_y = (scn_h - curHight) / 2
    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
    root.geometry(size_xy)


def get_args(args: List[Param], cache_file='args.json', 允许退出程序=True):
    """
    弹出框让用户设置参数，
    :return: 所有参数结果的list，如果用户点击关闭则自动退出程序
    """
    argNames = ''.join([item.label for item in args])
    cache_data = {}
    if cache_file and os.path.exists(cache_file):
        with open(cache_file, 'rb') as fd:
            cache_data = json.load(fd)
            data = cache_data.get(argNames, {})
            for arg in args:
                if arg.label in data and not arg.escapeCache:
                    arg.defaultVal = data[arg.label]

    root = tkinter.Tk()
    root.title("设置参数")
    root.resizable(0, 0)
    title = tkinter.Label(root, text="设置参数", font=tkinter.font.Font(family='microsoft yahei', size=14), pady=15)
    title.grid(row=0, column=0)
    frame = tkinter.ttk.Frame(root, padding=(30, 0, 30, 10))

    for (idx, param) in enumerate(args):
        param.put_items(frame, idx)

    _ret = {"ret": "exit"}

    def confirm():
        # 点击确定按钮后，检查所有的参数，并且收集所有的结果
        tmp = []
        for arg in args:
            msg = arg.valid()
            if msg:
                tkinter.messagebox.showwarning("参数不正确", arg.label + msg)
                return
            else:
                tmp.append(arg.value())
        _ret["ret"] = tmp
        root.destroy()

    btn = tkinter.Button(frame, text="确定", padx=20, command=confirm)
    btn.grid(row=len(args), column=1, sticky="W", pady=10)
    frame.grid(row=1, column=0)

    __set_center(root)
    if not 允许退出程序:
        root.protocol("WM_DELETE_WINDOW", lambda: False)
    root.mainloop()

    if _ret["ret"] == "exit":
        os._exit(0)

    tmp = {}
    for idx, p in enumerate(args):
        tmp[p.label] = _ret["ret"][idx]

    if cache_file:
        cache_data[argNames] = tmp
        jsonStr = json.dumps(cache_data, ensure_ascii=False, indent=4)
        with open(cache_file, 'w', encoding='utf8') as fd:
            fd.write(jsonStr)

    return tmp


def ask_option(title: str, options: List[str], 允许退出程序=False):
    root = tkinter.Tk()
    root.title(title)

    root.resizable(0, 0)
    _title = tkinter.Label(root, text=title, font=tkinter.font.Font(family='microsoft yahei', size=14), pady=30,
                           padx=30)
    _title.grid(row=0, column=0, sticky='w')

    frame = tkinter.ttk.Frame(root, padding=(15, 0, 15, 30))
    _ret = {}

    def handler(option):
        def ret():
            _ret["ret"] = option
            root.destroy()

        return ret

    for idx, option in enumerate(options):
        btn = tkinter.Button(frame, text=option, padx=15, command=handler(option))
        btn.grid(row=0, column=idx, padx=15)

    frame.grid(row=1, column=0)
    __set_center(root)
    if not 允许退出程序:
        root.protocol("WM_DELETE_WINDOW", lambda: False)
    root.mainloop()
    # 如果主循环关闭了，还没有设置选项，那就是因为点击了X导致的
    if len(_ret) == 0:
        os._exit(0)
    return _ret["ret"]


if __name__ == '__main__':
    # ret = get_args([TextParam("姓名说带飞时代发", notBlank=True, defaultVal="sssssssss"),
    #                 TextParam("年龄", isNumber=True, defaultVal=3),
    #                 MultiChoiceParam("duoxuan", ["苹果", "梨子"], defaultVal=["苹果"], notEmpty=False),
    #                 SingleChoiceParam("玩具", ["dao", "bi"], defaultVal="bi"),
    #                 FileParam("文件", required=False)], 允许退出程序=False)
    # print("ret = ", ret)
    #
    ret = get_args([TextParam("key", notBlank=True, defaultVal="sssssssss"),
                    TextParam("年龄", isNumber=True, defaultVal=3),
                    MultiChoiceParam("duoxuan", ["苹果", "梨子"], defaultVal=["苹果"], notEmpty=False),
                    SingleChoiceParam("玩具", ["dao", "bi"], defaultVal="bi"),
                    FileParam("文件", required=False)])

    print("ret2 = ", ret)

    ask_option("事实上事实上事实上", ["确 定"])
