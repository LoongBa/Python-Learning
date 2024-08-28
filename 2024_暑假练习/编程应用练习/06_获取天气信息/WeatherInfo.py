# 从网站获取今天或指定日期的天气信息
# 通过编写程序调用第三方 API，练习获取网页信息、调用网站 API 的编程技巧
# 通过编写程序读写数据文件，练习读写 Excel 的编程技巧
#
# 主要功能：
# 通过调用第三方提供的免费 API 获取天气信息，并保存到数据文件中缓存
# 后续用于数据统计、分析和绘制图表
# 作者：loongba
# 修改记录：
#   Ver1.0 20240826 调用 API 查询北京未来三天的天气信息，未读取参数、未加入缓存
#   Ver1.1 20240827: 读取城市名字，调用 API 查询城市编码
#   Ver1.2 20240828: 微调、重构了 API 调用代码
#   Ver1.3 TODO: 检查是否有缓存、读取缓存、缓存到本地文件
#   Ver1.4 TODO: 加入模块：从某网站读取历史天气信息并保存为文件
#   Ver1.x TODO: 加入数据统计和绘制图表

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
import sys
import os

# 添加上级目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from myUtils import print_error, run_file_by_default_app, print_color

api_key = "4221343812994b3db7eb5cc3bb6e252f"


# 从运行参数中获取城市名称或 ID
def get_argv():
    if len(sys.argv) > 1:
        location = sys.argv[1]
        if len(sys.argv) > 2:
            location_adm = sys.argv[2]
    else:
        print("请提供有效的城市 ID 或 城市名称")
        sys.exit(1)

    return location, location_adm


# 判断是否已经有本地数据缓存
def is_cache_exists(location, date):
    # TODO: 判断是否已经有本地数据缓存
    return False


# 从本地数据文件获取天气信息
def get_weather_info_from_cache(location, date):

    return "晴，最高温度 30 度，最低温度 20 度"


# 获取城市的地理信息：行政区划编码、城市名称——Business Logic
def get_geo_info(location_string, location_adm = ""):
    api_url = f"https://geoapi.qweather.com/v2/city/lookup?location={location_string}&adm={location_adm}&range=cn&key={api_key}"
    json = call_web_api(api_url)
    if "code" in json and json["code"] == "200":
        return {
            "location_id": json["location"][0]["id"],
            "location_name": json["location"][0]["name"],
            "location_adm1": json["location"][0]["adm1"],
            "location_adm2": json["location"][0]["adm2"],
        }
    else:
        print_error(f"获取城市编码出错：{location_string} {location_adm} \r\n\t{json}")
    return None

# 调用 API 获取天气信息，并缓存
def get_weather_info_from_api(location_id, days = 3):
    # 调用 和风天气的 API 获取未来三日天气预报
    api_url = f"https://devapi.qweather.com/v7/weather/3d?location={location_id}&key={api_key}"
    json = call_web_api(api_url)
    if "code" in json and json["code"] == "200":
        return json
    else:
        print_error(f"获取天气信息出现异常：{json}\r\n\t{api_url}")

    return None

# 工具方法：没有业务逻辑
# 提高了程序的可复用性——提取到工具箱作为公共模块
def call_web_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # 如果返回的 HTTP 状态码不是 2xx
        return response.json()
    except Exception as e:
        print_error(f"调用 API 出现异常：{e}\r\n\t{api_url}")
    return None

# 将天气信息缓存到数据文件
def save_weather_info_to_cache(location, weather_info, date):
    # print(f"城市：{location} 从 {date} 起，未来三日天气预报：\r\n\t{weather_info}")
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
    # 1. 获取参数：要查询哪个城市、哪一天的天气信息
    location_string, location_adm = get_argv()
    # 从运行参数中获取城市名称或 ID
    location_info = get_geo_info(
        location_string, location_adm
    )  # information，例如 GIS：Geographic Information System
    location_id = location_info["location_id"]
    location_name = location_info["location_name"]

    # 默认获取今天的日期
    date = datetime.now()
    # 2. 判断是否已经有本地数据缓存
    if is_cache_exists(location_id, date):
        # 2.1. 如果有缓存，从本地数据文件获取天气信息
        weather_info = get_weather_info_from_cache(location_id, date)
        # print(f"本地缓存中查询到天气信息")
    else:
        # 2.2. 如果没有缓存，则调用 API 获取天气信息，并将天气信息保存到数据文件
        weather_info = get_weather_info_from_api(location_id)
        # print(f"API 查询到天气信息")
    # 3. 显示天气信息
    if weather_info:
        print_weather_info(location_name, weather_info)
    else:
        print_error("查询天气信息失败")

    return


if __name__ == "__main__":
    main()
