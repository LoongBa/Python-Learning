import json
import os
import re
import requests
from playwright.sync_api import sync_playwright
from tqdm import tqdm

json_filename = "《小学生C++创意编程》_在线视频课程.json"
video_html_filename = "《小学生C++创意编程》_在线视频课程.html"

def extract_urls_with_playwright(urls, urls_json, wait_time=2):
    results = []
    # Create a new instance of Playwright
    with sync_playwright() as playwright:
        # Launch the default browser
        browser = playwright.chromium.launch(channel="msedge", headless=False)
        # Create a new page
        page = browser.new_page()

        count = 0
        for url in urls:
            # 忽略 urls_json 中已经存在的链接

            record = [record for record in urls_json if record[2] == url[1]]
            if record:  # 在 urls_json 中找到 url[1] 相同的记录
                count += 1
                record = record[0]
                results.append(
                    (record[0], record[1], record[2], record[3], record[4], record[5])
                )
                print(f"{count:003d} \033[92m{url[0]} 已提取，\033[93m忽略\033[0m", end="")
                if record[4]:
                    print(f"\t\033[92m{record[4]}\033[0m")
                else:
                    print(f"\t\033[93m其它资源\033[0m")
                continue
            # Navigate to the specified URL
            page.goto(url[1])
            # Wait for the specified time
            page.wait_for_timeout(wait_time * 1000)

            link_element = page.query_selector("#serialNumExport")
            count += 1
            if link_element:
                link_href = link_element.get_attribute("href")
                if link_href:
                    # 提取文件名
                    file_name = link_href.split("attname=")[1].split("&")[0]
                    file_name = requests.utils.unquote(file_name)
                    # 文件名符合模式：第8课
                    if re.match(r"第\d+课", file_name):
                        id = re.findall(r"\d+", file_name)[0]
                        results.append(
                            (True, url[0], url[1], int(id), file_name, link_href)
                        )
                        print(
                            f"{count:003d} {url[0]}\t\033[92m 成功：{file_name}\033[0m"
                        )
                        continue
            results.append((False, url[0], url[1], 0, "", ""))
        browser.close()

    return results

def download_video(url, save_path, file_name):
    # 如果问价按已经存在，则跳过
    fullfilename = os.path.join(save_folder, file_name)
    if os.path.exists(fullfilename):
        # 判断文件大小超过 1M
        if os.path.getsize(fullfilename) > 1024 * 1024:
            return (True, "文件已经存在", save_path, file_name, fullfilename)

    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name)
        with open(fullfilename, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                pbar.update(len(data))
        pbar.close()
    except requests.exceptions.RequestException as err:
        return (False, f"下载失败，错误信息：{err}", save_path, file_name, fullfilename)
    except IOError as err:
        return (False, f"文件写入失败，错误信息：{err}", save_path, file_name, fullfilename)

    return (True, "下载成功", save_path, file_name, fullfilename)

def download_videos(save_path):
    # 读取 json 文件为 urls_json 对象
    if not os.path.exists(json_filename):
        with open(json_filename, "w") as file:
            json.dump([], file)

    with open(json_filename, "r") as file:
        urls_json = json.load(file)

    # 过滤掉无效记录
    records = [r for r in urls_json if r[0]]
    
    # 下载
    logs = []

    pbar = tqdm(records, desc="下载视频文件中")
    for record in pbar:
        video_id = record[1]
        id = record[3]
        file_name = record[4]
        url = record[5]
        pbar.set_description_str(f"正在下载: {video_id} 《{file_name}》")
        r = download_video(url, save_path, file_name)
        logs.append((r[0], id, file_name, video_id, url))
        #pbar.write(f"\t已下载: {video_id} 《{file_name}》")
    return logs

def process_video(urls, save_path):
    # 读取 json 文件为 urls_json 对象
    if not os.path.exists(json_filename):
        with open(json_filename, "w") as file:
            json.dump([], file)

    with open(json_filename, "r") as file:
        urls_json = json.load(file)

    results = extract_urls_with_playwright(urls, urls_json, 2)
    # 根据results[1]去重，排序
    results = list(set(results))
    results = sorted(results, key=lambda x: x[3])

    # 保存为 JSON 文件
    with open(json_filename, "w") as file:
        json.dump(results, file)

    # 过滤掉 results[i][0] 为 False
    results = [result for result in results if result[0]]
    # 保存为 HTML 文件
    count = 0
    with open(video_html_filename, "w") as file:
        file.write("<html><body><ul>")
        for result in results:
            count += 1
            file.write(f'<li>{count:003d} <a href="{result[2]}">{result[4]}</a></li>')
        file.write("</ul></body></html>")

    return

def process_video_urls(idList):
    urls = []
    idList = sorted(list(set(idList)))
    for video_id in idList:
        video_url = video_url_pattern.format(video_id)
        urls.append((video_id, video_url))

    process_video(urls, save_folder)
    return

def extract_video_urls():
    idList = [404104]
    idList.extend([403322 + i for i in range(25)])
    idList.extend([401952 + i for i in range(10)])
    idList.extend([403124 + i for i in range(11)])
    idList.extend(
        [
            404109,
            403270,
            404236,
            403280,
            403289,
            403297,
            403205,
            403206,
            403267,
            403269,
            403313,
            403319,
            403320,
            403322,
            404647,
            404100,
        ]
    )
    idList.extend([403635 + i for i in range(3)])
    idList.extend([403656 + i for i in range(20)])
    idList.extend([404076 + i for i in range(20)])

    process_video_urls(idList)
    return

if __name__ == "__main__":
    # url 模板
    video_url_pattern = "https://www.wqyunpan.com/resourceDetail.html?id={0}&qrcodeId=344170&sign=c2lnbjR0QzF5N21GSHdoOUE0dEctMTcxNTA4NzIxMzU5Mg==@c2lnbkZvcnltaFkzZ2I1b3BWaU0tMTcxNTA4NzIxMzU5Mg=="
    # 保存路径——需要修改
    save_folder = "D:\\_Videos_\\《小学生C++创意编程》"

    # 提取 urls
    extract_video_urls()

    # 根据 json 文件下载视频
    count = 0
    logs = download_videos(save_folder)
    for log in logs:
        count += 1
        print(f"\033[94m{count:003d}\033[0m", end="")
        if log[0]:
            print(f"\033[92m 下载成功\033[0m", end="")
        else:
            print(f"\033[91m 下载失败\033[0m", end="")
        print(f"\t\033[92m{log[3]}\t{log[2]}\033[0m")
