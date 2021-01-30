"""
爬取【苏宁】商品价格
"""
import random
import json

from bs4 import BeautifulSoup

from utils import get_user_agent,get_session
from logger import logger



def get_city_id():
    url = 'http://ipservice.suning.com/ipQuery.do'
    session = get_session()
    res = session.get(url, headers = get_user_agent(), timeout=10)
    if res.status_code != 200:
        logger.warning(f'【苏宁】地理位置查询失败，url: {url} error: {res.text}')
        return ''
    res = res.json()
    return res.get('cityLESId', '')


def get_goods_price(goods_name):
    # keyword 搜索关键字 st=9 价格降序
    search_url = f'https://search.suning.com/emall/searchV1Product.do?keyword={goods_name}&ci=0&pg=01&cp=0&il=1&isNoResult=0&st=9&iy=0&n=1'
    price_url = f'https://ds.suning.com/ds/generalForTile/'
    session = get_session()
    ug = get_user_agent()
    search_res = session.get(search_url, headers=ug, timeout=10)
    if search_res.status_code != 200:
        logger.warning(f'【苏宁】商品查询失败，keyword: {goods_name} error: {search_res.text}')
        return []

    soup = BeautifulSoup(search_res.text, 'lxml')
    # moreVendor = soup.find(id='moreVendor')
    goods_list = soup.find(id='product-list')
    goods_list_lis = goods_list.find_all('li')
    price_infos = []
    goods_res = {}
    for goods in goods_list_lis:
        name = goods.find(class_='title-selling-point').find('a').text
        goods_img = goods.find(class_='res-img').find('img').get('src')
        if goods_img:
            goods_img = 'http:' + goods_img

        price_info = goods.find(class_='def-price')
        datasku = price_info.get('datasku')
        mdmgroupid = price_info.get('mdmgroupid')
        brand_id = price_info.get('brand_id')
        dataskures = datasku.split('|')
        partnumber = dataskures[0]
        _type = dataskures[2]
        supplierCode = dataskures[5]
        if _type in (100, 101, 102, '03', '04', 'p', 'm', 'o1', 'o2', 'zl', 'g', 'o1m', 'lv'):
            pass
        if supplierCode == '':
            _type = 1
        else:
            _type = 2
        price_infos.append({
            'partnumber': partnumber,
            'type': _type,
            'supplierCode': supplierCode,
            'threegroupId': mdmgroupid,
            'brand_id': brand_id
        })
        key = '0000000' + str(partnumber)
        goods_res[key] = {
            'name': name,
            'goods_img': goods_img
        }

    typeAry = {}
    codeAry = {}
    for price in price_infos[:10]:
        _type = price['type']
        code = price['supplierCode']
        typeKey = '_' + str(_type)
        codeKey = '_' + str(code)
        data = typeAry.get(typeKey)
        if not data:
            data = {
                'index': len(typeAry),
                'key': _type,
                'num': 0
            }
            typeAry[typeKey] = data
        typeAry[typeKey]['num'] += 1

        data = codeAry.get(codeKey)
        if not data:
            data = {
                'index': len(codeAry),
                'key': code,
                'num': 0
            }
            codeAry[codeKey] = data
        codeAry[codeKey]['num'] += 1

    defaultType = None
    maxnumType = 0
    for k, v in typeAry.items():
        if v['num'] > maxnumType:
            maxnumType = v['num']
            defaultType = v['key']

    defaultCode = None
    maxnumCode = 0
    for k, v in codeAry.items():
        if v['num'] > maxnumCode:
            maxnumCode = v['num']
            defaultCode = v['key']

    _callback = 'ds000000000' + str(int(random.random() * 10000))

    urlAry = []
    for price in price_infos[:10]:
        urlparams = []
        partnumber = price.get('partnumber')
        supplierCode = price['supplierCode']
        urlparams.append(f'0000000{partnumber}__')
        if supplierCode == defaultCode:
            urlparams.append(price['type'])
        urlparams.append('_')
        if supplierCode != defaultCode:
            urlparams.append(supplierCode)
        urlparams.append('_')
        urlparams.append('_')
        urlparams.append(price['threegroupId'])
        urlparams.append('_')
        urlparams.append(price['brand_id'])
        urlAry.append(''.join([str(i) for i in urlparams]))
    url = ','.join(urlAry)
    cityId = get_city_id()
    url = f'{price_url}{url}-{cityId}-{defaultType}-{defaultCode}-1--{_callback}.jsonp'
    res = session.get(url, headers=ug, timeout=10)
    if res.status_code != 200:
        logger.warning(f'【苏宁】商品价格查询失败，keyword: {goods_name} error: {res.text} url: {url}')
        return []
    goods_info = res.text.replace(f"{_callback}(", "")
    goods_info = goods_info[:-2]
    goods_info = json.loads(goods_info)
    goods_infos = goods_info.get('rs', [])
    goods_infos = {g['cmmdtyCode']: g['price'] for g in goods_infos}
    res = []
    for k, v in goods_infos.items():
        g = goods_res.get(k, {})
        res.append({
            'price': v,
            'name': g.get('name', ''),
            'goods_img': g.get('goods_img', '')
        })
    # print(res)
    return res


def test():
    get_goods_price('python')
    # get_city_id()

# test()








'''
https://ds.suning.com/ds/generalForTile/
000000012126515298__2_0071269006__R9011070_0001400NQ,
000000011590690947__2_0070859890__R9011095_0001400CU,
000000000154318181_____R9011095_000140ADJ,
000000000647185561__2_0071046110__R9011070_0001400UN,
000000012126514651__2_0071269006__R9011070_0001400QC,
000000012189089603__2_0070504352__R9011070_000149999,
000000000139020561_____R9011095_0001400CU,
000000012189089603__2_0071303773__R9011070_000149999,
000000010974601116__2_0070067633__R9011070_0001400CU,
000000010678463707_____R9011070_0001400ZU-020-2-0070172873-1--ds0000000005871.jsonp?callback=ds0000000005871
'''

'''
https://ds.suning.com/ds/generalForTile/
000000010727825334_____R9011070_0001400ZU,
000000000621475097_____R9011095_0001400DH,
000000012121608323__2_0071269006__R9011070_0001400ZU,
000000010747515133__2_0070067633__R9011070_000140A0H,
000000012196908646__2_0071143228__R9011095_0001400ZU-020-2-0070172873-1--ds0000000002115.jsonp?callback=ds0000000002115
'''