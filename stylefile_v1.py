import requests
import time
import datetime
from bs4 import BeautifulSoup
from dhooks import Webhook

# python3 stylefile_v1.py > server.log &


def find_all_items_stylefile(page_link_as_string):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(page_link_as_string, 'lxml', headers=headers)
    soup = BeautifulSoup(result.content, "html.parser")
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
    hook = Webhook("https://discord.com/api/webhooks/541035168954056704/Um3GJlpWAEuqw0ZPsup9i3cPDGwyI-ZD3qW5raN6gZ7YH0GPQ0eD18M5HQEdOWUAxb5Y")
    hook.send(text)


discord_send("testtest")

item_list_base = find_all_items_stylefile("https://www.stylefile.de/suche?q=air+force+1")

while True:
    item_list_new = find_all_items_stylefile("https://www.stylefile.de/suche?q=air+force+1")
    if len(item_list_base) != len(item_list_new):
        if len(item_list_new) > len(item_list_base):
            discord_send(str("New item: " + str(set(item_list_new) - set(item_list_base))))
            # print("change")
        elif len(item_list_new) < len(item_list_base):
            discord_send("Item removed: " + str(set(item_list_base) - set(item_list_new)))
            # print("change")
    elif len(item_list_new) == len(item_list_base):
        print(str(datetime.datetime.now()) + " success" + str(len(item_list_base)) + str(len(item_list_new)), flush=True)
    else:
        print(str(datetime.datetime.now()) + " error" + str(len(item_list_base)) + str(len(item_list_new)), flush=True)
    item_list_base = item_list_new
    time.sleep(60)

