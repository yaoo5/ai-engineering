
from playwright.sync_api import sync_playwright
import logging
import requests
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def scrape_page_list(url, max_size = 5):
    articles = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 创建上下文
        context = browser.new_context(
            viewport={'width': 1440, 'height': 900},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
        )
        page = context.new_page()

        # 访问掘金页面
        page.goto(url, timeout=60000)

        page.wait_for_timeout(1000)  # 等待加载

        articles_elems = page.query_selector_all('.entry-list > .item')

        for article_elem in articles_elems[:max_size]:
            title = article_elem.query_selector('.title-row a.title').text_content().strip()
            detail_url = article_elem.query_selector('.title-row a.title').get_attribute('href')
            user = article_elem.query_selector('.user-popover').text_content().strip()
            view = article_elem.query_selector('.view span').text_content().strip()

            logging.info(f'{title}, {detail_url}, {user}, {view}')
            articles.append({
                "title": title,
                "user": user,
                'view': view,
                'detail_url': f'https://juejin.cn{detail_url}'
            })

        browser.close()
    
    return articles

def send_message(robot_url, articles):
    logging.info('send_message start')

    if not robot_url:
        logging.error('send_message failed, not robot_url')
        return False
    
    headers = {
        "Content-Type": "application/json"
    }
    robot_data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "掘金｜⏰ 本周榜单",
                    "content": [
                        [
                            {
                                "tag": "a",
                                "text": f"1. {articles[0]['title']}\n",
                                "href": articles[1]['detail_url']
                            },
                            {
                                "tag": "a",
                                "text": ">>> 查看更多\n\n",
                                "href": "https://juejin.cn/recommended"
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


def get_robot_url():
    command_robot_url = ''
    for arg in sys.argv[1:]:
        if arg.startswith("--robotUrl="):
            command_robot_url = arg.split("=", 1)[1]
            break

    return command_robot_url

def main():
    articles = scrape_page_list("https://juejin.cn/recommended", 10)
    
    robot_url = get_robot_url()
    send_message(robot_url, articles)


if __name__ == '__main__':
    main()
else:
    logging.error('run failed, __name is not __main__')
