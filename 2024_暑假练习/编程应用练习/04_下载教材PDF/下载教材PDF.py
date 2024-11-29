# 下载教材PDF文件小工具
# 主要功能：从国家智慧教育公共服务平台下载小学、中学的教材电子版
# 作者：loongba
# 版本：V1.2

# Stmart Education 智慧教育
# SmartEdu.cn
# 国家智慧教育公共服务平台 —— 推进教育资源公平化：网络课件 同等的教育资源
# 国家中小学智慧教育平台 —— basic.SmartEdu.cn 基础教育：基教处——《义务教育法》，“九漏鱼”
# 

# 主要步骤：
# 1. 获取用户输入的参数：教材的 Url/GUID，教材的名字
# 2. 从教材的 Url/GUID 中提取教材 GUID，构造下载 PDF 的 Url
# 3. 用代码下载该 Url 的文件，另存为 PDF 文件：按照用户提供的教材的名字
# 4. 完成，显示提示信息，打开 PDF 文件

import os
import sys
import re
import requests       # request 请求 response 回应/响应
# 添加上级目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from myUtils import print_error, run_file_by_default_app, print_color

# 获取指定 Url 的 HTML 并返回
def get_html_by_url(url):
    session = requests.Session()
    try:
        response = session.get(url, allow_redirects=False, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.RequestException as e:
        print_error(f"获取 HTML 时发生错误: {e}")
        return None    
    return html

# 获取课件的 PDF url 并返回
def get_book_pdf_url(book_guid_or_url:str):
    # book_url 可能是 GUID
    pattern = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
    match = re.match(pattern, book_guid_or_url)
    if match:   # 不是 GUID
        book_guid = book_guid_or_url
    else:
        # https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=8b9c7052-add4-4744-ab04-69d6c180d5d9&catalogType=tchMaterial&subCatalog=tchMaterial
        # 定义一个正则表达式规则，用于匹配 PDF url
        # pattern 模式, content 内容
        pattern = r"contentId=(.*?)(&|$)"
        # 使用 re.search() 函数查找匹配的字符串
        match = re.search(pattern, book_guid_or_url)    # find, search 查找, match 匹配、比赛
        # 如果找到匹配的字符串，返回它；否则，返回 None
        if match:   # 是 BookUrl
            book_guid = match.group(1)
        else:
            return None
    
    book_pdf_url = f"https://r1-ndr.ykt.cbern.com.cn/edu_product/esp/assets_document/{book_guid}.pkg/pdf.pdf"
    return book_pdf_url

# 下载指定的文件，并以指定的文件名，保存到指定的位置
def download_file(file_url, save_path, save_file_name):
    try:
        print_color(f"开始下载：{file_url}", 'green')
        response = requests.get(file_url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})      # response 响应，request 请求
        response.raise_for_status() # status 状态       # 确保返回 200

        # 写入文件
        new_file_fullname = os.path.join(save_path, save_file_name)
        with open(new_file_fullname, 'wb') as file:        # Readable/Writable, Binary/Text
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        return True, new_file_fullname
    except requests.RequestException as e:      # except 例外
        print(f"下载文件时发生错误: {e}")
        return False, e
    return

def main():
    #book_guid_or_url = "https://basic.smartedu.cn/tchMaterial/detail?contentType=assets_document&contentId=8b9c7052-add4-4744-ab04-69d6c180d5d9&catalogType=tchMaterial&subCatalog=tchMaterial"
    #book_guid_or_url = "8b9c7052-add4-4744-ab04-69d6c180d5d9"
    #book_name = "义务教育教科书·语文七年级上册"
    # 1. 获得要下载的教材的 URL——参数：用户提供
    if len(sys.argv) > 2:
        book_guid_or_url = sys.argv[1]
        book_name = sys.argv[2]
    else:
        print_error("请提供有效的教材 Url/GUID 和教材名字")
        return

    # 2. 用代码下载该 Url，获得网页的内容 HTML
    #html = get_html_by_url(book_guid_or_url)

    # 3. 分析该 book_url 找出我们所需要的内容：教材PDF 的 URL
    book_pdf_url = get_book_pdf_url(book_guid_or_url)
    if not book_pdf_url:
        print_error(f"提供的 教材 Url/GUID 不正确：{book_guid_or_url}")
        print_error(f"没找到匹配的教材 GUID：{book_guid_or_url}")
        return

    # 4. 用代码下载该 URL，另存为 PDF 文件
    # 默认保存在脚本的同级目录下
    script_folder_path = os.path.dirname(os.path.abspath(__file__))  #相对路径转换为绝对路径，以防万一
    success, pdf_file_path = download_file(book_pdf_url, script_folder_path, f"{book_name}.pdf")
    if not success:
        print_error(f"下载文件失败：{pdf_file_path}")
        return
    
    # 5. 完成，显示提示信息，打开 PDF 文件
    print_color(f"成功下载教材 {book_name} 的 PDF 文件：{pdf_file_path}", "green")
    run_file_by_default_app(pdf_file_path)
    run_file_by_default_app(script_folder_path)

if __name__ == "__main__":
    main()