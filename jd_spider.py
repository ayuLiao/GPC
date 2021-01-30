"""
爬取【京东】商品价格
"""

from bs4 import BeautifulSoup

from utils import get_user_agent, get_session
from logger import logger

def get_goods_price(goods_name):
    # keyword 搜索的内容， psort=2 价格从低到高排序
    search_url = f'https://search.jd.com/Search?keyword={goods_name}&psort=2'
    session = get_session()
    ug = get_user_agent()

    search_res = session.get(search_url, headers=ug, timeout=10)
    if search_res.status_code != 200:
        logger.warning(f'【京东】商品查询失败，keyword: {goods_name} error: {search_res.text}')
        return []
    soup = BeautifulSoup(search_res.text, 'lxml')
    goods_list = soup.find(id='J_goodsList')
    goods_list_lis = goods_list.find_all('li')
    res = []
    for goods in goods_list_lis:
        try:
            price = goods.find(class_='p-price').text.strip()
            name = goods.find(class_='p-name').text.strip()
            goods_img = goods.find(class_='p-img').find('img').get('data-lazy-img')
            if goods_img:
                goods_img = 'http:' + goods_img
            res.append({
                'price': price,
                'name': name,
                'goods_img': goods_img
            })
        except Exception as e:
            logger.warning(f'【京东】在解析商品基本信息时出现异常，error: {e}')

    return res


def test():
    print(get_goods_price("python"))

# test()