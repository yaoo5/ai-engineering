"""
仅用作爬虫学习，侵权删。
"""
import requests
import logging
import json
import sys
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
        logging.error('get_source_code failed, url=%s, {e}', url, exc_info=True)

def parse_weekly(html, maxSize = 5):
    logging.info(f'>>> parse_list start..., maxSize={maxSize}')

    doc = pq(html)
    weeklys = doc('.module-content .module-list .module-list-item')
    weeklys_data = []
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
        weeklys_data.append({
            "title": title,
            "detail_url": detail_url
        })
    
    return weeklys_data

def send_message(robot_url, data):
    try:
        logging.info('send_message start')

        if not robot_url:
            logging.error('send_message failed, not robot_url')
            return False

        message = "## 科技周刊"
        headers = {
            "Content-Type": "application/json"
        }
        robot_data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "【dev】科技爱好者周刊｜⏰ 更新提醒",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": "☞☞☞ "
                                },
                                {
                                    "tag": "a",
                                    "text": f"{data[0]['title']}\n",
                                    "href": data[0]['detail_url']
                                },
                                {
                                    "tag": "text",
                                    "text": "「更多内容的爬取还在开发中，敬请期待。」\n\n"
                                },
                                {
                                    "tag": "text",
                                    "text": "🦃 往期回顾\n",
                                },
                                {
                                    "tag": "a",
                                    "text": f"1. {data[1]['title']}\n",
                                    "href": data[1]['detail_url']
                                },

                                {
                                    "tag": "a",
                                    "text": f"2. {data[2]['title']}\n",
                                    "href": data[2]['detail_url']
                                },
                                {
                                    "tag": "a",
                                    "text": f"3. {data[3]['title']}\n",
                                    "href": data[3]['detail_url']
                                },
                                {
                                    "tag": "a",
                                    "text": f"4. {data[4]['title']}\n",
                                    "href": data[4]['detail_url']
                                },
                                {
                                    "tag": "a",
                                    "text": ">>> 查看更多\n\n",
                                    "href": "https://www.ruanyifeng.com/blog/weekly/"
                                },
                                {
                                    "tag": "at",
                                    "user_id": "all"
                                }
                            ]
                        ]
                    }
                }
            }
        }
        requests.post(robot_url, json=robot_data, headers=headers)
        logging.info('send_message success')
    except Exception as e:
        logging.error('send_message failed, {e}', exc_info=True)

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

def get_robot_url():
    command_robot_url = ''
    for arg in sys.argv[1:]:
        if arg.startswith("--robotUrl="):
            command_robot_url = arg.split("=", 1)[1]
            break

    return command_robot_url

def main():
    logging.info(">>> main start")
    
    url = 'https://www.ruanyifeng.com/blog/weekly/'
    html = get_source_code(url)
    weekly_data = parse_weekly(html)

    # save_json(weekly_data, 'ruanyifeng.weekly.json')
    robot_url = get_robot_url()
    send_message(robot_url, weekly_data);


if __name__ == '__main__':
    main()
else:
    logging.error('run failed, __name is not __main__')