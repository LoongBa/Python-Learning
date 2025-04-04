# 拆分动态照片 MotionPhoto
# 主要功能：
# 将一个动态照片文件拆分为静态照片和视频两个文件。
# 作者：loongba
# 时间：2024-07-27
# 版本：    
#       v1.0     2024-12-11 完成主要功能
#       v1.1     2024-12-12 修改bug
#       v1.2     2024-12-14 完善细节：用资源管理器打开文件夹时，兼容不同情况；拆分文件时，返回错误信息

# 主要步骤：
# 1. 获取要拆分的动态照片文件的完整路径
# 2. 读取文件内容，搜索关键字以找到要拆分的位置
# 3. 读取几个部分的数据，分别保存为 jpg 和 mp4 文件（注意文件命名规则）
# 4. 输出信息，自动打开保存拆分后文件的文件夹

import os
import sys

# 读取文件内容，搜索关键字以找到要拆分的位置
# 读取几个部分的数据，分别保存为 jpg 和 mp4 文件（注意文件命名规则）
def save_split_files(motion_pitcture_path):
    # 检查参数，确保文件存在
    if not os.path.isfile(motion_pitcture_path):
        return None, f"文件 {motion_pitcture_path} 不存在，或不是文件。"

    # 以二进制方式读取文件内容
    with open(motion_pitcture_path, "rb") as f:
        file_content = f.read()

    # 在读取的内容中搜索指定的二进制值，找到其位置，保存为变量 jpg_pos_end
    keywords = b"\xFF\xD9\x00\x00" #图片内容结束标识
    jpg_pos_end = file_content.find(keywords)
    if jpg_pos_end == -1:
        return None, "文件内容中未找到图片结束标识，无法拆分。"

    # 在读取的内容中搜索指定的二进制值，找到其位置，保存为变量 mp4_pos_start
    keywords = b"\x00\x00\x00\x18\x66\x74\x79\x70" #视频内容开头标识
    mp4_pos_start = file_content.find(keywords)
    if mp4_pos_start == -1:
        return None, "文件内容中未找到视频开始标识，无法拆分。"

    # 将从开始到 jpg_pos_end 的数据，保存为文件 jpg_file_path
    jpg_content = file_content[:jpg_pos_end + len(keywords)] # 语法糖
    # "D:\_Dev_\_Repos_\Github\_CoffeeScholar_\Python-Learning\2024_暑假练习\编程应用练习\02_拆分动态照片\20230612_161417.jpg"
    jpg_file_path = motion_pitcture_path.replace(".jpg", "_Photo.jpg")

    # 语法糖
    with open(jpg_file_path, "wb") as file:
        file.write(jpg_content)

    # 将从 mp4_pos_start 到结束的数据，保存为文件 mp4_file_path
    mp4_content = file_content[mp4_pos_start:]
    mp4_file_path = motion_pitcture_path.replace(".jpg", "_Movie.mp4")
    with open(mp4_file_path, "wb") as file:
        file.write(mp4_content)

    return jpg_file_path, mp4_file_path

# 打开保存拆分后文件的文件夹
def open_file_explorer_by_folder(folder_path):
    # 判断是否为绝对路径
    if not os.path.isabs(folder_path):
        # 把相对路径转换为绝对路径
        folder_path = os.path.abspath(folder_path)

    # 判断是否是文件夹
    if os.path.isfile(folder_path):
        # 取文件所在目录
        folder_path = os.path.dirname(folder_path)

    # 判断是否是 Mac 系统
    if os.name == "posix":
        os.system(f"open {folder_path}")
    elif os.name == "nt":
        # 如果是 Windows 系统，使用 start explorer
        os.system(f"start explorer {folder_path}")
    else:
        pass # do nothing

    return

def get_motion_pitcture_path():
    #path = "D:/_Dev_/_Repos_/Github/_CoffeeScholar_/Python-Learning/2024_暑假练习/编程应用练习/02_拆分动态照片/20230612_161417.jpg"
    #print(sys.argv)
    path = ""
    script_name = os.path.basename(sys.argv[0])
    #script_name = os.path.basename(__file__)
    if len(sys.argv) < 2:
        print("请提供动态照片文件的完整路径")
        print(f"例如：{script_name} 20230612_161417.jpg")
        sys.exit(1)
    else:
        path = sys.argv[1]

    if os.path.isfile(path) and path.endswith(".jpg"):
        return path
    else:
        print(f"所提供的参数不是有效的文件，或不是 JPG 文件：'{path}'")
        sys.exit(1)

    return path

def main():
    # 1. 获取要拆分的动态照片文件的完整路径
    motion_pitcture_path = get_motion_pitcture_path()
    # 2. 读取文件内容，搜索关键字以找到要拆分的位置
    # 3. 读取几个部分的数据，分别保存为 jpg 和 mp4 文件（注意文件命名规则）
    jpg_file_path, mp4_file_path = save_split_files(motion_pitcture_path)
    if jpg_file_path is None:
        print("拆分失败：", mp4_file_path)
        return
    
    # 4. 输出信息，自动打开保存拆分后文件的文件夹
    print("拆分文件 '{motion_pitcture_path}' 为：\n\t{jpg_file_path}\n\t{mp4_file_path}")
    open_file_explorer_by_folder(motion_pitcture_path)
    return

if __name__ == "__main__":
    main()