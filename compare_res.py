# -*- coding: utf-8 -*-

from global_vars import *


def compare(folder_prefix):
    print('Comparing:')
    index = 1
    while True:
        filename1 = folder_prefix + FOLDER_POSTFIX + '/' + THREAD + str(index) + '.txt'
        filename2 = folder_prefix + FOLDER_POSTFIX + '_old/' + THREAD + str(index) + '_old.txt'
        try:
            with open(filename1, encoding='utf-8') as handler1, open(filename2, encoding='utf-8') as handler2:
                print(filename1, filename2, end=' ')
                file1 = handler1.readlines()
                file2 = handler2.readlines()
                zipped = zip(file1, file2)
                if (not len(list(zipped))) and (file1 or file2):
                    print("One of the files is empty")
                else:
                    for line1, line2 in zip(file1, file2):
                        if line1 != line2:
                            print()
                            print(line1)
                            print(line2)
                            print()
                            print()
                            break
                    else:
                        print('ok')
        except FileNotFoundError:
            break
        print()
        index += 1


if __name__ == '__main__':
    pass
