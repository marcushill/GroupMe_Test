__author__ = 'Marcus'

import requests


def get_groups(access_token):
    resp = requests.get('https://api.groupme.com/v3/groups', params={'token': access_token})
    data = resp.json()
    return [Group(x, access_token) for x in data['response']]


def get_messages(access_token, group_id):
    pass


class Group():
    def __init__(self, json, access_token):
        self.__initialize(json)
        self.access_token = access_token

    def __initialize(self, json):
        self.id = json['id']
        self.name = json['name']
        self.type = json['type']
        self.description = json['description']
        self.members = [Group_Member(x) for x in json['members']]
        self.last_message = json['messages']['last_message_id']
        self.message_before = False

    def __str__(self):
        result = ["Group {}: name = {} , type = {}".format(self.id, self.name, self.type)]
        result.extend(str(x) for x in self.members)
        return "\n".join(result)

    def refresh(self, access_token):
        if access_token is not None:
            self.access_token = access_token
        url = 'https://api.groupme.com/v3/groups/{}'.format(self.id)
        resp = requests.get(url, params={'token': self.access_token})
        data = resp.json()
        self.__initialize(data['response'])

    def messages(self, page_size=20):
        url = 'https://api.groupme.com/v3/groups/{}/messages'.format(self.id)
        params = {'token': self.access_token, 'limit': page_size}
        store = []
        resp = requests.get(url, params=params)
        data = resp.json()['response']
        store.extend(data['messages'])
        store.reverse()
        while True:
            if resp.json()['meta']['code'] == 304:  # Not Modified response. Essentially nothing more
                print('resp', data)
                raise StopIteration
            if len(store) == 0:
                params['before_id'] = self.last_message
                resp = requests.get(url, params=params)
                data = resp.json()['response']
                store.extend(data['messages'])
                store.reverse()
                yield store.pop()
            else:
                self.last_message = store[0]['id']
                yield store.pop()


class Group_Member():
    def __init__(self, json):
        self.user_id = json["user_id"]
        self.nickname = json["nickname"]
        self.muted = json['muted']
        self.image_url = json['image_url']

    def __str__(self):
        return "Member {}: nickname = {}".format(self.user_id, self.nickname)
