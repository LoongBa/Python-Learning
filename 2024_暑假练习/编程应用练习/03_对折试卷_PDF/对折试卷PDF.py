# 对折试卷 PDF 工具
# 主要功能：将 A3 幅面的 PDF 试卷对半对折为 A4 幅面的 PDF
# 作者：loonba
# 版本号：Ver1.6

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
# V1.4 增加奇偶页不同剪裁参数，自动识别密封线和中线位置
# V1.5 优化剪裁参数逻辑，支持奇偶页专用参数覆盖通用参数
# V1.6 增加自动去除四周花边功能（--auto-crop-border）；增强自动检测密封线/中线算法（动态阈值+Otsu-like+prominence过滤）；新增 auto_crop_borders 函数

import sys
import os
import argparse
import numpy as np
from PIL import Image, ImageFilter
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

# 自动识别密封线位置（增强版）
def detect_seam_line(page_image: Image.Image) -> int:
    # 将图像转换为灰度
    gray_image = page_image.convert('L')
    # 转换为numpy数组
    img_array = np.array(gray_image)
    
    # 增强：动态阈值二值化（Otsu-like）
    flat = img_array.flatten()
    threshold = np.percentile(flat, 85)
    binary = (img_array < threshold).astype(np.uint8) * 255
    
    # 边缘检测（Sobel）
    from scipy.ndimage import sobel
    edge_horizontal = sobel(binary, axis=1)  # 水平边缘
    
    # 投影分析
    # 计算每列的边缘强度
    edge_projection = np.sum(np.abs(edge_horizontal), axis=0)
    
    # 平滑处理
    from scipy.ndimage import gaussian_filter1d
    smoothed_projection = gaussian_filter1d(edge_projection, sigma=2)
    
    # 寻找边缘强度较高的区域（增强：prominence过滤）
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(smoothed_projection, 
                          height=np.mean(smoothed_projection) + 1.5 * np.std(smoothed_projection),
                          prominence=0.15 * np.max(smoothed_projection))
    
    # 根据位置判断是左侧密封线还是右侧密封线
    width = page_image.width
    left_region = width // 4
    right_region = 3 * width // 4
    
    left_peaks = [p for p in peaks if p < left_region]
    right_peaks = [p for p in peaks if p > right_region]
    
    # 选择最可能的密封线位置
    if left_peaks and right_peaks:
        # 如果两侧都有可能的密封线，选择边缘强度更高的
        left_max = max(left_peaks, key=lambda p: smoothed_projection[p])
        right_max = max(right_peaks, key=lambda p: smoothed_projection[p])
        
        if smoothed_projection[left_max] > smoothed_projection[right_max]:
            return left_max
        else:
            return right_max
    elif left_peaks:
        return max(left_peaks, key=lambda p: smoothed_projection[p])
    elif right_peaks:
        return max(right_peaks, key=lambda p: smoothed_projection[p])
    else:
        # 没有找到明显的密封线
        return -1

# 自动识别中线位置（支持两版和三版布局）（增强版）
def detect_center_line(page_image: Image.Image) -> tuple:
    # 将图像转换为灰度
    gray_image = page_image.convert('L')
    # 转换为numpy数组
    img_array = np.array(gray_image)
    
    # 1. 增强：动态阈值
    flat = img_array.flatten()
    content_threshold = np.percentile(flat, 80)
    
    # 基于内容密度
    content_density = np.mean(img_array < content_threshold, axis=0)
    
    # 2. 基于水平投影的方法
    column_means = np.mean(img_array, axis=0)
    
    # 3. 结合两种方法（权重调整）
    combined_score = 0.8 * (1 - content_density) + 0.2 * column_means
    
    # 4. 平滑处理
    from scipy.ndimage import gaussian_filter1d
    smoothed_score = gaussian_filter1d(combined_score, sigma=3)
    
    # 5. 寻找局部最小值（增强：prominence + distance）
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(-smoothed_score, distance=50, prominence=0.1 * np.ptp(smoothed_score))
    
    # 6. 根据页面宽度判断是两版还是三版
    width = page_image.width
    if len(peaks) >= 2:
        # 可能是三版布局
        sorted_peaks = sorted(peaks)
        # 找到最接近1/3和2/3位置的峰值
        third_width = width // 3
        peak1 = min(sorted_peaks, key=lambda x: abs(x - third_width))
        peak2 = min(sorted_peaks, key=lambda x: abs(x - 2 * third_width))
        # 距离检查防误判
        if abs(peak2 - peak1) < width // 4:
            return (width // 2, None)
        return (peak1, peak2)
    elif len(peaks) == 1:
        # 可能是两版布局
        return (peaks[0], None)
    else:
        # 没有找到明显的分割线，使用默认的中点
        return (width // 2, None)

# 新增：自动去除四周花边（基于内容投影）
def auto_crop_borders(page_image: Image.Image, content_threshold: int = 240, min_content_pixels: int = 8) -> tuple[int, int, int, int]:
    """返回需剪裁的四边像素量 (left, top, right, bottom)"""
    gray = np.array(page_image.convert('L'))
    height, width = gray.shape
    
    # 列投影：每列非白像素数
    col_density = np.sum(gray < content_threshold, axis=0)
    # 行投影
    row_density = np.sum(gray < content_threshold, axis=1)
    
    # 左边：第一个有足够内容的列
    crop_left = 0
    for i in range(width):
        if col_density[i] > min_content_pixels:
            crop_left = i
            break
    
    # 右边：最后一个有内容的列
    crop_right = 0
    for i in range(width - 1, -1, -1):
        if col_density[i] > min_content_pixels:
            crop_right = width - 1 - i
            break
    
    # 上边
    crop_top = 0
    for i in range(height):
        if row_density[i] > min_content_pixels:
            crop_top = i
            break
    
    # 下边
    crop_bottom = 0
    for i in range(height - 1, -1, -1):
        if row_density[i] > min_content_pixels:
            crop_bottom = height - 1 - i
            break
    
    return crop_left, crop_top, crop_right, crop_bottom

# 提取 PDF 文件中的每一页为图像对象
def split_pdf(pdf_file_path: str, new_pdf_file_path: str, 
              crop_left=0, crop_right=0, crop_top=0, crop_bottom=0,
              crop_left_odd=0, crop_right_odd=0, crop_top_odd=0, crop_bottom_odd=0,
              crop_left_even=0, crop_right_even=0, crop_top_even=0, crop_bottom_even=0,
              offset_x=0, offset_y=0,
              margin_top=0, margin_bottom=0, margin_left=0, margin_right=0,
              auto_detect_seam=False, auto_detect_center=False,
              auto_crop_border=False) -> str:
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
        
        # 根据页码确定使用的剪裁参数
        if page_number % 2 == 1:  # 奇数页
            # 如果设置了奇数页专用参数，则使用奇数页专用参数，否则使用通用参数
            current_crop_left = crop_left_odd if crop_left_odd != 0 else crop_left
            current_crop_right = crop_right_odd if crop_right_odd != 0 else crop_right
            current_crop_top = crop_top_odd if crop_top_odd != 0 else crop_top
            current_crop_bottom = crop_bottom_odd if crop_bottom_odd != 0 else crop_bottom
        else:  # 偶数页
            # 如果设置了偶数页专用参数，则使用偶数页专用参数，否则使用通用参数
            current_crop_left = crop_left_even if crop_left_even != 0 else crop_left
            current_crop_right = crop_right_even if crop_right_even != 0 else crop_right
            current_crop_top = crop_top_even if crop_top_even != 0 else crop_top
            current_crop_bottom = crop_bottom_even if crop_bottom_even != 0 else crop_bottom
        
        # 新增：自动去除四周花边（加到当前剪裁量）
        if auto_crop_border:
            auto_l, auto_t, auto_r, auto_b = auto_crop_borders(page_image)
            current_crop_left += auto_l
            current_crop_top += auto_t
            current_crop_right += auto_r
            current_crop_bottom += auto_b
        
        # 自动检测密封线位置
        if auto_detect_seam:
            seam_line = detect_seam_line(page_image)
            # 调整剪裁参数以排除密封线
            if seam_line != -1:
                if seam_line < page_image.width // 2:
                    current_crop_left = max(current_crop_left, seam_line + 10)
                else:
                    current_crop_right = max(current_crop_right, page_image.width - seam_line + 10)
        
        # 自动检测中线位置
        if auto_detect_center:
            center_line1, center_line2 = detect_center_line(page_image)
            if center_line2 is not None:  # 三版布局
                # 将图像分为三部分
                image1 = page_image.crop((current_crop_left, current_crop_top, center_line1, page_image.height - current_crop_bottom))
                image2 = page_image.crop((center_line1, current_crop_top, center_line2, page_image.height - current_crop_bottom))
                image3 = page_image.crop((center_line2, current_crop_top, page_image.width - current_crop_right, page_image.height - current_crop_bottom))
                
                # 添加边距
                if margin_top > 0 or margin_bottom > 0 or margin_left > 0 or margin_right > 0:
                    image1 = add_margins(image1, margin_top, margin_bottom, margin_left, margin_right)
                    image2 = add_margins(image2, margin_top, margin_bottom, margin_left, margin_right)
                    image3 = add_margins(image3, margin_top, margin_bottom, margin_left, margin_right)
                
                # 添加到结果列表
                splited_images_list.extend([image1, image2, image3])
                print_color(f"\t\t成功对折第 {page_number} 页（三版布局）。")
                continue
        
        # 对折页对应的图片为两个图片，传入边距参数
        page_images_list = split_image_into_images(
            page_image, 
            current_crop_left, current_crop_right, current_crop_top, current_crop_bottom,
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

# 添加边距到图像
def add_margins(image: Image.Image, margin_top, margin_bottom, margin_left, margin_right) -> Image.Image:
    width, height = image.size
    
    # 创建带边距的新图像
    new_width = width + margin_left + margin_right
    new_height = height + margin_top + margin_bottom
    
    # 创建白色背景的新图像
    new_image = Image.new('RGB', (new_width, new_height), color='white')
    
    # 将原图粘贴到新图像上，保留边距
    new_image.paste(image, (margin_left, margin_top))
    
    return new_image

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
        image_left = add_margins(image_left, margin_top, margin_bottom, margin_left, margin_right)
        image_right = add_margins(image_right, margin_top, margin_bottom, margin_left, margin_right)

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
    
    # 通用剪裁参数（同时应用于奇数页和偶数页）
    parser.add_argument('-cl', '--crop-left', type=int, default=0, help='左边剪裁量（像素），默认为0')
    parser.add_argument('-cr', '--crop-right', type=int, default=0, help='右边剪裁量（像素），默认为0')
    parser.add_argument('-ct', '--crop-top', type=int, default=0, help='上边剪裁量（像素），默认为0')
    parser.add_argument('-cb', '--crop-bottom', type=int, default=0, help='下边剪裁量（像素），默认为0')
    
    # 奇数页专用剪裁参数（如果设置，则覆盖通用参数）
    parser.add_argument('-clo', '--crop-left-odd', type=int, default=0, help='奇数页左边剪裁量（像素），如果设置则覆盖通用参数')
    parser.add_argument('-cro', '--crop-right-odd', type=int, default=0, help='奇数页右边剪裁量（像素），如果设置则覆盖通用参数')
    parser.add_argument('-cto', '--crop-top-odd', type=int, default=0, help='奇数页上边剪裁量（像素），如果设置则覆盖通用参数')
    parser.add_argument('-cbo', '--crop-bottom-odd', type=int, default=0, help='奇数页下边剪裁量（像素），如果设置则覆盖通用参数')
    
    # 偶数页专用剪裁参数（如果设置，则覆盖通用参数）
    parser.add_argument('-cle', '--crop-left-even', type=int, default=0, help='偶数页左边剪裁量（像素），如果设置则覆盖通用参数')
    parser.add_argument('-cre', '--crop-right-even', type=int, default=0, help='偶数页右边剪裁量（像素），如果设置则覆盖通用参数')
    parser.add_argument('-cte', '--crop-top-even', type=int, default=0, help='偶数页上边剪裁量（像素），如果设置则覆盖通用参数')
    parser.add_argument('-cbe', '--crop-bottom-even', type=int, default=0, help='偶数页下边剪裁量（像素），如果设置则覆盖通用参数')
    
    # 偏移参数
    parser.add_argument('-xo', '--offset-x', type=int, default=0, help='X方向中线偏移量（像素），默认为0')
    parser.add_argument('-yo', '--offset-y', type=int, default=0, help='Y方向中线偏移量（像素），默认为0')
    
    # 边距参数
    parser.add_argument('-ml', '--margin-left', type=int, default=0, help='左边距（像素），默认为0')
    parser.add_argument('-mr', '--margin-right', type=int, default=0, help='右边距（像素），默认为0')
    parser.add_argument('-mt', '--margin-top', type=int, default=0, help='上边距（像素），默认为0')
    parser.add_argument('-mb', '--margin-bottom', type=int, default=0, help='下边距（像素），默认为0')
    
    # 自动检测参数
    parser.add_argument('-ads', '--auto-detect-seam', action='store_true', help='自动检测密封线位置')
    parser.add_argument('-adc', '--auto-detect-center', action='store_true', help='自动检测中线位置（支持两版和三版布局）')
    # 新增：自动去除四周花边
    parser.add_argument('-acb', '--auto-crop-border', action='store_true', help='自动去除四周花边（基于内容边界）')
    
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
        args.crop_left_odd, args.crop_right_odd, args.crop_top_odd, args.crop_bottom_odd,
        args.crop_left_even, args.crop_right_even, args.crop_top_even, args.crop_bottom_even,
        args.offset_x, args.offset_y,
        args.margin_top, args.margin_bottom, args.margin_left, args.margin_right,
        args.auto_detect_seam, args.auto_detect_center,
        args.auto_crop_border
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
