# 学习中经常有各种试卷的 PDF 文件，其中一部分是 A3 幅面
# A3 幅面打印时需要对应的 A3 打印机，一般只有打印店、办公室才有，家用一般是小一些的 A4 打印机
# A3 幅面的尺寸是 A4 幅面的两倍。如果将一张 A3 幅面的试卷，对半对折为两张 A4 幅面的试卷，就可以用家用打印机打印。
# 但有部分 A3 幅面试卷是分三段的，就不能简单的"对半分"。本工具，主要针对可以对半分的 A3 幅面试卷。

# 对折试卷 PDF 工具
# 主要功能：将 A3 幅面的 PDF 试卷对半对折为 A4 幅面的 PDF
# 作者：loonba
# 版本号：Ver1.3


# 主要步骤：
# 1. 获得要对折的 PDF 文件的名字和完整路径；
# 2. 将 PDF 文件中的每一页提取为图像对象；
# 3. 对提取的每一页的图像对象，左右对折为两个图像对象
#       （各为原来图像的一半）
# 4. 按顺序将对折后的图像对象重新组成一个 PDF 文件，
#       保存原PDF文件相同的位置，文件名加后缀 "_A4"
# 5. 输出提示信息、打开文件

# V1.0 完成基本功能
# V1.1 增强了代码的健壮性：将传入参数的相对路径转为绝对路径
# V1.2 加入剪裁图片边框，支持左右边距设置
# V1.3 增加中线偏移参数，支持上下左右边距设置

import sys
import os
import argparse
from PIL import Image
from pdf2image import convert_from_path
# 添加上级目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from myUtils import print_error, run_file_by_default_app, print_color

# 获得要对折的 PDF 文件的名字和完整路径
def get_pdf_file_path() -> str:
    if len(sys.argv) < 2:
        print_error("请提供要对折的 PDF 文件的完整路径。")
        return None, None

    pdf_file_path = sys.argv[1]
    if not os.path.isabs(pdf_file_path):    # 是否是绝对路径
        #pdf_file_path = os.path.join(current_workingfolder_path, pdf_file_path)    
        pdf_file_path = os.path.abspath(pdf_file_path)      # os.path.abspath() 获取绝对路径——拼接了当前工作目录的绝对路径
        # 尝试基于当前工作目录查找文件
        if not is_pdf(pdf_file_path):
            # 如果在当前工作目录中找不到文件，再尝试基于脚本所在目录查找文件
            script_folder_path = os.path.dirname(os.path.abspath(__file__))     # __file__ 当前脚本的完整路径
            pdf_file_path = os.path.join(script_folder_path, sys.argv[1])
        
    if not is_pdf(pdf_file_path):
        print_error(f"请提供有效的 PDF 文件：{pdf_file_path}")
        return None, None

    new_pdf_file_path = pdf_file_path.lower().replace(".pdf", "_A4.pdf")    
    return pdf_file_path, new_pdf_file_path

# 提取 PDF 文件中的每一页为图像对象
def split_pdf(pdf_file_path: str, new_pdf_file_path: str, 
              crop_left=0, crop_right=0, crop_top=0, crop_bottom=0,
              offset_x=0, offset_y=0,
              margin_top=0, margin_bottom=0, margin_left=0, margin_right=0) -> str:
    # 每个函数，是个承担"单一职责"的命令集合
    # 就像应用题需要提供必要的数据，这里就对应着参数；
    # 解应用题时，需要根据题目（参数）提供的直接信息推导出所需要的间接信息
    if not is_pdf(pdf_file_path):
        return False, f"请提供有效的 PDF 文件：{pdf_file_path}"

    # 调用第三方包，对折 PDF 为多个图像的对象
    pages_images = convert_from_path(pdf_file_path)  # convert 转换
    #TODO: 检查错误
    pdf_file_name = os.path.basename(pdf_file_path).lower()
    print_color(f"\t正在对折：{pdf_file_name}")  # 输出信息

    splited_images_list = []
    # 遍历每一页对应的图像文件（内存中）
    for i, page_image in enumerate(pages_images):
        # 利用了 enumerate 将可枚举类型返回为 加了索引的 可枚举类型：元组的 Array
        page_number = i + 1
        # 对折页对应的图片为两个图片，传入边距参数
        page_images_list = split_image_into_images(
            page_image, 
            crop_left, crop_right, crop_top, crop_bottom,
            offset_x, offset_y,
            margin_top, margin_bottom, margin_left, margin_right
        )  # 调用函数对折图片
        splited_images_list.extend(page_images_list) 
        # 顺手学单词：extend 扩展， append 追加， Injection 注入
        print_color(f"\t\t成功对折第 {page_number} 页。")  # 输出信息

    # 保存为 PDF 文件
    pdf_first_page_image = splited_images_list[0]
    pdf_first_page_image.save(new_pdf_file_path, "PDF", save_all = True,
        # 追加剩余图像  append: 追加
        append_images = splited_images_list[1:], 
    )

    return True, new_pdf_file_path


# 将指定的图片文件，拆分成两个图片文件
# 支持设置左右边距和中线偏移
def split_image_into_images(page_image: Image.Image, 
                           crop_left=0, crop_right=0, crop_top=0, crop_bottom=0,
                           offset_x=0, offset_y=0,
                           margin_top=0, margin_bottom=0, margin_left=0, margin_right=0) -> list[Image.Image]: 
    # 获得图像的宽度和高度
    width, height = page_image.size
    
    # 计算实际可用的宽度（减去左右剪裁）
    usable_width = width - crop_left - crop_right
    # 计算实际可用的高度（减去上下剪裁）
    usable_height = height - crop_top - crop_bottom
    
    # 计算分割点（在可用宽度的中间，加上x偏移量）
    split_point = crop_left + usable_width // 2 + offset_x
    
    # 裁剪图片，将图片分成两部分
    image_left = page_image.crop((crop_left, crop_top, split_point, height - crop_bottom))
    image_right = page_image.crop((split_point, crop_top, width - crop_right, height - crop_bottom))
    
    # 如果需要添加边距，创建新的图像对象
    if margin_top > 0 or margin_bottom > 0 or margin_left > 0 or margin_right > 0:
        # 获取分割后的图像尺寸
        left_width, left_height = image_left.size
        right_width, right_height = image_right.size
        
        # 创建带边距的新图像
        new_left_width = left_width + margin_left + margin_right
        new_left_height = left_height + margin_top + margin_bottom
        new_right_width = right_width + margin_left + margin_right
        new_right_height = right_height + margin_top + margin_bottom
        
        # 创建白色背景的新图像
        new_image_left = Image.new('RGB', (new_left_width, new_left_height), color='white')
        new_image_right = Image.new('RGB', (new_right_width, new_right_height), color='white')
        
        # 将原图粘贴到新图像上，保留边距
        new_image_left.paste(image_left, (margin_left, margin_top))
        new_image_right.paste(image_right, (margin_left, margin_top))
        
        # 更新图像对象
        image_left = new_image_left
        image_right = new_image_right

    # 将裁剪后的图片存入列表
    image_list = [image_left, image_right]
    return image_list   # 返回图像列表，以便调用代码合并到已有数组

# 合并图像列表为一个 PDF 文件
def merge_images_into_pdf(images_list: list[Image.Image],
                            new_pdf_file_path: str) -> str:
    try:
        pdf_first_page_image = images_list[0]
        pdf_first_page_image.save(
            new_pdf_file_path, "PDF", save_all = True,
            # 追加剩余图像  append: 追加
            append_images = images_list[1:], 
        )
        return True, ""
    except Exception as e:
        return False, f"合并图像列表为 PDF 文件失败：{e}"

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='对折试卷 PDF 工具')
    parser.add_argument('pdf_file', help='要对折的 PDF 文件的路径')
    
    # 剪裁参数
    parser.add_argument('-cl', '--crop-left', type=int, default=0, help='左边剪裁量（像素），默认为0')
    parser.add_argument('-cr', '--crop-right', type=int, default=0, help='右边剪裁量（像素），默认为0')
    parser.add_argument('-ct', '--crop-top', type=int, default=0, help='上边剪裁量（像素），默认为0')
    parser.add_argument('-cb', '--crop-bottom', type=int, default=0, help='下边剪裁量（像素），默认为0')
    
    # 偏移参数
    parser.add_argument('-xo', '--offset-x', type=int, default=0, help='X方向中线偏移量（像素），默认为0')
    parser.add_argument('-yo', '--offset-y', type=int, default=0, help='Y方向中线偏移量（像素），默认为0')
    
    # 边距参数
    parser.add_argument('-ml', '--margin-left', type=int, default=0, help='左边距（像素），默认为0')
    parser.add_argument('-mr', '--margin-right', type=int, default=0, help='右边距（像素），默认为0')
    parser.add_argument('-mt', '--margin-top', type=int, default=0, help='上边距（像素），默认为0')
    parser.add_argument('-mb', '--margin-bottom', type=int, default=0, help='下边距（像素），默认为0')
    
    args = parser.parse_args()
    
    # 1. 获得要对折的 PDF 文件的名字和完整路径；
    pdf_file_path = args.pdf_file
    if not os.path.isabs(pdf_file_path):    # 是否是绝对路径
        pdf_file_path = os.path.abspath(pdf_file_path)      # os.path.abspath() 获取绝对路径——拼接了当前工作目录的绝对路径
        # 尝试基于当前工作目录查找文件
        if not is_pdf(pdf_file_path):
            # 如果在当前工作目录中找不到文件，再尝试基于脚本所在目录查找文件
            script_folder_path = os.path.dirname(os.path.abspath(__file__))     # __file__ 当前脚本的完整路径
            pdf_file_path = os.path.join(script_folder_path, args.pdf_file)
        
    if not is_pdf(pdf_file_path):
        print_error(f"请提供有效的 PDF 文件：{pdf_file_path}")
        return
    
    new_pdf_file_path = pdf_file_path.lower().replace(".pdf", "_A4.pdf")
    
    # 2. 提取 PDF 文件中的每一页为图像对象，传入边距参数
    is_success, new_pdf_file_path = split_pdf(
        pdf_file_path, new_pdf_file_path, 
        args.crop_left, args.crop_right, args.crop_top, args.crop_bottom,
        args.offset_x, args.offset_y,
        args.margin_top, args.margin_bottom, args.margin_left, args.margin_right
    )
    if not is_success:
        print_error(f"提取 PDF 文件失败：{pdf_file_path}")
        return

    print_color(f"PDF 文件已保存到: {new_pdf_file_path}")

    # 4. 运行新的 PDF 文件：使用默认的 PDF 阅读器打开
    run_file_by_default_app(new_pdf_file_path)
    return

def is_pdf(pdf_file_path):
    return os.path.isfile(pdf_file_path) and pdf_file_path.lower().endswith(".pdf")


if __name__ == "__main__":
    main()
