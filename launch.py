# -*- coding: utf-8 -*-

from scrape import *
from dump_files import *
from selectae import *


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

    # launch(1, FANFICTION, collate_urls=(F_P, fanfiction))


