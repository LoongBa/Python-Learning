# 备份壁纸工具
# 主要功能：把 Windows 11 系统里的锁屏壁纸、桌面壁纸被分到指定的文件夹。
# Version 1.0
# 作者：loongba

# 分解步骤：
# 1. 获取要备份的图片所在的位置——图片的来源目录
# 2. 获取要备份到那里去的位置——备份的目标目录
# 3. 从来源目录，把每个文件复制到目标目录
# 4. 复制完成，用资源管理器打开目标目录，并提示

#History
#   Ver 1.0 2024-08-05 备份壁纸到目标目录

#TODO:
#   Ver 1.1 备份锁屏壁纸到目标目录
#   Ver 1.2 优化：检查文件是否重复，忽略重复文件
#   Ver 1.3 优化：计算文件 Hash 值，用于判断是否重复
#   Ver 1.4 增加运行日志，以便用于任务计划自动运行时掌握运行状态
#   Ver 1.5 优化：增加数据文件，避免重复计算文件 Hash 值

from pathlib import Path
import os

def get_wallpaper_folder()-> str:
    """
    获取 Windows 壁纸文件夹的路径。

    返回值：
    - str: 壁纸文件夹的路径。

    异常：
    - 如果在获取壁纸文件夹路径时发生错误，将打印错误信息并返回 None。
    """
    try:
        #%USERPROFILE%\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets
        #%LOCALAPPDATA%\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets
        # 构造壁纸文件夹的路径，使用环境变量 %LOCALAPPDATA% 来获取用户目录
        wallpaper_dir = Path(os.environ['LOCALAPPDATA']) / r'Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
        return str(wallpaper_dir)
    except Exception as e:
        print(f"获取壁纸文件夹路径时发生错误: {e}")
        return None


def get_backup_folder():
    
    return

def backup_wallpaper_files(wallpaper_folder, backup_folder):
    
    return

def open_file_explorer_by_folder(backup_folder):

    return

def main():
    # 1. 获取要备份的图片所在的位置——图片的来源目录
    wallpaper_folder = get_wallpaper_folder()
    # 2. 获取要备份到那里去的位置——备份的目标目录
    backup_folder = get_backup_folder()
    # 3. 从来源目录，把每个文件复制到目标目录
    backup_wallpaper_files(wallpaper_folder, backup_folder)
    # 4. 复制完成，用资源管理器打开目标目录，并提示
    open_file_explorer_by_folder(backup_folder)
    return

if __name__ == "__main__":
    main()
