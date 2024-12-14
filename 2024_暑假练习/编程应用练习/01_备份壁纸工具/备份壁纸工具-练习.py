# 备份壁纸工具
# 主要功能：把 Windows 11 系统里的锁屏壁纸、桌面壁纸被分到指定的文件夹。
# Version 1.0
# 作者：loongba

# 分解步骤：
# 1. 获取要备份的图片所在的位置——图片的来源目录
# 2. 获取要备份到那里去的位置——备份的目标目录
# 3. 从来源目录，把每个文件复制到目标目录
# 4. 复制完成，用资源管理器打开目标目录,并提示

import os
import shutil
import winreg

# 获取 Windows 聚焦图片所在的路径
def get_windows_spotlight_images_path():
    appdata_folder = os.getenv("LOCALAPPDATA") # 获取环境变量的值
    source_folder = os.path.join(appdata_folder, "Packages", "Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy", "LocalState", "Assets")

    return source_folder

# 获取“我的图片”的路径
def get_windows_my_pictures():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        )
        my_pictures_path, _ = winreg.QueryValueEx(key, "My Pictures")
        # 如果路径包含环境变量（如 %USERPROFILE%），需要展开它
        my_pictures_path = os.path.expandvars(my_pictures_path)
        return my_pictures_path
    except Exception as e:
        print(f"读取注册表时出错：{e}")
        return None

# 备份来源目录下所有文件到指定目录
def backup_files_from(source_dir, backup_dir):
    bakcup_sub_dir = os.path.join(backup_dir, "_备份壁纸_")
    # 如果备份目录不存在，则创建
    if not os.path.exists(bakcup_sub_dir):
        os.mkdir(bakcup_sub_dir) # 对比 os.makedirs() 不需要判断
    # 获取来源目录的每一个子项
    files = os.listdir(source_dir)
    # 遍历来源目录的所有子项
    for filename in files:
        source_file_path = os.path.join(source_dir, filename)    # 拼接来源目录 和 文件名
        if not os.path.isfile(source_file_path):
            continue    # 如果是目录则跳过
        # 拼接目标目录 和 文件名，得到完整的目标文件路径
        dest_file_path = os.path.join(bakcup_sub_dir, filename + ".jpg") # destination 目标
        shutil.copy2(source_file_path, dest_file_path)
        print(f"复制文件: {source_file_path} 到 {dest_file_path}")
    return bakcup_sub_dir

# 用资源管理器打开指定目录
def open_dir_by_explorer(dir):
    os.system("explorer.exe " + dir)
    #os.startfile(dir)
    return

# 主程序
def main():
    # 1. 获取要备份的图片所在的位置——图片的来源目录
    source_dir = get_windows_spotlight_images_path()
    # 2. 获取要备份到那里去的位置——备份的目标目录，约定保存到 "我的照片" 目录下
    backup_dir = get_windows_my_pictures()
    # 3. 从来源目录，把每个文件复制到目标目录
    backup_dir = backup_files_from(source_dir, backup_dir)
    # 4. 复制完成，用资源管理器打开目标目录，并提示
    open_dir_by_explorer(backup_dir)
    return

# 用于判断当前脚本是不是被单独运行，还是被其它脚本调用
if __name__ == "__main__":
    main()