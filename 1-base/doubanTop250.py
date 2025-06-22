import requests
from bs4 import BeautifulSoup
import time
import csv

# 1. 设置请求头模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

# 2. 创建CSV文件保存结果
with open('douban_top250.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['排名', '电影名称', '评分', '简介'])

    # 3. 循环爬取10页数据（每页25条）
    for page in range(0, 10):
        url = f'https://movie.douban.com/top250?start={page*25}'
        
        # 4. 发送HTTP请求
        response = requests.get(url, headers=headers)
        print(f'正在爬取第{page+1}页，状态码:', response.status_code)
        
        # 5. 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 6. 定位电影条目
        movie_items = soup.find_all('div', class_='item')
        
        for item in movie_items:
            # 7. 提取具体数据
            rank = item.find('em').text  # 排名
            title = item.find('span', class_='title').text  # 中文标题
            rating = item.find('span', class_='rating_num').text  # 评分
            
            # 处理可能缺失的简介
            quote_tag = item.find('span', class_='inq')
            quote = quote_tag.text if quote_tag else '暂无简介'
            
            # 8. 写入CSV
            writer.writerow([rank, title, rating, quote])
        
        # 9. 礼貌性延迟，避免请求过快
        time.sleep(2)  # 每次请求后暂停2秒

print('爬取完成！数据已保存到 douban_top250.csv')