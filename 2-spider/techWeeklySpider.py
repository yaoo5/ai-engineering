"""
仅用作爬虫学习，侵权删。
"""
import requests
import logging
import json
from pyquery import PyQuery as pq

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
def get_source_code(url):
    logging.info('>>> get_source_code start, url:%s', url)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logging.info('>>> get_source_code success, url:%s', url)
            response.encoding = 'utf-8'
            return response.text
    except requests.RequestException:
        logging.error('get_source_code failed, url=%s', url, exc_info=True)

def parse_weekly(html, maxSize = 5):
    logging.info(f'>>> parse_list start..., maxSize={maxSize}')

    doc = pq(html)
    weeklys = doc('.module-content .module-list .module-list-item')
    weeklysData = []
    count = 0

    for weekly in weeklys.items():
        if (count >= maxSize):
            break

        # 计数器+1
        count += 1
        # 标题有个邮箱保护元素  [email protected]。
        # Todo 日期获取也有邮箱保护技术，获取不到，有空来处理
        unwanted_text = "[email protected]"
        title = weekly.find('a').text().replace(unwanted_text, '').strip()
        detail_url = weekly.find('a').attr('href')
        weeklysData.append({
            "title": title,
            "detail_url": detail_url
        })
    
    return weeklysData

def save_json(data, filename):
    try:
        logging.info('>>> save_json success...')

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logging.info('save_json success, filename=%s', filename)
        return True
    except Exception as e:
        logging.error('save_json failed, {e}', exc_info=True)
        return False

def main():
    logging.info(">>> main start")
    
    url = 'https://www.ruanyifeng.com/blog/weekly/'
    html = get_source_code(url)
    weeklyData = parse_weekly(html)

    save_json(weeklyData, 'tech.weekly.json')


if __name__ == '__main__':
    main()
else:
    logging.error('run failed, __name is not __main__')