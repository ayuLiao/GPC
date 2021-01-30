from bs4 import BeautifulSoup

from utils import get_user_agent, get_session
from logger import logger

def get_goods_price(goods_name):
    search_url = f'http://search.dangdang.com/?key={goods_name}&act=input&sort_type=sort_xlowprice_asc'
    session = get_session()
    ua = get_user_agent()
    search_res = session.get(search_url, headers=ua, timeout=10)
    if search_res.status_code != 200:
        return []
    soup = BeautifulSoup(search_res.text, 'lxml')
    goods_list = soup.find(id='search_nature_rg')
    goods_list_lis = goods_list.find_all('li')
    res = []
    for goods in goods_list_lis:
        try:
            name = goods.find(class_='name').text.strip()
            price = goods.find(class_='search_now_price').text.strip()
            goods_img = goods.find('img').get('src')
            res.append({
                'price': price,
                'name': name,
                'goods_img': goods_img
            })
        except Exception as e:
            logger.warning(f'【当当】在解析商品基本信息时出现异常，error: {e}')

    return res



def test():
    get_goods_price("python")

# test()