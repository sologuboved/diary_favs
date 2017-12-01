# -*- coding: utf-8 -*-

THREAD = 'thread'
FOLDER_POSTFIX = '_threads/'
CREEPY = 'creepy'
FANFICTION = 'fanfiction'
SOCIAL = 'social'
ROLEPLAY = 'roleplay'
RSYA = 'rsya'
FEMSLASH = 'femslash'
O_E = 'o_e'
MISC = 'misc'


def compare(till, folder_prefix1, folder_prefix2):
    print 'Comparing:'
    for index in range(1, till + 1):
        filename1 = folder_prefix1 + FOLDER_POSTFIX + THREAD + str(index) + '.txt'
        filename2 = folder_prefix2 + FOLDER_POSTFIX + THREAD + str(index) + '.txt'
        print filename1, filename2,
        with open(filename1) as handler1, open(filename2) as handler2:
            for line1, line2 in zip(handler1.readlines(), handler2.readlines()):
                if line1 != line2:
                    print
                    print line1
                    print line2
                    break
            else:
                print "are fine"
        print


if __name__ == '__main__':
    compare(50, ROLEPLAY, ROLEPLAY + '2')
