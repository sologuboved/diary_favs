# -*- coding: utf-8 -*-

import html
from generate_urls import *


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


if __name__ == '__main__':
    pass
