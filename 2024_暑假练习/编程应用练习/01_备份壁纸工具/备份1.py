# 备份壁纸工具
# 主要功能： 备份壁纸到指定文件夹
# version 1.1

# 分解步骤：
# 1. 获取要备份的图片所在位置
# 2. 获取备份的目标位置
# 3. 从来源位置复制图片到目标位置
# 4. 用资源管理器打开目标位置，并提示备份完成

# History:
# Ver 1.1 2024-12-19 增强了 copy_files() 方法：添加两个参数，允许指定扩展名和关键字
#TODO:
# Ver 1.2 
    # 1. 一些小细节的改进：彩色输出、记录运行日志
    # 2. 读取图片信息，用于构造目标文件名，并保存到不同的目录，例如：2024年10月、2024年11月、2024年12月
    #     判断重复：已经复制过的文件，就不再复制
    # 3. 判断重复的方法升级：使用 Hash 值判断，提高准确性
    # 4. 判断重复的方法升级：使用记录文件，优化性能


import os
import sys
import shutil

# 1. 获取要备份的图片所在位置
# 2. 获取备份的目标位置
def get_file():
    script_name = os.path.basename(sys.argv[0])
    if len(sys.argv) < 3:
        print(f"Usage: python {script_name} <source_directory> <target_directory>")
        sys.exit(1)
    source_directory = sys.argv[1]
    target_directory = sys.argv[2]
    return source_directory, target_directory

# 3. 从来源位置复制文件到目标位置
def copy_files(source_folder, target_folder, extension_filters = [], keywords = None):
    # 支持的图片文件扩展名
    if extension_filters is not None and len(extension_filters) > 0:
        # 确保 extension_filters 里的元素都是小写
        image_extensions = [ext.lower() for ext in extension_filters]
        #image_extensions = (ext.lower() for ext in extension_filters)
    else:   # 未指定参数 extension_filters 的值时，过滤图片
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        #image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')——元组
        # 可枚举类型/带有迭代器——通过迭代器获取下一个元素：【遍历】——比如，遍历链表：通过 Next 指针获取下一个元素的地址
        #C11/C++11 引入了 'for in'

        # []、()、{} 三种数据结构，都是可枚举类型，都可以用于遍历
        #for image_ext in image_extensions:

    # 获取目录中的所有文件
    files = os.listdir(source_folder)

    # 根据关键字过滤
    if keywords is not None:
        files_filted = [file for file in files if keywords.lower() in file.lower()]
    else:
        files_filted = files

    if extension_filters is not None:
        files_filted = [file for file in files_filted if os.path.splitext(file)[1].lower() in image_extensions]

    # 遍历source_file，将每一个文件复制到target_file
    for image_file in files_filted:
        source_file_path = os.path.join(source_folder, image_file)
        target_file_path = os.path.join(target_folder, image_file)
        shutil.copy2(source_file_path, target_file_path)
    return

# 4. 用资源管理器打开目标位置，并提示备份完成
def open_file(file):
    # 检查文件夹是否存在
    if not os.path.isdir(file):
        print(f"文件夹不存在: {file}")
        sys.exit(1)
    else:
        # 如果是Mac系统
        if os.name == "posix":
            os.system(f"open {file}")
            return
        # 如果是Windows系统
        if os.name == "nt":
            os.system(f"start explorer {file}")
    return



def main():
    # 1. 获取要备份的图片所在位置
    # 2. 获取备份的目标位置
    picture_sourse_file, picture_target_file = get_file()
    # 3. 从来源位置复制图片到目标位置
    copy_files(picture_sourse_file, picture_target_file)
    # 4. 用资源管理器打开目标位置，并提示备份完成
    open_file(picture_target_file)

    return

if __name__ == "__main__":
    main()


