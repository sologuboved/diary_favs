# -*- coding: utf-8 -*-

THREAD = 'thread'
FOLDER_POSTFIX = '_threads'
CREEPY = 'creepy'
FANFICTION = 'fanfiction'
SOCIAL = 'social'
ROLEPLAY = 'roleplay'
RSYA = 'rsya'
FEMSLASH = 'femslash'
O_E = 'o_e'
MISC = 'misc'


def compare(folder_prefix):
    print('Comparing:')
    index = 1
    while True:
        filename1 = folder_prefix + FOLDER_POSTFIX + '/' + THREAD + str(index) + '.txt'
        filename2 = folder_prefix + FOLDER_POSTFIX + '2/' + THREAD + str(index) + '.txt'
        try:
            with open(filename1, encoding='utf-8') as handler1, open(filename2, encoding='utf-8') as handler2:
                print(filename1, filename2, end=' ')
                for line1, line2 in zip(handler1.readlines(), handler2.readlines()):
                    if line1 != line2:
                        print()
                        print()
                        print(line1)
                        print(line2)
                        break
                else:
                    print('ok')
        except FileNotFoundError:
            break
        print()
        index += 1


if __name__ == '__main__':
    compare(CREEPY)
