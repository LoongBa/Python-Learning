# 从网站获取今天或指定日期的天气信息
# 通过编写程序调用第三方 API，练习获取网页信息、调用网站 API 的编程技巧
# 通过编写程序读写数据文件，练习读写 Excel 的编程技巧
#
# 主要功能：
# 通过调用第三方提供的免费 API 获取天气信息，并保存到数据文件中缓存
# 后续用于数据统计、分析和绘制图表
# 作者：loongba
# 版本号：Ver1.0

# 自顶向下，逐层分解
# 主要步骤：
# 0. 准备工作：确定所需的 API——和风天气 API，申请 API 密钥
# 1. 获取参数：要查询哪个城市、哪一天的天气信息
# 2. 判断是否已经有本地数据缓存
# 3. 如果没有缓存，则调用 API 获取天气信息，并将天气信息保存到数据文件
# 4. 如果有缓存，从本地数据文件获取天气信息
# 5. 显示天气信息
from datetime import datetime
import requests
import json

# 判断是否已经有本地数据缓存
def is_cache_exists(location, date):
    # TODO: 判断是否已经有本地数据缓存
    return False

# 从本地数据文件获取天气信息
def get_weather_info_from_cache(location, date):

    return "晴，最高温度 30 度，最低温度 20 度"
# 调用 API 获取天气信息，并缓存
def get_weather_info_from_api(api_key, location, date = datetime.now().strftime("%Y-%m-%d")):
    # 调用 和风天气的 API 获取未来三日天气预报
    url = f"https://devapi.qweather.com/v7/weather/3d?location={location}&key={api_key}"
    # print(url)
    response = requests.get(url)
    weather_info = response.json()
    # TODO: 将天气信息缓存到数据文件

    return weather_info

# 将天气信息缓存到数据文件
def save_weather_info_to_cache(location, weather_info, date):
    print(f"城市：{location} 从 {date} 起，未来三日天气预报：\r\n\t{weather_info}")
    return

# 显示天气信息
def print_weather_info(location_name, weather_info):
    print(f"{location_name}未来三日天气预报：")
    for day_info in weather_info["daily"]:
        tempMax = day_info["tempMax"]
        tempMin = day_info["tempMin"]
        date = day_info["fxDate"]
        print(f"\t{date} 最高温度：{tempMax} 度，最低温度：{tempMin}")
        print(f"\t\t日升时间：{day_info['sunrise']}\t日落时间：{day_info['sunset']}")
    return

def main():
    api_key = "4221343812994b3db7eb5cc3bb6e252f"
    # 1. 获取参数：要查询哪个城市、哪一天的天气信息
    location = "101010100" 
    location_name = "北京"
    # 默认获取今天的日期
    date = datetime.now()
    # 2. 判断是否已经有本地数据缓存
    if is_cache_exists(location, date):
        # 2.1. 如果有缓存，从本地数据文件获取天气信息
        weather_info = get_weather_info_from_cache(location, date)
        print(f"本地缓存中查询到天气信息")
    else:
        # 2.2. 如果没有缓存，则调用 API 获取天气信息，并将天气信息保存到数据文件
        weather_info = get_weather_info_from_api(api_key, location, date)
        print(f"API 查询到天气信息")
    # 3. 显示天气信息    
    print_weather_info(location_name, weather_info)

    return

if __name__ == '__main__':
    main()