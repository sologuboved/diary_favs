# -*- coding: utf-8 -*-

# C:/Users/vesna/Documents/Werecoder/diary_favs_py3/o_e_threads2/thread1.txt

import os


def rename_files():
    for foldername in os.listdir('.'):
        if '.' not in foldername and '__' not in foldername and '_old' in foldername:
            print()
            print(foldername)
            for old_filename in os.listdir(foldername):
                filename, extension = old_filename.split('.')
                new_filename = filename + '_old.' + extension
                os.rename(foldername + '/' + old_filename, foldername + '/' + new_filename)


def rename_directories():
    for old_foldername in os.listdir('.'):
        if '.' not in old_foldername and '__' not in old_foldername and '2' in old_foldername:
            new_foldername = old_foldername[: -1] + '_old'
            os.rename(old_foldername, new_foldername)


if __name__ == '__main__':
    # rename_directories()
    # rename_files()
    pass
