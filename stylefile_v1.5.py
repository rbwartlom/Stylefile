import requests
import time
import datetime
from bs4 import BeautifulSoup, SoupStrainer
from dhooks import Webhook

# v2 = [general cleanup] + [no more list + set]
# v3 goal: scrapy instead of bs


def find_all_items_stylefile(page_link_as_string):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    search_result_content = SoupStrainer('div', attrs={'class': 'search-result-content'})
    result = requests.get(page_link_as_string, 'lxml', headers=headers)
    soup = BeautifulSoup(result.content, "html.parser", parse_only=search_result_content)
    lists = soup.find_all('li', class_="grid-tile")
    in_stock_item_names = []

    for listElement in lists:
        item_name_link = listElement.find('a', class_="name-link")
        item_name = item_name_link.text.strip()
        pid = listElement.find('div', class_="product-tile")['data-producttilempid']
        item_link = item_name_link['href']
        in_stock_item_names.append(item_name + " " + pid + " " + item_link)

    return in_stock_item_names


def discord_send(text):
    hook = Webhook("https://discord.com/api/webhooks/822574588129968179/KVtDJPGx_90FWzbY6vL1GvJNE3KLdDoGfmsiNf8pEuYX6E4pCF6Tf1cWLBinnLrygRFF")
    hook.send(text)


def log(action):
    print(str(datetime.datetime.now()) + " " + action + str(len(item_list_base)) + str(len(item_list_new)), flush=True)


discord_send("launched")

item_list_base = find_all_items_stylefile("https://www.stylefile.de/suche?q=air+force+1")

try:
    while True:
        item_list_new = find_all_items_stylefile("https://www.stylefile.de/suche?q=air+force+1")
        if len(item_list_new) > len(item_list_base):
            discord_send("New item: " + str(set(item_list_new) - set(item_list_base)))
            log("change")
        elif len(item_list_new) < len(item_list_base):
            discord_send("Item removed: " + str(set(item_list_base)) - set(item_list_new))
            log("change")
        elif len(item_list_new) == len(item_list_base):
            log("success")
        else:
            log("error")
        item_list_base = item_list_new
        time.sleep(60)
except:
    print('error in while true')
