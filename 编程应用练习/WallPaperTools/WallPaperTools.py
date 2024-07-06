# 编写程序，读取 Windows 11 壁纸目录下的文件
# 如果文件名结尾不是 jpg，则复制到当前目录下的 WallPapers 目录下，并改名为 .jpg
import os
import shutil
import datetime
import winreg
import argparse
import logging
import hashlib
import glob
from pathlib import Path
from PIL import Image

AutoOpenFolder = False

# 获取当前脚本的目录
script_dir = os.path.dirname(os.path.realpath(__file__))
# 设置日志文件路径
log_file = os.path.join(script_dir, 'task.log')

# 设置日志格式
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def calculate_file_hash(filename, hash_method=hashlib.sha256, bufsize=8192):
    """计算文件的 Hash 值"""
    hasher = hash_method()
    with open(filename, 'rb') as f:
        buffer = f.read(bufsize)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = f.read(bufsize)
    return hasher.hexdigest()

# 获取图片文件的高度和宽度,
def GetImageSize(filename):
    try:
        with Image.open(filename) as img:
            width, height = img.size
        return True, width, height
    except:
        return False, None, None


# 根据图片文件的高度、宽度、修改时间，构造文件名
def ComposeNewFilename(filename, prefix="WallPaper"):
    modifiedTime = os.path.getmtime(filename)
    modifiedTime = datetime.datetime.fromtimestamp(modifiedTime)
    succeed, width, height = GetImageSize(filename)
    if not succeed:
        print(f"\t\033[33m{filename} 不是图片文件，忽略。\033[0m")
        return None
    sizeString = f"{os.path.getsize(filename):,}"
    fileHash = calculate_file_hash(filename)[:8]  # 取 Hash 值的前八位
    newFilename = f"{prefix}_{modifiedTime.strftime('%Y%m%d_%H%M%S')}_{height}x{width}_{sizeString}_{fileHash}.jpg"
    yearAndMonthDir = modifiedTime.strftime("%Y%m")
    return newFilename, yearAndMonthDir

def CheckForDuplicateFiles(targetDir, filename:str):
    """使用搜索模式检查目录中是否有文件名中包含相同文件大小和 Hash 值前八位的文件"""
    targetFileInfo = filename.split("_")[-2:]  # 获取 "_460,010_b16625da"
    # 构造搜索模式
    searchPattern = f"*_{targetFileInfo[0]}_{targetFileInfo[1]}"   # "*_460,010_b16625da.jpg"
    # 在目标目录及子目录中搜索匹配的文件
    matchingFiles = glob.glob(str(targetDir / '**' / searchPattern), recursive=True)
    
    # 如果找到匹配的文件，则认为存在重复文件
    return len(matchingFiles) > 0

# 备份当前桌面图片 desktopWallPaperFilename 到目标目录下
def BackupDesktopWallPaper(targetDir):
    desktopWallPaperFilename = (
        os.getenv("APPDATA") + "\\Microsoft\\Windows\\Themes\\TranscodedWallpaper"
    )
    desktopWallPaperFilename = Path(desktopWallPaperFilename)

    # 构造备份文件名
    newFilename, subDir = ComposeNewFilename(desktopWallPaperFilename, "Desktop")

    # 创建目标目录，格式为当前月份
    backupDir = targetDir / subDir
    backupDir.mkdir(exist_ok=True)

    backupFilename = backupDir / newFilename
    # 检查目标文件夹是否已经存在同名文件
    if CheckForDuplicateFiles(targetDir, newFilename):
        print(f"\t桌面壁纸\t{newFilename}\t\033[34m已存在，忽略\033[0m")
    else:
        # 复制当前桌面图片到目标目录，并使用备份文件名
        shutil.copy2(desktopWallPaperFilename, backupFilename)
        print(f"\t桌面壁纸\t{newFilename}\t\033[32m备份完成\033[0m")
    print()
    return desktopWallPaperFilename.parent


# 备份锁屏壁纸到 targetDir 目录下
def BackupWallPapers(targetDir):
    # 读取环境变量 %USERPROFILE% 的值，用于构造完整路径
    wallpaperDir = (
        os.getenv("USERPROFILE")
        + "\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"
    )

    i = 0
    # 遍历壁纸目录中的文件
    for fileEntry in Path(wallpaperDir).iterdir():
        if fileEntry.is_file():
            filename = fileEntry.name
            extension = fileEntry.suffix

            # 检查文件扩展名是否不是 ".jpg"
            if extension != ".jpg":
                # 获取文件的创建日期
                print(f"{(i := i + 1):03}", "\t源文件: ", filename)
                # 构造新的文件名
                newFilename, subDir = ComposeNewFilename(fileEntry, "WallPaper")
                # 创建目标目录，格式为当前月份
                backupDir = targetDir / subDir
                backupDir.mkdir(exist_ok=True)

                print("\t     => ", newFilename, end="")
                newFilename = backupDir / newFilename

                # 将文件复制到目标目录，并使用新的文件名
                if CheckForDuplicateFiles(targetDir, newFilename.name):
                    print("\t\033[34m已存在，忽略\033[0m")
                else:
                    shutil.copy2(fileEntry, newFilename)
                    print("\t\033[32m备份完成\033[0m")
    return wallpaperDir


# 通过注册表信息，获取用户图片文件夹位置
def get_user_shell_folders():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders",
    )
    folders = dict(
        [(winreg.EnumValue(key, i)[:2]) for i in range(winreg.QueryInfoKey(key)[1])]
    )
    return folders.get("My Pictures")


def main():
    print("壁纸备份工具 V1.40 \n作者：xxx CopyRight 2024")
    print("---------------------------")
    print("自动备份锁屏壁纸、桌面壁纸到系统“我的图片”文件夹下，按年月创建子目录。支持指定备份目录。")
    print("新增基于 Hash 值避免重复文件。")
    print("TODO: 可以用已有图片替换桌面和锁屏壁纸。\n")
    logging.info('Script started')

    parser = argparse.ArgumentParser(description="壁纸工具")
    parser.add_argument("--open-source-folder", action="store_true", help="自动打开来源文件夹")
    parser.add_argument("--open-backup-folder", action="store_true", help="自动打开备份文件夹")
    # 添加一个新的参数用于指定备份目录，默认为用户的图片文件夹
    parser.add_argument(
        "backup_dir",
        nargs="?",
        type=Path,
        default=Path(get_user_shell_folders()) / "_WallPaper_Backup_",
        help="指定备份目录的路径，默认为系统“我的图片”文件夹下的_WallPaper_Backup_目录",
    )
    args = parser.parse_args()
    OpenSourceFolder = args.open_source_folder
    OpenBackupFolder = args.open_backup_folder
    # 使用用户指定的备份目录或默认值
    wallpaperBackupDir = args.backup_dir
    # 创建目标目录如果它不存在
    wallpaperBackupDir.mkdir(parents=True, exist_ok=True)

    # 创建目标目录如果它不存在（默认在当前目录下）
    # currentDir = Path.cwd()  # 获取当前目录
    # wallpaperBackupDir = currentDir / "_WallPaper_Backup_"
    # wallpaperBackupDir.mkdir(exist_ok=True)

    # 备份桌面壁纸
    desktopWallPaperDir = BackupDesktopWallPaper(wallpaperBackupDir)
    # 备份锁屏壁纸
    wallpaperDir = BackupWallPapers(wallpaperBackupDir)

    # 输出完整路径，后续仅输出文件名
    print("---------------------------")
    print("桌面壁纸所在位置：\t", desktopWallPaperDir)
    print("锁屏壁纸所在位置：\t", wallpaperDir)
    print("壁纸备份位置：\t\t", wallpaperBackupDir)
    print("---------------------------")

    # 执行命令，用资源管理器打开 备份文件夹
    if OpenBackupFolder:
        os.system("start " + str(wallpaperBackupDir))
    # 执行命令，用资源管理器打开 desktopWallPaperDir 文件夹
    if OpenSourceFolder:
        os.system("start " + desktopWallPaperDir)
        os.system("start " + wallpaperDir)

    logging.info('Script finished')
        
    return


if __name__ == "__main__":
    main()
