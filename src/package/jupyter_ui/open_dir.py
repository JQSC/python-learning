import tkinter as tk
from tkinter import filedialog
import ipywidgets as widgets
from IPython.display import HTML


def select_directory():
    # 初始化 Tkinter 主窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 打开文件选择对话框
    folder_selected = filedialog.askdirectory()

    # 关闭 Tkinter 主窗口
    root.destroy()

    return folder_selected


def select_file():
    # 初始化 Tkinter 主窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 打开文件选择对话框
    folder_selected = filedialog.askopenfilename()

    # 关闭 Tkinter 主窗口
    root.destroy()

    return folder_selected


button_dir = widgets.Button(
    description="选择解析目录",
    disabled=False,
    button_style="success",  # 'success', 'info', 'warning', 'danger' or ''
    tooltip="选择目录，目录下所有文件将解析",
)

button_file = widgets.Button(
    description="选择解析文件",
    disabled=False,
    button_style="info",  # 'success', 'info', 'warning', 'danger' or ''
    tooltip="选择的文件将被解析",
)

dir_text = widgets.Text(
    value="",
    placeholder="解析路径",
    # description='选中的目录地址:',
    disabled=False,
)


def btn_disable():
    button_file.disabled = not button_file.disabled
    button_dir.disabled = not button_dir.disabled


def dir_btn_click(b):
    # btn_disable()
    dir_text.value = select_directory()
    # btn_disable()


def file_btn_click(b):
    # btn_disable()
    dir_text.value = select_file()
    # btn_disable()


button_dir.on_click(dir_btn_click)
button_file.on_click(file_btn_click)


# 使用方式
# import sys
# module_path = '../common/lib'
# if module_path not in sys.path:
#     sys.path.append(module_path)
# import open_dir


def open_dir_ui():
    return widgets.GridBox(
        [button_dir, button_file, dir_text],
        layout=widgets.Layout(grid_template_columns="repeat(3, 160px)"),
    )
