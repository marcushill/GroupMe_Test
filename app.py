__author__ = 'Marcus'

import group_me as gm


def main():
    with open('TOKEN') as f:
        ACCESS_TOKEN = f.read()
    for g in gm.get_groups(ACCESS_TOKEN):
        i = 1
        for message in g.messages(100):
            print(i, '. ', message['text'])
            i += 1


main()