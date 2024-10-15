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

# 设备列表，按照制造商分组
instruments = [
    {"name": "啤酒分析仪", "model": "DMA4500M", "manufacturer": "奥地利安东帕"},
    {"name": "显微红外光谱仪", "model": "NICILET iN10", "manufacturer": "Thermo"},
    {"name": "测汞仪", "model": "Hydra-IIC", "manufacturer": "美国LEEMAN"},
    {"name": "X射线荧光光谱仪", "model": "ARL PERFORMX 4200型", "manufacturer": "Thermo"},
    {"name": "拉曼红外光谱仪", "model": "Nicolet iS50", "manufacturer": "Thermo"},
    {"name": "红外线水分测定仪", "model": "MA100C-000230V1", "manufacturer": "Sartorius"},
    {"name": "紫外可见分光光度计", "model": "Cary300", "manufacturer": "美国瓦利安"},
    {"name": "原子荧光光度计", "model": "AFS-3000", "manufacturer": "北京科创海光"},
    {"name": "原子荧光光度计", "model": "RGF-8780", "manufacturer": "北京博晖创新光电技术公司"},
    {"name": "原子吸收光谱仪", "model": "PinAAcle900Z", "manufacturer": "铂金埃尔默仪器有限公司"},
    {"name": "原子吸收光谱仪", "model": "PinAAcle900T", "manufacturer": "铂金埃尔默仪器有限公司"},
    {"name": "紫外可见分光光度计", "model": "Cary 60 UV-Vis", "manufacturer": "Agilent Technologies"},
    {"name": "原子吸收仪", "model": "AA240Z", "manufacturer": "美国瓦利安"},
    {"name": "紫外可见分光光度计", "model": "Evolution220", "manufacturer": "赛默飞世尔科技（中国）有限公司"},
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
