# 获取天气历史信息

import requests
from datetime import datetime
import regex as re
import json
import sys
import os
# 添加上级目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from myUtils import print_error, print_color, debug_print

# 获取指定城市指定月份的天气信息
def get_weather_history_monthly(city_name, date_month: datetime):
    date_month = datetime.now().strftime("%Y%m")
    url = f"http://tianqihoubao.com/lishi/{city_name}/month/{date_month}.html"
    debug_print(f"获取天气历史信息：{url}")
    response = requests.get(url)
    html = response.text
    # 1. 剪裁去掉不要的部分
    start = html.find("<table")
    end = html.find("</table>") + len("</table>")
    data_html = html[start:end]
    # 2. 简单清理：去掉多余的空格和回车换行
    data_html = re.sub("[\s]+", " ", data_html)
    data_html = re.sub("[\r\n]+", "", data_html)
    # 3. 解析HTML，获取天气信息
    # <tr><td><a href="/lishi/kunming/20110101.html" title="2011年01月01日昆明天气预报">2011年01月01日</a></td><td>晴/多云</td><td>7℃/17℃</td><td>无持续风向 微风/无持续风向 微风</td></tr>
    weather_info = {"city_id": city_name, "city_name": "", "history": []}
    pattern = re.compile(r'<td>.*?<a(.*?)>(?P<date>.*?)</a>.*?</td>.*?<td>(?P<weather>.*?)</td>.*?<td>(?P<temperature>.*?)</td>.*?<td>(?P<wind>.*?)</td>', re.S)
    matches = pattern.finditer(data_html)
    for row in matches:
        date_str = row.group('date').strip()
        # 将日期字符串转换为日期格式
        date = datetime.strptime(date_str, "%Y年%m月%d日")
        weather = row['weather'].strip()
        temperature = row['temperature'].strip()
        wind = row['wind'].strip()
        weather_info["history"].append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "weather": weather,
                "temperature": temperature,
                "wind": wind,
            }
        )
    return weather_info if weather_info["history"] else None

def main():
    city_name = "kunming"
    date_month = datetime.now() # 本月
    weather_info = get_weather_history_monthly(city_name, date_month)
    print(json.dumps(weather_info, ensure_ascii=False, indent=4))
    return

if __name__ == "__main__":
    main()