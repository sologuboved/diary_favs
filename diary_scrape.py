# -*- coding: utf-8 -*-

import os
import json
import re
import requests
import html
from bs4 import BeautifulSoup
from select_threads import *
from global_vars import *

STEP = 20


def load_json(json_filename):
    with open(json_filename) as data:
        return json.load(data)


def dump_json(entries, json_filename):
    with open(json_filename, 'w') as handler:
        json.dump(entries, handler)


def json_to_txt(json_filename, txt_filename):
    thread = sorted(load_json(json_filename).items(), key=lambda entry: int(entry[0].split()[0]))
    with open(txt_filename, 'w', encoding='utf-8') as handler:
        for date, post in thread:
            handler.write(date + '\n')
            handler.write(post + '\n\n\n\n')


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


def dump_thread(thread, folder_prefix, filename_index):
    foldername = folder_prefix + FOLDER_POSTFIX
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    filename = foldername + '/' + THREAD + str(filename_index)  # e.g. 'o_e' + '_threads/' + 'thread' + 1
    json_filename = filename + '.json'
    txt_filename = filename + '.txt'

    print("Dumping %s..." % json_filename)
    dump_json(thread, json_filename)
    print("Dumping %s..." % txt_filename)
    json_to_txt(json_filename, txt_filename)
    print()


def scrape_thread(thread_url, thread_index=1, total=1):
    print("Scraping thread %s (%d out of %d)" % (thread_url, thread_index, total))

    thread_html = requests.get(thread_url).content
    thread_html = thread_html.replace('&'.encode(), '&amp;'.encode())  # otherwise "save&kill, да" --> "save&kill;, да"
    soup = BeautifulSoup(thread_html, 'html.parser')

    for tag_br in soup.find_all('br'):  # keeping paragraphs
        tag_br.replace_with('\n')

    for tag_a in soup.find_all('a', href=True):  # keeping links
        tag_a.replace_with(tag_a.text + ' ' + '<' + tag_a.get('href') + '>')

    print(soup)

    print('dates:', end=' ')
    dates = list()
    raw_dates = soup.find_all('div', {'class': 'postTitle header'})
    # e.g. "Правда №8432"
    title = raw_dates.pop(0).find('h2').text
    # e.g. <span title="1 год 1 месяц назад">Вторник, 04 октября 2016</span></div> --> "04 октября 2016"
    first_date = soup.find('div', {'id': 'post' + url_to_num(thread_url)}).find('span').text.split(',')[1][1:]
    # e.g. "0 (http://fandomnaya-pravda.diary.ru/p210614015.htm) Правда №8432 - 04 октября 2016"
    dates.append('0' + " (" + thread_url + ") " + title + ' - ' + first_date)
    print(0, end=' ')

    index = 1
    for date in raw_dates:
        date = date.find('span').text.split()
        dates.append(str(index) + ' ' + date[0] + ' ' + date[2])  # e.g. 2017-11-14 в 17:30 --> "57 2017-11-14 17:30"
        print(index, end=' ')
        index += 1
    print()

    print('posts:', end=' ')
    posts = list()
    raw_posts = soup.find_all('div', {'class': 'postContent'})
    # print(raw_posts)
    index = 0

    for raw_post in raw_posts:
        post = process_post(raw_post)
        if post:
            posts.append(post)
        else:
            posts.append(u'<some missing media>')
        print(index, end=' ')
        index += 1
    print()

    assert len(dates) == len(posts), (len(dates), len(posts))

    return dict(zip(dates, posts))  # combining dates and posts


def process_post(raw_post):
    raw_post = raw_post.find('div', {'class': 'postInner'}).find('div', {'class': 'paragraph'})

    clean_post = raw_post.find('div').text

    quotations = raw_post.find_all('span', {'class': 'quote_text'})
    if quotations:
        for raw_quotation in quotations:
            raw_quotation = raw_quotation.text
            clean_quotation = '\n\n[[[[' + raw_quotation + ']]]]\n\n'
            clean_post = clean_post.replace(raw_quotation, clean_quotation)

    clean_post = html.unescape(clean_post)  # otherwise >< --> &gt;&lt;
    clean_post = clean_post.replace('¤', '&curren')  # otherwise /?action=view&current --> /?action=view¤t

    return clean_post


def launch(filename_index, folder_prefix, collate_urls=None, scrape_urls=None):
    # e.g.:
    # launch(1, FANFICTION, collate_urls=('fandomnaya-pravda', fanfiction))
    # launch(1, CREEPY, scrape_urls='http://fandomnaya-pravda.diary.ru/?tag=127627')
    print(folder_prefix.upper())
    print()

    if collate_urls:
        diary, thread_nums = collate_urls
        thread_urls = collate_all_urls(diary, thread_nums)
    elif scrape_urls:
        thread_urls = scrape_all_urls(scrape_urls)
    else:
        print("No urls!")
        return

    thread_index = 1
    total = len(thread_urls)
    for thread_url in thread_urls:
        thread = scrape_thread(thread_url, thread_index, total)
        dump_thread(thread, folder_prefix, filename_index)
        thread_index += 1
        filename_index += 1


if __name__ == '__main__':
    pass
    # launch(1, CREEPY, scrape_urls=creepy)
    # launch(21, CREEPY, scrape_urls=perev1)
    # launch(24, CREEPY, scrape_urls=perev2)

    # launch(1, O_E, scrape_urls=o_e)

    # launch(1, RSYA, scrape_urls=rsya1)
    # launch(7, RSYA, scrape_urls=rsya2)

    # launch(1, ROLEPLAY, scrape_urls=roleplay)
    #
    # launch(1, FEMSLASH, scrape_urls=femslash)
    #
    # launch(1, KINKS, scrape_urls=kinks)
    #
    # launch(1, SOCIONICS, scrape_urls=socionics)

    scrape_thread('http://fandomnaya-pravda.diary.ru/p210590156.htm')
