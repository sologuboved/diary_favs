# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from global_vars import *


def url_to_num(url):
    # e.g.:
    # http://fandomnaya-pravda.diary.ru/p214133239.htm --> 214133239
    return str(re.findall('p(\d*)\.htm', url)[0])


def num_to_url(diary, thread_num):
    # e.g.:
    # 'fandomnaya-pravda', 214133239 --> http://fandomnaya-pravda.diary.ru/p214133239.htm
    return URL % (diary, thread_num)


def collate_all_urls(diary, thread_nums):
    # e.g.:
    # collate_all_urls('fandomnaya-pravda', [214133239, 214101823])
    # -->
    # [http://fandomnaya-pravda.diary.ru/p214133239.htm, http://fandomnaya-pravda.diary.ru/p214101823.htm]
    print("Collating thread urls...")
    thread_urls = [num_to_url(diary, thread_num) for thread_num in map(str, thread_nums)]
    print(len(thread_urls), "thread urls collected")
    print()
    return thread_urls


def scrape_all_urls(initial_url):
    # e.g.:
    # scrape_all_urls('http://fandomnaya-pravda.diary.ru/?tag=91761') collects all urls for posts under this tag
    print("Scraping thread urls...")
    thread_urls = list()
    span = 0
    while True:
        page_url = initial_url + FROM + str(span)
        print(page_url)
        new_urls = scrape_urls_from_page(page_url)
        if new_urls:
            thread_urls.extend(new_urls)
            span += STEP
        else:  # "Нет записей"
            break
    print(len(thread_urls), "thread urls collected")
    print()
    return thread_urls


def scrape_urls_from_page(page_url):
    # e.g.:
    # scrape_all_urls('http://fandomnaya-pravda.diary.ru/?tag=91761&from=20') collects all urls for posts from the
    # given page
    page_html = requests.get(page_url).content
    soup = BeautifulSoup(page_html, 'html.parser')
    raw_links = soup.find_all('div', {'class': 'postLinksBackg'})
    return [raw_link.find('span', {'class': 'urlLink'}).find('a').get('href') for raw_link in raw_links]
