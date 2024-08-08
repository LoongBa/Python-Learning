# 拆分动态照片 MotionPhoto
# 主要功能：
# 将一个动态照片文件拆分为静态照片和视频两个文件。
# 作者：loongba
# 时间：2024-07-27
# 版本：v1.0
#       V1.1    2024-07-28: 加入对当前脚本所在目录下所有 jpg 文件的处理
#       V1.2    2024-07-28: 使用命令行参数：可以指定要处理的目录，否则对当前脚本所在目录进行处理
#       V1.3    2024-07-28: 加入颜色控制符

# 自顶向下，逐层分解步骤：
# 1. 获取要拆分的动态照片文件的完整路径
# 2. 读取文件内容，搜索关键字以找到要拆分的位置
# 3. 将拆分位置前后部分，分别保存为 jpg 和 mp4 文件
# 4. 输出信息，自动打开保存拆分后文件的文件夹

import os
import sys
import win32gui
import win32process

def do_with_motion_photo_file(filename, keyword = "MotionPhoto_Data", sub_folder_name = "_Output_"):
# 读取文件内容
    try:

        with open(filename, 'rb') as f:
            file_content = f.read()

        folder = os.path.dirname(filename)  # directory name
        # 搜索关键字以找到要拆分的位置
        split_pos = file_content.find(keyword.encode())

        # 将拆分位置前后部分，分别保存为 jpg 和 mp4 文件
        if split_pos != -1:
            jpg_content = file_content[:split_pos]
            mp4_content = file_content[split_pos + len(keyword):]

            filename = os.path.basename(filename)
            jpg_filename = filename.replace(".jpg", "_Photo.jpg")
            mp4_filename = filename.replace(".jpg", "_Video.mp4")

            sub_folder = os.path.join(folder, sub_folder_name)
            if not os.path.exists(sub_folder):
                os.mkdir(sub_folder)

            # 在子目录下新建文件
            with open(os.path.join(sub_folder, jpg_filename), 'wb') as f:
                f.write(jpg_content)
            # 在子目录下新建文件
            with open(os.path.join(sub_folder, mp4_filename), 'wb') as f:
                f.write(mp4_content)
        else:
            #print(f"\033[33m没有找到关键字：\"{keyword}\"，文件 \"{filename}\" 可能不是动态照片。\033[0m")
            return None, None, None
    except Exception as e:
        print(f"\033[31mdo_with_motion_photo_file() 出错：{e}\033[0m")
        return None, None, None

    return sub_folder, jpg_filename, mp4_filename

# 
def do_with_motion_photo_in_folder(folder_path, keyword = "MotionPhoto_Data", sub_folder_name = "_Output_"):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".jpg"):
            fullpath = os.path.join(folder_path, filename)
            if os.path.isfile(fullpath):
                sub_folder, jpg_filename, video_filename = do_with_motion_photo_file(fullpath, keyword, sub_folder_name)
                if sub_folder == None:
                    print(f"\033[33m{filename} 文件并非动态照片。\033[0m")
                else:
                    saved_folder = sub_folder
                    print(f"\033[32m拆分 {filename} 为 {jpg_filename} 和 {video_filename}\033[0m")
    return saved_folder

# 用资源管理器打开指定的文件夹
def start_file_or_open_folder(file_or_folder_path):
    if not file_or_folder_path :
        return
    if os.path.isdir(file_or_folder_path) and not is_explorer_window_open(file_or_folder_path):
        os.system("explorer /select," + file_or_folder_path)
    else:
        os.startfile(file_or_folder_path)
    return

def is_explorer_window_open(folder_path):
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            class_name = win32gui.GetClassName(hwnd)
            if class_name == "CabinetWClass":
                extra['found'] = True
                window_text = win32gui.GetWindowText(hwnd)
                print(f"\033[33mExplorer.exe \t{window_text}\033[0m")

                return False  # Stop enumeration
        return True  # Continue enumeration

    extra = {'found': False}
    win32gui.EnumWindows(callback, extra)
    return extra['found']    

def main():
    # 获取命令行参数
    if len(sys.argv) > 1:   # 如果有参数，则以第一个参数作为来源文件夹
        pictures_folder = sys.argv[1]
        if not os.path.isdir(pictures_folder):
            print(f"\033[31m请提供有效的路径，参数 \"{pictures_folder}\" 不是有效的路径。\033[0m")
            return  # 结束主函数
    else:
        pictures_folder = os.path.dirname(os.path.realpath(__file__))

    # 1. 获取要拆分的动态照片文件的完整路径
    # 遍历当前文件夹，对其中所有 jpg 文件进行处理
    output_folder = do_with_motion_photo_in_folder(pictures_folder)  # current work directory
    # 用资源管理器打开保存拆分后文件的文件夹
    start_file_or_open_folder(output_folder)
    
    return

if __name__ == "__main__":
    main()