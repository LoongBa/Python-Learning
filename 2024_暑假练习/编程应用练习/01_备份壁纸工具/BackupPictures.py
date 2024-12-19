# 备份壁纸工具
# 主要功能：把 Windows 11 系统里的锁屏壁纸、桌面壁纸被分到指定的文件夹。
# Version 1.0
# 作者：loongba

# 分解步骤：
# 1. 获取要备份的图片所在的位置——图片的来源目录
# 2. 获取要备份到那里去的位置——备份的目标目录
# 3. 从来源目录，把每个文件复制到目标目录
# 4. 复制完成，用资源管理器打开目标目录，并提示

import os
import sys
import shutil

# 1. 获取要备份的图片所在的位置——图片的来源目录
def get_pictures_source_folder():

    return "2024_暑假练习/编程应用练习/01_备份壁纸工具/Assets"

# 2. 获取要备份到那里去的位置——备份的目标目录
def get_pictures_destination_folder():

    return "2024_暑假练习/编程应用练习/01_备份壁纸工具/Backup"

# 3. 从来源目录，把每个文件复制到目标目录
def copy_pictures(source_folder, destination_folder):
    # 遍历 source_folder 将每一个文件复制到 destination_folder
    dirs_and_files = os.listdir(source_folder)
    for file in dirs_and_files:
        #source_filename = source_folder + "/" + file   # 硬编码，不推荐
        source_file_path = os.path.join(source_folder, file) # 推荐，与系统无关的方法
        if os.path.isdir(source_file_path): # 如果是文件夹，跳过
            continue
        destination_file_path = os.path.join(destination_folder, file)
        shutil.copy2(source_file_path, destination_file_path)

    return

# 打开文件夹
def open_folder(pictures_destination_folder):

    return

# 4. 复制完成，用资源管理器打开目标目录，并提示
def main():
    # 1. 获取要备份的图片所在的位置——图片的来源目录
    pictures_source_folder = get_pictures_source_folder()

    # 2. 获取要备份到那里去的位置——备份的目标目录
    pictures_destination_folder = get_pictures_destination_folder()

    # 3. 从来源目录，把每个文件复制到目标目录
    copy_pictures(pictures_source_folder, pictures_destination_folder)

    # 4. 复制完成，用资源管理器打开目标目录，并提示
    print(f"备份完成！")
    print(f"\tFrom:{pictures_source_folder}")
    print(f"\tTo:{pictures_destination_folder}")
    # 打开文件夹
    open_folder(pictures_destination_folder)

    return

if __name__ == "__main__":
    main()