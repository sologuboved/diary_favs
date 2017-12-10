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
                for line1, line2 in zip(handler1.readlines(), handler2.readlines()):
                    # print()
                    # print()
                    # print(1, line1)
                    # print(2, line2)
                    if line1 != line2:
                        # print("NOOOOOOOOOOOO")
                        print()
                        print(line1)
                        print(line2)
                        print()
                        print()
                        # for ind in range(len(line2)):
                        #     if line1[ind] != line2[ind]:
                        #         print(line1[ind])
                        #         print(line2[ind])
                        #         print(len(line1))
                        #         print(len(line2))
                        # print(len(line2))
                        break
                else:
                    print('ok')
        except FileNotFoundError:
            break
        print()
        index += 1


if __name__ == '__main__':
    pass
    # compare(CREEPY)
    # compare(O_E)
    compare(RSYA)
    # i = 1
    # with open(O_E + FOLDER_POSTFIX + '/' + THREAD + str(11) + '.txt', encoding='utf-8') as h:
    #     for line in h.readlines():
    #         print(i, line)
    #         i += 1


