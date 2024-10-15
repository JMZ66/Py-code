import requests
import os
import time
from urllib.parse import quote

# Google Custom Search API 相关配置
API_KEY = 'AIzaSyDaFv9yogP4EINJtXXfar1MEmzqb9YvOjM'  # 替换为你的Google API Key
CX = '93139cc93b2a84586'  # 替换为你的Custom Search Engine ID

# 创建保存图片的基础文件夹
base_dir = 'instrument_images'
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

instruments = [
    {"name": "压样机", "model": "ZHY-401A", "manufacturer": "北京众合创业科技发展有限责任公司"},
    {"name": "压片机", "model": "SDY-20", "manufacturer": "天津市科器高新技术公司"},
    {"name": "振动磨", "model": "ZHM-1A", "manufacturer": "北京众合创业科技发展有限责任公司"},
    {"name": "色差仪", "model": "CM-2600d", "manufacturer": "柯尼卡"},
    {"name": "感应加热设备", "model": "GHB-C2S", "manufacturer": "成都恒贵科技有限责任公司"},
    {"name": "玻璃瓶耐内压力试验机", "model": "BY99-2", "manufacturer": "深圳市科比瑞科技有限公司"},
    {"name": "冷却水循环器", "model": "TF800", "manufacturer": "LabTech"},
    {"name": "百分之一天平", "model": "CP2102", "manufacturer": "奥豪斯"},
    {"name": "分析天平", "model": "AL204", "manufacturer": "梅特勒托利多(上海)公司"},
    {"name": "培养基自动分装系统", "model": "APS 320", "manufacturer": "梅里埃"},
    {"name": "荧光定量PCR仪", "model": "CFX connect", "manufacturer": "美国伯乐"},
    {"name": "培养基制备系统", "model": "Masterclave 09", "manufacturer": "梅里埃"},
    {"name": "液体密度计", "model": "DMA5000M", "manufacturer": "奥地利安东帕"},
    {"name": "自动电位滴定仪", "model": "905", "manufacturer": "瑞士万通"},
    {"name": "粗糙度仪", "model": "TIME3220", "manufacturer": "北京时代之峰科技有限公司"},
    {"name": "分析天平", "model": "LAC214", "manufacturer": "常熟衡器厂"},
    {"name": "标准铂电阻温度计", "model": "WZPB-2", "manufacturer": "云南大方米特尔实业有限公司"},
    {"name": "标准铂电阻温度计", "model": "WZPB-9", "manufacturer": "昆明大方自动控制科技有限公司"},
    {"name": "电子天平", "model": "LP3102", "manufacturer": "常熟衡器厂"},
    {"name": "一等标准酒精计", "model": "（0-100）%", "manufacturer": "冀州耀华"},
    {"name": "二等标准铂电阻温度计", "model": "WZPB-9", "manufacturer": "昆明大方自动控制科技有限公司"},
    {"name": "台式数字式压力技标准装置", "model": "MCS100", "manufacturer": "约克仪器"},
    {"name": "恒温槽", "model": "CJTH-300B", "manufacturer": "湖州唯立仪表科技有限公司"},
    {"name": "恒温槽", "model": "CJTL-35A-GD", "manufacturer": "湖州唯立仪表科技有限公司"},
    {"name": "恒温水槽", "model": "CTS-95A", "manufacturer": "湖州晶觅试验设备公司"},
    {"name": "电子天平", "model": "JD3000-2", "manufacturer": "沈阳龙腾电子有限公司"},
    {"name": "电子天平", "model": "XP205", "manufacturer": "梅特勒-托利多"},
    {"name": "电子天平", "model": "XS1003SX", "manufacturer": "梅特勒-托利多"},
    {"name": "电子天平", "model": "XP6", "manufacturer": "梅特勒-托利多"},
    {"name": "电子天平", "model": "XS6002SX", "manufacturer": "梅特勒-托利多"},
    {"name": "电子天平", "model": "JD-1000-2", "manufacturer": "沈阳龙腾"},
    {"name": "电子天平", "model": "EX24001ZH", "manufacturer": "奥豪斯仪器(常熟)有限公司"},
    {"name": "电子天平", "model": "XS204SX", "manufacturer": "梅特勒-托利多"},
    {"name": "恒温槽", "model": "CJTH-300A", "manufacturer": "湖州唯立仪表厂"},
    {"name": "恒温槽", "model": "CJTL-OA", "manufacturer": "湖州唯立仪表厂"},
    {"name": "十万分之一天平", "model": "CPA225D", "manufacturer": "赛多利斯"},
    {"name": "万分之一天平", "model": "QUINTIX224", "manufacturer": "赛多利斯"},
    {"name": "千分之一天平", "model": "CP213", "manufacturer": "奥豪斯"},
]


# 从Google Custom Search API获取图片
def search_image_google_cse(query, api_key, cx):
    encoded_query = quote(query)
    search_url = f"https://www.googleapis.com/customsearch/v1?q={encoded_query}&key={api_key}&cx={cx}&searchType=image&num=1"
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json()
        if "items" in results:
            image_url = results["items"][0]["link"]
            return image_url
        else:
            print(f"未找到 '{query}' 的图片")
            return None
    else:
        print(f"Google API 请求失败，状态码: {response.status_code}, 错误消息: {response.text}")
        return None

# 下载图片并保存
def download_image(name, model, manufacturer, image_url):
    manufacturer_dir = os.path.join(base_dir, manufacturer)
    if not os.path.exists(manufacturer_dir):
        os.makedirs(manufacturer_dir)

    try:
        img_data = requests.get(image_url).content
        filename = f"{name}_{model}.jpg".replace(' ', '_')
        filepath = os.path.join(manufacturer_dir, filename)
        with open(filepath, 'wb') as img_file:
            img_file.write(img_data)
        print(f"图片已保存到: {filepath}")
    except Exception as e:
        print(f"下载图片失败: {e}")

# 执行图片下载
for instrument in instruments:
    manufacturer = instrument['manufacturer']
    name = instrument['name']
    model = instrument['model']
    search_query = f"{name} {model} {manufacturer}"

    print(f"正在搜索: {search_query}")
    image_url = search_image_google_cse(search_query, API_KEY, CX)

    if image_url:
        download_image(name, model, manufacturer, image_url)
        time.sleep(2)  # 防止请求过快
