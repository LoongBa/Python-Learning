import argparse
import os
from tqdm import tqdm
import fitz
from PIL import Image
from PIL import ImageEnhance


def is_image_pdf(pdf_path):
    """
    判断PDF文件是否为图像PDF

    参数:
    - pdf_path (str): PDF文件的路径

    返回值:
    - bool: 是否为图像PDF的布尔值
    """
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        page = doc[i]
        if page.get_text() != "":
            return False
        if len(page.get_images(full=True)) == 0:
            return False
    return True


def split_pdf_images(pdf_path: str) -> tuple:
    """
    将PDF文件拆分为单页图像文件

    参数:
    - pdf_path (str): PDF文件的路径

    返回值:
    - tuple: 操作是否成功的布尔值和图像文件夹的路径
    """
    folder_name = os.path.join(
        os.path.dirname(pdf_path), os.path.splitext(os.path.basename(pdf_path))[0]
    )
    os.makedirs(folder_name, exist_ok=True)

    doc = fitz.open(pdf_path)

    i = 0
    for page_num in tqdm(
        range(len(doc)),
        desc="拆分PDF为图像文件",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
    ):
        page = doc[page_num]
        pix = page.get_pixmap()
        image_path = os.path.join(folder_name, f"Image_{page_num:03d}.png")
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image.save(image_path, "png", quality=100)

        # 测试只拆分前三页
        i += 1
        if i == 3:
            break

    return True, folder_name


def enhance_image(
    image_path: str,
    enhanced_image_path: str,
    enhance_technique: dict = {"Contrast": 1.2, "Brightness": 1.2, "Sharpness": 1},
) -> bool:
    """
    增强单个图像文件的对比度、亮度和锐度

    参数:
    - image_path (str): 原始图像文件的路径
    - enhanced_image_path (str): 增强后的图像文件的路径
    - enhance_technique (dict): 增强技术参数，包括对比度、亮度和锐度，默认值为{"Contrast": 1.5, "Brightness": 1.5, "Sharpness": 1.5}

    返回值:
    - bool: 操作是否成功的布尔值
    """
    enhanced_image = Image.open(image_path)

    contrast = enhance_technique.get("Contrast", 1)
    if contrast != 1:
        enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(contrast)

    brightness = enhance_technique.get("Brightness", 1)
    if brightness != 1:
        enhanced_image = ImageEnhance.Brightness(enhanced_image).enhance(brightness)

    sharpness = enhance_technique.get("Sharpness", 1)
    if sharpness != 1:
        enhanced_image = ImageEnhance.Sharpness(enhanced_image).enhance(sharpness)

    # 按原始画质保存图像
    enhanced_image.save(enhanced_image_path, quality=100)
    return True


def enhance_images_in_folder(
    folder_path: str,
    enhance_technique: dict = {"Contrast": 1.2, "Brightness": 1.2, "Sharpness": 1},
) -> tuple:
    """
    增强文件夹中的所有图像文件的对比度、亮度和锐度

    参数:
    - folder_path (str): 图像文件夹的路径

    返回值:
    - tuple: 操作是否成功的布尔值和增强的图像文件数量
    """
    image_files = [
        file
        for file in os.listdir(folder_path)
        if file.lower().endswith((".png", ".jpg", ".jpeg"))
        and file.startswith("Image_")
    ]

    for index, image_file in tqdm(
        enumerate(image_files),
        total=len(image_files),
        desc="增强图像文件",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
    ):
        image_path = os.path.join(folder_path, image_file)
        enhanced_image_file = f"Enhanced_{image_file}"
        enhanced_image_path = os.path.join(folder_path, enhanced_image_file)
        enhance_image(image_path, enhanced_image_path, enhance_technique)

    return True, len(image_files)


def merge_images_to_pdf(folder_path: str, output_pdf_path: str) -> tuple:
    """
    将文件夹中的图像文件合并为PDF文件

    参数:
    - folder_path (str): 图像文件夹的路径
    - output_pdf_path (str): 输出PDF文件的路径

    返回值:
    - tuple: 操作是否成功的布尔值和输出PDF文件的路径
    """
    pdf_writer = fitz.open()

    # 需要合并的图像文件名列表
    image_files = [
        file
        for file in os.listdir(folder_path)
        if file.lower().endswith(".png") and file.startswith("Enhanced_")
    ]

    # 按照文件名排序
    image_files = sorted(image_files)

    # 逐个合并图像文件
    for image_file in tqdm(
        image_files,
        desc="合并图像为PDF文件",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
    ):
        image_path = os.path.join(folder_path, image_file)
        page = pdf_writer.new_page()
        

    pdf_writer.save(output_pdf_path)

    return True, output_pdf_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF 文件增强")
    parser.add_argument("pdf_file", type=str, help="PDF 文件的路径", nargs="?", default="X:\__学习资源__\软件开发\_算法和数据结构_\趣学算法_陈小玉_9787115459572 (Z-Library).pdf")
    parser.add_argument(
        "output_pdf_file", type=str, help="增强后的 PDF 文件的路径", nargs="?"
    )
    parser.add_argument("--constract", type=float, help="对比度增强参数", default=1.5)
    parser.add_argument("--brightness", type=float, help="亮度增强参数", default=1.2)
    parser.add_argument("--sharpness", type=float, help="锐度增强参数", default=1)
    args = parser.parse_args()

    pdf_file = args.pdf_file
    contrast = args.constract
    brightness = args.brightness
    sharpness = args.sharpness
    output_pdf_file = args.output_pdf_file

    if os.path.exists(pdf_file) is False:
        print("PDF 文件不存在。")
        exit()

    if is_image_pdf(pdf_file):
        print("PDF 文件为图像 PDF，将增强文件中的图像。")
    else:
        print("PDF 文件不是图像 PDF，忽略。")
        exit()

    if output_pdf_file != None and os.path.exists(output_pdf_file) is True:
        print(f"输出 PDF 文件已存在，将覆盖该文件：{output_pdf_file}")
    else:
        print("未指定输出 PDF 文件，将使用默认文件名：")
        output_pdf_file = None

    # 如果提供了 output_pdf_file 参数，则使用该参数作为输出文件名，否则使用默认文件名
    enhanced_pdf_filename = os.path.splitext(os.path.basename(pdf_file))[0]
    enhanced_pdf_filename = f"{enhanced_pdf_filename}_enhanced.pdf"
    enhanced_pdf_filename = (
        enhanced_pdf_filename if output_pdf_file is None else output_pdf_file
    )
    print(f"\t增强后的 PDF 文件名为：{enhanced_pdf_filename}")

    succeed, images_folder_path = split_pdf_images(pdf_file)
    if succeed is False:
        print("拆分 PDF 文件失败。")
        exit()
    else:
        print(f"拆分 PDF 文件成功，输出图像文件到：{images_folder_path}")

    contrast = 1
    brightness = 1.2
    sharpness = 1
    print(f"开始增强图像，参数：\r\n\t对比度={contrast}，亮度={brightness}，锐度={sharpness}")
    succeed, files_count = enhance_images_in_folder(
        images_folder_path,
        {"Contrast": contrast, "Brightness": brightness, "Sharpness": sharpness},
    )
    if succeed is False:
        print("增强图像失败。")
        exit()
    else:
        print(f"增强图像成功，共计增强图像文件 {files_count} 个。")

    succeed, enhanced_pdf = merge_images_to_pdf(
        images_folder_path, enhanced_pdf_filename
    )
    if succeed is False:
        print("合并图像为 PDF 文件失败。")
    else:
        print(f"增强图像 PDF 成功：{enhanced_pdf}")
