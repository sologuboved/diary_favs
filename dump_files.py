# -*- coding: utf-8 -*-

import json
import os
from global_vars import *


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
