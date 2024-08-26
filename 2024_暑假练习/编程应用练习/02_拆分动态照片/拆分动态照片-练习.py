# 拆分动态照片工具 Motion Photo Splitter
# 主要功能：
# 把指定的动态照片的静态照片和视频拆分为两个单独的文件。
# 作者：loongba
# 时间：2024-07-27
# 版本：v1.0

# 主要步骤：
# 1. 获取要拆分的动态照片文件的完整路径
# 2. 读取文件内容，搜索关键字以找到要拆分的位置
# 3. 将拆分位置前后部分，分别保存为 jpg 和 mp4 文件
# 4. 输出信息，自动打开保存拆分后文件的文件夹

import sys
import os

# 从传入的参数获取动态照片完整路径
def get_photo_file_path():
    if len(sys.argv) < 2:
        print("请提供要拆分的动态照片文件路径")
        sys.exit(1)
    # 取传入的第一个参数作为文件路径
    photo_file_path = sys.argv[1]
    if not os.path.isfile(photo_file_path):
        print(f"文件不存在：{photo_file_path}")
        sys.exit(1)
    return photo_file_path

# 拆分动态照片为静态照片和视频文件，默认保存在动态照片所在目录
# 注意，此函数没有检查参数是否有效，没有对文件操作做错误处理，以后学习处理异常
def split_motion_photo_into_files(photo_file_path):
    # 2. 读取文件内容，搜索关键字以找到要拆分的位置
    with open(photo_file_path, 'rb') as file:# 二进制模式读取文件内容
            file_content = file.read()      # 读取所有内容为二进制数组
    keywords = b"\x00\x00\x00\x18\x66\x74\x79\x70" # 视频内容开头标识
    position = file_content.find(keywords)  # 搜索关键字的位置
    if position == -1:
        print(f"未找到关键字 '{keywords}'，无法拆分文件。")
        return None # 注意判断返回值

    # 3. 将拆分位置前后部分，分别保存为 jpg 和 mp4 文件
    jpg_content = file_content[0:position]  # 静态照片内容：从开始到关键字前
    mp4_content = file_content[position:]   # 视频内容：从关键字到结束（含关键字）
    # 分别保存为 jpg 和 mp4 文件，文件名为原动态照片文件名加后缀
    jpg_file_path = photo_file_path.replace(".jpg", "_Photo.jpg")
    mp4_file_path = photo_file_path.replace(".jpg", "_Video.mp4")
    with open(jpg_file_path, 'wb') as jpg_file:
            jpg_file.write(jpg_content)
    with open(mp4_file_path, 'wb') as mp4_file:
            mp4_file.write(mp4_content)
    return os.path.dirname(photo_file_path) # 返回拆分后文件所在的文件夹路径

# 用资源管理器打开指定的文件夹 
# 注意：现阶段并未检查参数的有效性，也未判断当前操作系统是否 Windows
def open_folder_by_explorer(folder_path):
    # 用资源管理器打开指定文件夹
    os.system(f"explorer.exe {folder_path}") 
    return

def main():
    # 1. 获取要拆分的动态照片文件的完整路径
    photo_file_path = get_photo_file_path()
    # 2. 读取文件内容，搜索关键字以找到要拆分的位置
    # 3. 将拆分位置前后部分，分别保存为 jpg 和 mp4 文件
    output_folder = split_motion_photo_into_files(
        photo_file_path)
    if output_folder is None:
        print("拆分动态照片失败：未找到关键字 'ftype'，可能不是动态照片。")
        return
    # 4. 输出信息，自动打开保存拆分后文件的文件夹
    open_folder_by_explorer(output_folder)
    return

if __name__ == '__main__':
    main()
