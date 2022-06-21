import requests
import time
import datetime
from bs4 import BeautifulSoup, SoupStrainer
from dhooks import Webhook

pagelink = "https://www.stylefile.de/suche?q=air+force+1&start=0&sz=50"
sendto_webhook = "https://discord.com/api/webhooks/822574588129968179/KVtDJPGx_90FWzbY6vL1GvJNE3KLdDoGfmsiNf8pEuYX6E4pCF6Tf1cWLBinnLrygRFF"


def find_all_items_stylefile(func_link):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    search_result_content = SoupStrainer('div', attrs={'class': 'search-result-content'})
    result = requests.get(func_link, 'lxml', headers=headers)
    soup = BeautifulSoup(result.content, "html.parser", parse_only=search_result_content)
    lists = soup.find_all('li', class_="grid-tile")
    dict_all_pids = dict()
    dict_keys = set()

    for item in lists:
        item_name_and_link = item.find('a', class_="thumb-link")
        item_name = item_name_and_link['title']
        item_link = item_name_and_link['href']
        pid = item.find('div', class_="product-tile")['data-producttilempid']
        dict_keys.add(pid)
        dict_all_pids[pid] = {"sku": pid, "name": item_name, "link": item_link}

    return dict_all_pids, dict_keys


def discord_send(text, local_dict=dict(), dict_keys=set()):
    hook = Webhook(sendto_webhook)
    item_info = str()
    dict_values = ["sku", "name", "link"]
    for key in dict_keys:
        for d in dict_values:
            item_info += local_dict[str(key)][d] + " "
        item_info += " | "
    hook.send(str(text + item_info))


def log(action):
    print(str(datetime.datetime.now()) + " " + action + str(len(keys_set_base)) + str(len(keys_set_new)), flush=True)


dict_base, keys_set_base = find_all_items_stylefile(pagelink)
discord_send("launched")
while True:
    dict_new, keys_set_new = find_all_items_stylefile(pagelink)
    if len(keys_set_new) != len(keys_set_base):
        if len(keys_set_new) > len(keys_set_base):
            discord_send("New item: ", dict_new, (keys_set_new - keys_set_base))
            log("change")
            print("base: " + str(keys_set_base))
            print("new:  " + str(keys_set_new))
            keys_set_base = keys_set_new
            dict_base = dict_new
        elif len(keys_set_new) < len(keys_set_base):
            discord_send("Item removed: ", dict_base, (keys_set_base - keys_set_new))
            log("change")
            print("base: " + str(keys_set_base))
            print("new:  " + str(keys_set_new))
    else:
        if len(keys_set_new) == len(keys_set_base):
            log("success")
        else:
            print("error1")
            print("base: " + str(keys_set_base))
            print("new:  " + str(keys_set_new))
    keys_set_base = keys_set_new
    dict_base = dict_new
    time.sleep(60)
