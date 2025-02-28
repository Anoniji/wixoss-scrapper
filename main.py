import os
from random import randint
import time
import requests
from bs4 import BeautifulSoup
import shutil
import json
import re
import math
from tqdm import tqdm
import cutlet
katsu = cutlet.Cutlet()

version = 'en'
rootUrl = {
    'jp': 'https://www.takaratomy.co.jp/products/wixoss',
    'en': 'https://www.takaratomy.co.jp/products/en.wixoss'
}

if version == 'jp':
    SearchUrl = rootUrl[version] + "/card/card_list.php"
else:
    SearchUrl = rootUrl[version] + "/card/itemsearch.php"

epoch_time = '1692264910944' # start session with ms
cards_by_page = 21
start_page = 0 # 33
# [en] start 0 / [jp] start 1

count = 0
CardInfo = {}
post_form = {
    'search': '1',
    'keyword': '',
    'card_kind': '',
    'card_type': '',
    'rarelity': '',
    'support_formats[]': '1',
    'x': '81',
    'y': '30'
}
'''先通过条件找到最大搜索结果分页'''
session = requests.Session()
res = session.post(SearchUrl, data=post_form)
res.encoding = 'utf-8'
pageListSoup = BeautifulSoup(res.text, "html.parser")

if version == 'jp':
    total_cards = pageListSoup.find(attrs="cont cardDip").find('span').string[:-1]
else:
    total_cards = json.loads(pageListSoup.string)['count']

maxPage = math.ceil(int(total_cards) / cards_by_page)

'''从每个页面分类上获得单卡url'''
for i in tqdm(range(start_page, maxPage + 1), desc='Page: '):

    if version == 'jp':
        res = session.get(SearchUrl + '?card_page=' + str(i))
    else:
        res = session.get(SearchUrl + '?p=' + str(i) + '&ord=asc&sor=&_=' + epoch_time)

    res.encoding = 'utf-8'
    cardListSoup = BeautifulSoup(res.text, "html.parser")

    if version == 'jp':
        cardList = cardListSoup.find_all(class_='ajax cboxElement')
    else:
        cardList = json.loads(cardListSoup.string)['items']

    '''从单卡页面上获得卡面信息'''
    for card_pos in tqdm(range(0, len(cardList)), leave=False, desc='Card: '):
        card = cardList[card_pos]
        if version == 'en':

            directory_output = './cards_' + version
            if not os.path.isdir(directory_output):
                os.mkdir(directory_output)

            directory_output = directory_output + '/' + card['card_no'].split('-')[0]
            if not os.path.isdir(directory_output):
                os.mkdir(directory_output)

            res = requests.get('https://www.takaratomy.co.jp/products/en.wixoss/card/thumb/' + card['card_no'] + '.jpg', stream=True)
            if res.status_code == 200:
                with open(directory_output + '/' + card['card_no'] + '.jpg', 'wb') as f:
                    shutil.copyfileobj(res.raw, f)

            json_object = json.dumps(card, indent=4)
            with open(directory_output + '/' + card['card_no'] + '.json', 'w', encoding='utf-8') as outfile:
                outfile.write(json_object)

        else:
            resCard = session.get(SearchUrl + card['href'])
            resCard.encoding = 'utf-8'
            cardSoup = BeautifulSoup(resCard.text, "html.parser")

            cardInfo = dict()
            cardInfo['wxid'] = cardSoup.find(class_='cardNum').string
            cardInfo['name'] = cardSoup.find(class_='cardName').get_text(strip=True)
            cardInfo['name_romanji'] = False
            if version == 'jp':
                cardInfo['name_romanji'] = katsu.romaji(cardInfo['name'])
            rarity = cardSoup.find(class_='cardRarity').string
            cardInfo['rarity'] = re.sub('\W+', '', rarity)
            cardInfo['cardImg'] = cardSoup.find(class_='cardImg').find('img')['src']

            cardInfo['cardData'] = {}
            cardData_titles = cardSoup.find(class_='cardData').findAll('dt')
            cardData_contents = cardSoup.find(class_='cardData').findAll('dd')
            for pos_data in range(len(cardData_titles)):
                if version == 'jp':
                    cardData_title = katsu.romaji(cardData_titles[pos_data].get_text(strip=True))
                else:
                    cardData_title = cardData_titles[pos_data].get_text(strip=True)
                cardData_content = cardData_contents[pos_data].get_text(strip=True)
                cardInfo['cardData'][cardData_title] = cardData_content

            cardInfo['illust'] = cardSoup.find(class_='cardImg').find('span').get_text(strip=True)

            directory_output = './cards_' + version
            if not os.path.isdir(directory_output):
                os.mkdir(directory_output)

            directory_output = directory_output + '/' + cardInfo['wxid'].split('-')[0]
            if not os.path.isdir(directory_output):
                os.mkdir(directory_output)

            res = requests.get(cardInfo['cardImg'], stream=True)
            if res.status_code == 200:
                with open(directory_output + '/' + cardInfo['wxid'] + '.jpg', 'wb') as f:
                    shutil.copyfileobj(res.raw, f)


            json_object = json.dumps(cardInfo, indent=4)
            with open(directory_output + '/' + cardInfo['wxid'] + '.json', 'w', encoding='utf-8') as outfile:
                outfile.write(json_object)

        delay = randint(1, 3)
        time.sleep(delay)
