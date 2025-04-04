import re
import sys

def compare_lists(list1_path, list2_path):
    """
    比较两个文本文件中的姓名名单，找出第一个名单中的名字是否作为子字符串存在于第二个名单中的某个名字里。
    """
    try:
        with open(list1_path, "r", encoding="utf-8") as file1:
            content1 = file1.read()
            list1 = re.split(r"\s+", content1.strip())
            list1 = [name for name in list1 if name]

        with open(list2_path, "r", encoding="utf-8") as file2:
            content2 = file2.read()
            list2 = re.split(r"\s+", content2.strip())
            list2 = [name for name in list2 if name]

        # 用列表 1 中的每一项在列表 2 中匹配子字符串
        list_found = []
        list_not_found = []
        for idx1, item1 in enumerate(list1, start=1):
            found = False
            for idx2, item2 in enumerate(list2, start=1):
                if item1 in item2:  # 检查 item1 是否作为子字符串存在于 item2 中
                    found = True
                    break
            if found:
                list_found.append((idx1, item1, idx2, item2))
            else:
                list_not_found.append((idx1, item1))
                print(f"\t序号 {idx1} {item1} 不存在")

        list_not_found.sort(key=lambda x: x[0])  # 按照序号排序
        list_found.sort(key=lambda x: x[0])  # 按照序号排序

        return list_found, list_not_found
    except FileNotFoundError:
        print("文件未找到，请检查文件路径。")
        return None, None

def main():
    """
    主函数，处理命令行参数并调用 compare_lists 函数进行名单对比
    """
    if len(sys.argv) != 3:
        print("用法: python CompareLists.py <list1_path> <list2_path>")
        sys.exit(1)

    list1_path = sys.argv[1]
    list2_path = sys.argv[2]

    list_found, list_not_found = compare_lists(list1_path, list2_path)

    if list_found is not None:
        i = 0
        print("在名单里的名字:")
        for idx, name, idx2, text in list_found:
            i += 1
            print(f"{i:2d}:\t({idx:2d})\t{name}\t\t{text}")

        print("\n不在名单里的名字:")
        for idx, name in list_not_found:
            print(f"({idx:2d})\t{name}")

if __name__ == "__main__":
    main()
