# 主要功能：备份 Windows 11 系统的锁屏壁纸图片，和 "Windows 聚焦" 的桌面壁纸图片到指定的目录。
# 作者：loongba
# 日期：2024-07-20
# 版本：1.0

# 第一步，先确认要备份的图片所在的路径
# 第二步，确认备份到哪里的路径——备份目录的路径
# 第三步，开始备份图片：将要备份的图片复制到备份目录中
# 第四步，备份完成后，给出提示信息，自动用文件管理器打开备份目录
import os       # Operating System，操作系统
import shutil

# 获取 Windows 11 系统的锁屏壁纸图片的位置
def get_windows_spotlight_images_path():
    # 获取当前用户名
    username = os.getenv('USERNAME')    # 从系统环境变量中获取当前用户名  get EnvironmentVariable 获取环境变量， Environment 环境， Variable 变量

    # 定义源文件夹和目标文件夹
    source_folder = fr"C:\Users\{username}\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
    #target_folder = fr"C:\Users\{username}\Desktop\WindowsSpotlightImages"
    return source_folder

# 获取当前用户的 "我的图片" 路径
# 复制文件夹中的文件到备份目录
def copy_files(source, destination):        # source 来源，destination 目标
    # 如果目标文件夹不存在，则创建 
    if not os.path.exists(destination):
        os.makedirs(destination)

    # 遍历源文件夹中的文件          Path，路径，目录
    for fileOrDirectory in os.listdir(source):         # list 列出，directory 目录，item 项（每一项）
        # 把 来源文件夹的路径 和 每一项的文件名或目录名 拼接为一个完整文件名
        sourceFullPath = os.path.join(source, fileOrDirectory)      # 要复制的源文件的完整路径          # join 加入、连接    
        destFullPath = os.path.join(destination, fileOrDirectory)   # 要复制到备份目录去的完整路径
        destFullPath = destFullPath + ".jpg"
        # 如果源文件夹中的文件是文件夹，则递归调用函数
        if not os.path.isdir(sourceFullPath):       # is Directory 判断是否是目录
            shutil.copy2(sourceFullPath, destFullPath)
            print(sourceFullPath, destFullPath)

    return    
    
# 复制文件夹中的文件到备份目录
def copy_files(source, destination):        # source 来源，destination 目标
    # 如果目标文件夹不存在，则创建 
    if not os.path.exists(destination):
        os.makedirs(destination)

    # 遍历源文件夹中的文件          Path，路径，目录
    for fileOrDirectory in os.listdir(source):         # list 列出，directory 目录，item 项（每一项）
        # 把 来源文件夹的路径 和 每一项的文件名或目录名 拼接为一个完整文件名
        sourceFullPath = os.path.join(source, fileOrDirectory)      # 要复制的源文件的完整路径          # join 加入、连接    
        destFullPath = os.path.join(destination, fileOrDirectory)   # 要复制到备份目录去的完整路径
        destFullPath = destFullPath + ".jpg"
        # 如果源文件夹中的文件是文件夹，则递归调用函数
        if not os.path.isdir(sourceFullPath):       # is Directory 判断是否是目录
            shutil.copy2(sourceFullPath, destFullPath)
            print(sourceFullPath, destFullPath)

    return    
    
# 复制文件夹中的文件到备份目录
def copy_files(source, destination):        # source 来源，destination 目标
    # 如果目标文件夹不存在，则创建 
    if not os.path.exists(destination):
        os.makedirs(destination)

    # 遍历源文件夹中的文件          Path，路径，目录
    for fileOrDirectory in os.listdir(source):         # list 列出，directory 目录，item 项（每一项）
        # 把 来源文件夹的路径 和 每一项的文件名或目录名 拼接为一个完整文件名
        sourceFullPath = os.path.join(source, fileOrDirectory)      # 要复制的源文件的完整路径          # join 加入、连接    
        destFullPath = os.path.join(destination, fileOrDirectory)   # 要复制到备份目录去的完整路径
        destFullPath = destFullPath + ".jpg"
        # 如果源文件夹中的文件是文件夹，则递归调用函数
        if not os.path.isdir(sourceFullPath):       # is Directory 判断是否是目录
            shutil.copy2(sourceFullPath, destFullPath)
            print(sourceFullPath, destFullPath)

    return    
    
def get_my_pictures_path():
    return os.path.join(os.path.expanduser("~"), "Pictures")
    # expanduser 扩展用户，~ 表示当前用户

# 打开文件管理器，并选中指定的文件夹
def open_folder_in_explorer(path):
    os.system(f'explorer /select,"{path}"')     # select 选中
    return

def main():
    # 备份 Windows 11 系统的锁屏壁纸图片，和 "Windows 聚焦" 的桌面壁纸图片到指定的目录。
    # 来源图片目录
    Source_Pictures_Folder = get_windows_spotlight_images_path()    # spotlight 聚光灯—— spot 点， light 灯
    print(Source_Pictures_Folder)
    # 备份目录 
    Backup_Pictures_Folder = os.path.join(get_my_pictures_path(), "_备份壁纸_")
    print(Backup_Pictures_Folder)
    if not os.path.exists(Backup_Pictures_Folder):
        os.makedirs(Backup_Pictures_Folder)     # make directory 创建目录

    # 备份图片
    copy_files(Source_Pictures_Folder, Backup_Pictures_Folder)

    # 打开备份目录
    open_folder_in_explorer(Backup_Pictures_Folder)

    return

if __name__ == "__main__":
    main()

