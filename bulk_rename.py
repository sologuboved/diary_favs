# -*- coding: utf-8 -*-

import os


def shift_indices(foldername, new_final, step):
    ind = new_final
    while ind > step:
        txt_old_filename = foldername + '/' + 'thread%d_old.txt' % (ind - step)
        json_old_filename = foldername + '/' + 'thread%d_old.json' % (ind - step)
        txt_new_filename = foldername + '/' + 'thread%d_old.txt' % ind
        json_new_filename = foldername + '/' + 'thread%d_old.json' % ind
        print(txt_old_filename, txt_new_filename)

        os.rename(txt_old_filename, txt_new_filename)
        os.rename(json_old_filename, json_new_filename)

        ind -= 1


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
    # shift_indices('kinks_threads_old', 22, 1)
    pass
