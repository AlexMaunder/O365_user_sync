import requests
import json


URL = 'https://apiserver.io/api/office365/19445/services/'

TOKEN = 'XXXX'


class Converge(object):
    def __init__(self):
        self.url = 'https://apiserver.io/api'
        self.session = requests.session()
        self.session.headers['Authorization'] = 'Token ' + TOKEN
        self.session.headers['Content-Type'] = 'application/json'

    def get_customers(self):
        customers = [
            {id: '1XXX5', 'filter_id': 'domain.com'},
			{id: 'XXXXX', 'filter_id': 'domain.com'},
        ]
        return customers

    def get_users(self, customer_id):
        url = self.url + '/office365/' + customer_id + '/services/'
        response = self.session.get(url)
        users = json.loads(response.text)
        o365users = []
        f = users.get('users')
        for each in f:
            o365_user = each.get('mail')
            if not o365_user:
                continue
            o365users.append(o365_user.lower())
        print(o365users)
        return o365users
