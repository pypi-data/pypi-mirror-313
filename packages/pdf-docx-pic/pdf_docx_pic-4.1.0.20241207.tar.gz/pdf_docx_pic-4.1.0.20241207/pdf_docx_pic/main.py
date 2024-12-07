import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from pdf2docx import Converter
from docx2pdf import convert
import os
from threading import Thread
import fitz
from PIL import Image


def main_window():
    global var
    root = ttk.Window(alpha=0.9)
    root.title("pdf转word程序3.0")
    root.geometry("600x200")

    var = ttk.StringVar()

    b1 = ttk.Button(root, text="PDF转Word", bootstyle="danger", command=pdf_to_word_tk)
    b1.pack(fill=BOTH, side=LEFT)

    b2 = ttk.Button(
        root, text="PDF批量转Word", bootstyle="warning", command=pdf_to_words_tk
    )
    b2.pack(fill=BOTH, side=LEFT)

    b3 = ttk.Button(root, text="Word转PDF", bootstyle="primary", command=word_to_pdf)
    b3.pack(fill=BOTH, expand=True)

    b4 = ttk.Button(root, text="PDF转图片", bootstyle="success", command=pdf_to_image)
    b4.pack(fill=BOTH, expand=True)

    b4 = ttk.Button(root, text="关于", bootstyle="danger", command=about)
    b4.pack(fill=BOTH, expand=True)

    menu = ttk.Menu(root)
    menu_main = ttk.Menu(menu)

    menu_main.add_command(label="批量PDF转Word", command=pdf_to_words_tk)
    menu_main.add_command(label="单个PDF文件转Word", command=pdf_to_word_tk)
    menu_main.add_command(label="Word转PDF")
    menu_main.add_command(label="PDF转图片", command=pdf_to_image)

    menu.add_cascade(label="操作", menu=menu_main)

    menu.add_command(label="关于", command=about)
    menu.add_command(label="退出", command=root.quit)
    root.config(menu=menu)
    root.mainloop()


def control_pdf_to_word():
    if v.get() == 1:
        l.grid_forget()
        start_entry.grid_forget()
        l1.grid_forget()
        end_entry.grid_forget()
        l2.grid_forget()
        zh.grid()
    if v.get() == 2:
        l.grid(row=3, column=0)
        start_entry.grid(row=3, column=1)
        l1.grid(row=3, column=2)
        end_entry.grid(row=3, column=3)
        zh.grid(row=4, column=0)
        l2.grid(row=3, column=4)


def pdf_to_word_tk():
    global root, root1, v, start_entry, end_entry, l, l1, l2, zh
    root1 = ttk.Toplevel(alpha=0.9)
    root1.title("PDF转Word")
    root1.geometry("428x140")
    file_entry = ttk.Entry(root1, bootstyle="danger", textvariable=var)
    file_entry.grid(row=0, column=0)
    ttk.Button(root1, text="选择文件", bootstyle="danger", command=select_file).grid(
        row=0, column=1
    )
    v = ttk.IntVar()
    ttk.Radiobutton(
        root1, text="全部转换", variable=v, value=1, command=control_pdf_to_word
    ).grid(row=1, column=0)
    ttk.Radiobutton(
        root1, text="选择页面", variable=v, value=2, command=control_pdf_to_word
    ).grid(row=2, column=0)
    l = ttk.Label(root1, text="从")
    start_entry = ttk.Entry(root1, width=5)
    l1 = ttk.Label(root1, text="页到")
    end_entry = ttk.Entry(root1, width=5)
    l2 = ttk.Label(root1, text="页")
    zh = ttk.Button(
        root1,
        text="开始转换",
        bootstyle="warning",
        command=lambda: Thread(target=pdf_to_word).start(),
    )
    root1.state(NORMAL)


def select_file():
    global pdf_file
    pdf_file = askopenfilename(title="选择PDF文档", filetypes=[("PDF文件", "*.pdf")])
    var.set(pdf_file)


def select_folder():
    global folder
    folder = askdirectory()
    var1.set(folder)


def pdf_to_word(start=None, end=None):
    try:
        wordfile = f"{os.path.splitext(pdf_file)[0]}.docx"
        cv = Converter(pdf_file)
        if v.get() == 1:
            cv.convert(wordfile)
        if v.get() == 2:
            cv.convert(start=1, end=2)

        cv.close()
        showinfo("提示", "转换成功!")
    except:
        showerror("错误", "你没有选择任何文件或者文件不存在！")


def pdf_to_words_tk():
    global folder_entry, var1
    var1 = ttk.IntVar()
    root2 = ttk.Toplevel(alpha=0.9)
    root2.title("PDF批量转Word")
    root2.geometry("300x120")
    folder_entry = ttk.Entry(root2, bootstyle="danger", textvariable=var1)
    folder_entry.grid(row=0, column=0)
    ttk.Button(root2, text="选择文件夹", bootstyle="danger", command=select_folder).grid(
        row=0, column=1
    )
    ttk.Button(
        root2,
        text="开始转换",
        bootstyle="danger",
        command=lambda: Thread(target=pdf_to_words).start(),
    ).grid()
    root2.mainloop()


def word_to_pdf():
    try:
        inputfile = askopenfilename(title="选择DOCX文档", filetypes=[("DOCX文档", "*.docx")])
        outputfile = os.path.splitext(inputfile)[0] + ".pdf"
        f1 = open(outputfile, "w")
        f1.close()
        convert(inputfile, outputfile)
        showinfo("提示", "转换成功!")
    except:
        showerror("错误", "你没有选择任何文件或文件不存在！")


def pdf_to_words():
    folder_name = "已转换的文件"
    if not os.path.exists(f"{folder}/已转换的文件"):
        os.makedirs(f"{folder}/已转换的文件")
    for file in os.listdir(folder):
        suff_name = os.path.splitext(file)[1]
        if suff_name != ".pdf":
            continue
        file_name = os.path.splitext(file)[0]
        pdf_file = f"{folder}/{file}"
        word_file = f"{folder}/{folder_name}/{file_name}.docx"
        cv = Converter(pdf_file)
        cv.convert(word_file)
        cv.close()
        showinfo("提示", "转换成功!")


def about():
    showinfo("关于", "由liuhongrun2022制作\n版本号：3.0")


def pdf_to_image():
    if not os.path.exists("已转换的文件"):
        os.makedirs("已转换的文件")
    try:
        pdf_file = askopenfilename(title="选择PDF文档", filetypes=[("PDF文件", "*.pdf")])
        doc = fitz.open(pdf_file)

        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_file = f"已转换的文件/{page_number+1}.png"
            img.save(img_file)

        showinfo("提示", "转换成功!")
    except:
        showerror("错误", "你没有选择任何文件或文件不存在!")


if __name__ == "__main__":
    main_window()
