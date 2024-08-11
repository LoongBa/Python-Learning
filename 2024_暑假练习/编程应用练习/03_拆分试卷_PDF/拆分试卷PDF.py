# 学习中经常有各种试卷的 PDF 文件，其中一部分是 A3 幅面
# A3 幅面打印时需要对应的 A3 打印机，一般只有打印店、办公室才有，家用一般是小一些的 A4 打印机
# A3 幅面的尺寸是 A4 幅面的两倍。如果将一张 A3 幅面的试卷，对半拆分为两张 A4 幅面的试卷，就可以用家用打印机打印。
# 但有部分 A3 幅面试卷是分三段的，就不能简单的“对半分”。本工具，主要针对可以对半分的 A3 幅面试卷。

# 拆分试卷 PDF 工具
# 主要功能：将 A3 幅面的 PDF 试卷对半拆分为 A4 幅面的 PDF
# 作者：loonba
# 版本号：Ver1.1


# 主要步骤：
# 1. 获得要拆分的 PDF 文件的名字和完整路径；
# 2. 将 PDF 文件中的每一页提取为图像对象；
# 3. 对提取的每一页的图像对象，左右拆分为两个图像对象（各为原来图像的一半）
# 4. 按顺序将拆分后的图像对象重新组成一个 PDF 文件，保存原PDF文件相同的位置，文件名加后缀 "_A4"
# 5. 输出提示信息、打开文件

# V1.0 完成基本功能
# V1.1 增强了代码的健壮性：将传入参数的相对路径转为绝对路径
# TODO: V1.2 加入剪裁图片边框

import sys
import os
from pdf2image import convert_from_path
#from PIL import Image


# 输出错误信息
def print_error(message):
    print_color(message, "red")
    return


def print_color(message, color="green", end_str="\r\n"):
    text = color_text(color, message)
    # 用 switch 判断常用的颜色，或者用 字典
    print(text, end=end_str)


def color_text(color, text):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }

    if color in colors:
        return f"{colors[color]}{text}{colors['reset']}"
    else:
        return text


# 拆分指定的 PDF 文件为多个图片文件
def split_pdf_into_images(pdf_file_path: str) -> str:
    # 每个函数，是个承担“单一职责”的命令集合
    # 就像应用题需要提供必要的数据，这里就对应着参数；
    # 解应用题时，需要根据题目（参数）提供的直接信息推导出所需要的间接信息
    if not os.path.isfile(pdf_file_path) or not pdf_file_path.lower().endswith(".pdf"):
        return False, f"请提供有效的 PDF 文件：{pdf_file_path}"

    # 调用第三方包，拆分 PDF 为多个图像的对象
    pages_images = convert_from_path(pdf_file_path)  # convert 转换
    pdf_file_name = os.path.basename(pdf_file_path).lower()
    print_color(f"\t正在拆分：{pdf_file_name}")  # 输出信息

    image_list = []
    # 遍历每一页对应的图像文件（内存中）
    for i, page_image in enumerate(pages_images):
        # 利用了 enumerate 将可枚举类型返回为 加了索引的 可枚举类型：元组的 Array
        page_number = i + 1
        # 拆分页对应的图片为两个图片
        page_images_list = split_image_into_images(
            page_image
        )  # 调用函数拆分图片
        image_list.extend(page_images_list) # extend 扩展， append 追加， Injection 注入
        print_color(f"\t\t成功拆分第 {page_number} 页。")  # 输出信息

    return True, image_list


# 将指定的图片文件，拆分成两个图片文件
def split_image_into_images(page_image: any):   # TODO: 将来扩展为支持拆分为三部分，支持剪裁试卷周围区域
    # 获得图像的宽度和高度
    width, height = page_image.size
    new_width = width // 2
    image_left = page_image.crop((0, 0, new_width, height))
    image_right = page_image.crop((new_width, 0, width, height))

    image_list = [image_left, image_right]
    return image_list


def merge_images_into_pdf(images_list: str, new_pdf_file_path: str) -> str:
    pdf = images_list[0]
    pdf.save(
        new_pdf_file_path,
        "PDF",
        resolution = 100.0,
        save_all = True,
        append_images = images_list[1:],
    )
    return True, new_pdf_file_path  # 返回完整路径


def run_file_by_default_app(file_path):
    if os.path.isfile(file_path):
        os.startfile(file_path)
    else:
        os.system("explorer.exe", file_path)

    return


def main():
    # 1. 获得要拆分的 PDF 文件的名字和完整路径；
    if len(sys.argv) < 2:
        print_error("请提供要拆分的 PDF 文件的完整路径。")
        return

    pdf_file_path = sys.argv[1]
    if not os.path.isabs(pdf_file_path):    # 是否是绝对路径
        #current_workingfolder_path = os.path.abspath(os.curdir)    # 注意：os.curdir 获取到的可能不是绝对路径，需要加上保险：os.path.abspath()
        #pdf_file_path = os.path.join(current_workingfolder_path, pdf_file_path)    
        pdf_file_path = os.path.abspath(pdf_file_path)      # os.path.abspath() 获取绝对路径——拼接了当前工作目录的绝对路径
        # 尝试基于当前工作目录查找文件
        if not is_pdf(pdf_file_path):
            # 如果在当前工作目录中找不到文件，再尝试基于脚本所在目录查找文件
            script_folder_path = os.path.dirname(os.path.abspath(__file__))     # __file__ 当前脚本的完整路径
            pdf_file_path = os.path.join(script_folder_path, sys.argv[1])
        
    if not is_pdf(pdf_file_path):
        print_error(f"请提供有效的 PDF 文件：{pdf_file_path}")
        return

    new_pdf_file_path = pdf_file_path.lower().replace(".pdf", "_A4.pdf")
    # 2. 将 PDF 文件中的每一页的图片导出到临时目录，注意文件名的顺序；
    is_success, image_list = split_pdf_into_images(pdf_file_path)
    if not is_success:
        print_error(f"拆分 PDF 文件失败：{image_list}")
        return
    # split 拆分     image 图像

    # 3. 对临时目录中的所有拆分过的图片文件，按顺序重新组成一个 PDF 文件；
    result = merge_images_into_pdf(
        image_list, new_pdf_file_path
    )  # merge 融合、合并
    if result:
        print_color(f"PDF 文件已保存到: {new_pdf_file_path}")

    # 4. 运行新的 PDF 文件：使用默认的 PDF 阅读器打开
    run_file_by_default_app(new_pdf_file_path)
    return

def is_pdf(pdf_file_path):
    return os.path.isfile(pdf_file_path) and pdf_file_path.lower().endswith(".pdf")


if __name__ == "__main__":
    main()
