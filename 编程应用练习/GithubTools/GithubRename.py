# 用于批量更改指定目录下所有 Git 仓库的远程仓库地址
# 仅限于更改了 Github 用户名的情况，仓库名未更改
# 用法：python GithubRename.py <old_username> <new_username>

import os
import re
import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Github 仓库远程地址更改工具")
    parser.add_argument("repositoryDir", type=str, help="仓库根目录")
    parser.add_argument("old_username", type=str, help="原用户名")
    parser.add_argument("new_username", type=str, help="新用户名")
    args = parser.parse_args()
    repositoryDir = args.repositoryDir
    old_username = args.old_username
    new_username = args.new_username

    print(f"对仓库根目录：{repositoryDir}")
    print(f"\t将用户名 {old_username} 改为：{new_username}\r\n")

    # 获取当前目录下所有文件夹
    dirs = [d for d in os.listdir(repositoryDir) if os.path.isdir(os.path.join(repositoryDir, d))]
    # 遍历所有文件夹
    for dir in dirs:
        # 切换到文件夹
        print(f"\t子目录：{dir}", end="")
        os.chdir(os.path.join(repositoryDir, dir))

        # 检查当前目录是否是一个 Git 仓库
        if not os.path.isdir(".git"):
            print(f"\t{dir} 不是一个 Git 仓库，跳过")
            continue

        # 列出所有远程仓库
        remotes = subprocess.getoutput("git remote").split('\n')
        print(f"\t Remotes:{remotes}")
        for remote_name in remotes:
            # 获取远程仓库地址
            remote_url = subprocess.getoutput(f"git remote get-url {remote_name}")
            print(f"\t\t{remote_name}\t\t{remote_url}", end="")
            # 如果远程仓库地址包含旧用户名，则替换为新用户名
            if old_username.lower() in remote_url.lower():
                new_remote_url = re.sub(re.escape(old_username), new_username, remote_url, flags=re.IGNORECASE)
                # 执行命令，更改远程仓库地址
                result = subprocess.run(["git", "remote", "set-url", remote_name, new_remote_url], check=True, capture_output=True, text=True).stdout.strip()
                print(f"\033[32m\t更改成功。{result}\033[0m")
            else:
                print("\033[34m\t无需更改。\033[0m")

        # 切换回上级目录
        os.chdir("..")

    print("__________________________________________\r\n")
    return


if __name__ == "__main__":
    main()
