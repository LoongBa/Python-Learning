from isort import file
import os
import sys
import glob
from tqdm import tqdm

def split_jpg_motion_file(jpg_file_path, output_folder_path = None):
    """
    将JPG动态文件拆分为图像和视频部分。

    参数:
        jpg_file_path (str): JPG动态文件的路径。
        output_folder_path (str): 可选参数，用于指定保存拆分文件的文件夹。未指定输出文件夹，默认采用当前文件夹

    返回值:
        tuple: 包含以下元素的元组:
            - success (bool): 表示文件是否成功拆分。
            - photo_filename (str): 保存图像部分的文件名。
            - video_filename (str): 保存视频部分的文件名。
            - folder (str): 包含原始文件的文件夹。

            如果文件无法拆分，则元组将具有以下值:
            - success (bool): False
            - photo_filename (str): 空字符串
            - video_filename (str): 空字符串
            - folder (str): 空字符串
    """
    if not os.path.exists(jpg_file_path):
        return (False, "文件不存在。", "", "")
    
    if not jpg_file_path.endswith(".jpg"):
        return (False, "文件类型必须为：jpg", "", "")

    # 获取文件名和文件夹
    folder = os.path.dirname(jpg_file_path)
    if output_folder_path is None:  # 未指定输出文件夹，默认采用当前文件夹
        output_folder_path = folder

    # 生成保存文件名
    jpg_filename = os.path.basename(jpg_file_path)
    video_filename = jpg_filename.replace(".jpg", "_Video.mp4")
    photo_filename = jpg_filename.replace(".jpg", "_Photo.jpg")

    # 读取源文件
    with open(jpg_file_path, "rb") as file:
        content = file.read()

    # 查找字符串 "MotionPhoto_Data" 的位置
    Mark = b"MotionPhoto_Data"
    position = content.find(Mark)

    if position != -1:
        # 将内容分割为图像和视频部分
        image_content = content[:position]
        video_content = content[position + len(Mark):]

        # 将图像部分保存为 jpg 文件
        filename = os.path.join(output_folder_path, photo_filename)
        with open(filename, "wb") as image_file:
            image_file.write(image_content)

        # 将视频部分保存为 mp4 文件
        filename = os.path.join(output_folder_path, video_filename)
        with open(filename, "wb") as video_file:
            video_file.write(video_content)

        return (True, "No Error", jpg_filename, photo_filename, video_filename, output_folder_path)
    else:
        return (False, "文件中未找到字符串。", "", "", "")

def split_jpg_motion_files_in_folder(folder_path):
    """
    拆分给定文件夹中的JPG动态文件。

    参数:
        folder_path (str): 包含JPG文件的文件夹的路径。

    返回值:
        None
    """
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"文件夹不存在：\033[91m{folder_path}\033[0m")
        return
    
    # 在当前目录下创建子目录：Output
    output_folder_path = os.path.join(folder_path, "Output")
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    jpg_source_files = glob.glob(folder_path + "/*.jpg")

    results = []
    for jpg_file_path in tqdm(jpg_source_files, desc="拆分文件中"):
        result = split_jpg_motion_file(jpg_file_path, output_folder_path)
        results.append(result)

    return results

if __name__ == "__main__":

    # 读取命令行参数：filename
    if len(sys.argv) < 2:
        print("用法: python split_jpg_motion_file.py 文件名")
        #sys.exit(1)

    folder_path = "D:\\_Videos_\\_学校作业_\\2024_劳动实践"
    output_folder_path = os.path.join(folder_path, "Output")

    # 使用示例
    results = split_jpg_motion_files_in_folder(folder_path)
    if results:
        output_folder_path = results[0][5]

    # 统计成功的数量
    count_succeed = len([result for result in results if result[0] == True])
    # 统计失败的数量
    count_failed = len([result for result in results if result[0] == False])

    print(f"拆分完成 \033[94m{len(results)}\033[0m 个文件，\r\n\t来源目录：\033[94m{folder_path}\033[0m")
    print(f"\t输出目录：\033[94m{output_folder_path}\033[0m")
    print(f"\t成功拆分：\033[92m{count_succeed}\033[0m 个文件；")
    print(f"\t拆分失败：\033[91m{count_failed}\033[0m 个文件。")
    print()

    count = 0
    for result in results:
        count += 1

        print(f"{count:02d}\t源文件：\033[94m{result[2]}\033[0m")
        if result[0]:
            print(f"\t\033[92m分割成功：")
            print(f"\t\t{result[3]}\r\n\t\t{result[4]}\033[0m")
        else:
            print(f"\t\033[91m分割失败：{result[1]}\033[0m")