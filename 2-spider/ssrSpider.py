import requests
import logging
import json
from pyquery import PyQuery as pq
from urllib.parse import urljoin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s:%(message)s'
)

BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10

def get_source_code(url):
    logging.info('>>> get_source_code start, url:%s', url)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info('>>> get_source_code success, url:%s', url)
            return response.text
    except requests.RequestException:
        logging.error('get_source_code failed, url=%s', url, exc_info=True)

def parse_list(html):
    logging.info('>>> parse_list start...')

    doc = pq(html)
    cards = doc('.el-card')
    cardsData = []

    for card in cards.items():
        name = card.find('.name h2').text()
        score = card.find('.score').text()
        detail_url = card.find('.name').attr('href')
        logging.info('name %s, score %s', name, score)
        cardsData.append({
            'name': name,
            'score': score,
            'detail_url': f'{BASE_URL}{detail_url}'
        })

    
    logging.info('>>> parse_list success...')
    return cardsData

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
    print('main function start...')

    list_url = f'{BASE_URL}/page/1'
    list_code = get_source_code(list_url)
    list_data = parse_list(list_code)
    save_json(list_data, 'ssr-spider.json')


if __name__ == '__main__':
    main()