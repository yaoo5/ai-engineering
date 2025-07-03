
from playwright.sync_api import sync_playwright
import logging
import requests
import sys
from concurrent.futures import ThreadPoolExecutor
# ThreadPoolExecutor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def scrape_page_list(url, max_size = 5):
    logging.info(f'scrape_page_list start, {url}')
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
        # page.wait_for_timeout(2000)  # 等待加载
        page.wait_for_selector('.entry-list > .item', state='attached', timeout=10000)  # 等待文章容器加载

        articles_elems = page.query_selector_all('.entry-list > .item')

        # TODO 这里应该加一个id去重、阅读量最小值
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
    
    logging.info(f'scrape_page_list success, {url}')
    return articles

def send_message(robot_url, articles):
    logging.info(f'send_message start, {len(articles)}')

    if not robot_url:
        logging.error('send_message failed, not robot_url')
        return False
    
    headers = {
        "Content-Type": "application/json"
    }

    articles_msg = []
    for idx, article in enumerate(articles, 1):
        articles_msg.append({
            "tag": "a",
            "text": f"{idx}、{article['title']}",
            "href": article['detail_url']
        })
        articles_msg.append({
            "tag": "text",
            "text": f" @{article['user']}  (阅读量：{article['view']})\n"
        })

    robot_data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "掘金｜💰 精彩文章推荐",
                    "content": [
                        articles_msg
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

# TODO 偶尔运行报错，这是什么毛病
def main():
    articles_all = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交所有爬取任务
        future_rec = executor.submit(scrape_page_list, "https://juejin.cn/recommended", 3)
        future_art = executor.submit(scrape_page_list, "https://juejin.cn/article", 2)
        future_car = executor.submit(scrape_page_list, "https://juejin.cn/career", 3)
        future_ai = executor.submit(scrape_page_list, "https://juejin.cn/ai", 2)
        
        # 获取结果
        articles_recommended = future_rec.result()
        articles_article = future_art.result()
        articles_career = future_car.result()
        articles_ai = future_ai.result()
    
    articles_all.extend(
        articles_recommended +
        articles_article +
        articles_career +
        articles_ai
    )

    print(f'all, {len(articles_all)}')
    robot_url = get_robot_url()
    send_message(robot_url, articles_all)


if __name__ == '__main__':
    main()
else:
    logging.error('run failed, __name is not __main__')
