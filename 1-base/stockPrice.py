import requests
from bs4 import BeautifulSoup

# 1. 设置请求头模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

url = f'https://www.futunn.com/hk/stock/01810-HK'

print("*" * 6, "📈 开始获取小米集团股票信息", "*" * 6)
# 4. 发送HTTP请求
response = requests.get(url, headers=headers)

# 5. 解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

name = soup.select_one('.stock-info-component .detail-top .name').text
price = soup.select_one('.detail-main .price-current .price').text
date =  soup.select_one('.stock-info-component .stock-data .status span').text

print(f"- 股票名称: {name.strip()}")
print(f"- 当前价格: {price.strip()}")  # 价格可以特别突出显示
print(f"- 更新时间: {date.strip()}")
