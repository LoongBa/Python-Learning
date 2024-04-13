import fitz
from tqdm import tqdm  # PyMuPDF


def process_hyperlinks(pdf_path):
    # 打开PDF文件
    doc = fitz.open(pdf_path)

    # 遍历每一页
    for page in doc:
    
#    for page in tqdm(
#        doc,        desc="Processing PDF",        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
#    ):
        textbox = page.get_textbox("url")
        if textbox.find("@163.com") > -1:
            print(f"{textbox}, {textbox.find('@163.com')}")
            textbox.delete()
            # 删除 textbox：文字及链接
            #page.delete_textbox(textbox)

    # 关闭文档
    doc.save("D:/_Dev_/_Repos_/Github/_CoffeeScholar_/Python-Learning/编程应用练习/PDF增强/程序员的算法趣题-无链接.pdf")
    doc.close()


pdf_filename = "D:/_Dev_/_Repos_/Github/_CoffeeScholar_/Python-Learning/编程应用练习/PDF增强/程序员的算法趣题.pdf"
process_hyperlinks(pdf_filename)
