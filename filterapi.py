'''highly obfuscated'''

import requests
import json

def generic_retry(func):
    def retried_func(*args, **kwargs):
        MAX_TRIES = 3
        tries = 0
        while True:
            try:
                resp = func(*args, **kwargs)
                if tries < MAX_TRIES:
                    return resp
            except:
                if tries < MAX_TRIES:
                    tries += 1
                    continue
        resp = {}
        return resp

    return retried_func


class FilterAPI(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip,deflate',
        }
        self.token = ''  # // Session token for making API calls, call login on instantiation.
        # if not self.token:
        #     self.login()

    @generic_retry
    def post_api(self, url=None, params=None, headers=None):
        req = requests.post(url, params=params, headers=headers)
        count = 0
        while count < 2:
            try:
                return json.loads(req.text)
            except Exception as e:
                params['token'] = self.login()
                count += 1
        return {'result': 'failed'}

    @generic_retry
    def get_api(self, url=None):
        req = requests.get(url)
        count = 0
        while count < 2:
            try:
                return json.loads(req.text)
            except Exception as e:
                count += 1
        return {'result': 'failed', 'status': 'failed', 'code': 400, 'enabled': 'failed'}

    def login(self):
        # // Used to login, in this case this is called automatically to generate a session when instantiating
        #   the class
        data = {'username': 'XXXX', 'password': 'XXXX', 'response': 'json'}
        url = 'https://filter.com/api/Login'
        resp = self.post_api(url, params=data, headers=self.headers)
        self.token = resp['LoginResponse']['result']['token']
        try:
            return resp['LoginResponse']['result']['token']
        except KeyError:
            return ""

    def user_login(self, username, password):
        # // Used to login, in this case this is called automatically to generate a session when instantiating
        #   the class
        data = {'username': username, 'password': password, 'response': 'json'}
        url = 'https://filter.com/api/Login'
        resp = self.post_api(url, params=data, headers=self.headers)
        try:
            self.token = resp['LoginResponse']['result']['token']
            return resp['LoginResponse']['result']['token']
        except:
            return ""



    def reseller_list(self, reseller_name):
        # // Used to get a list of all customers given a reseller name
        #   (only useful for MP as all our customers are customers under us)
        data = {'resellername': reseller_name, 'token': self.token, 'response': 'json'}
        url = 'https://filter.com/api/GetResellerList'
        resp = self.post_api(url, params=data, headers=self.headers)
        try:
            return resp['GetResellerListResponse']['result']
        except KeyError:
            return []

    def customer_list(self, resellername):
        # // Used to get a list of all customers given a reseller name
        #   (only useful for MP as all our customers are customers under us)
        data = {'resellername': resellername, 'token': self.token, 'response': 'json'}
        url = 'https://filter.com/api/GetCustomerList'
        resp = self.post_api(url, params=data, headers=self.headers)
        try:
            return resp['GetCustomerListResponse']['result']
        except KeyError:
            return []

    def domain_list(self, customer_name):
        # // Used to get a list of all domains given a selected customer name
        data = {'customername': customer_name, 'token': self.token, 'response': 'json'}
        url = 'https://filter.com/api/GetDomainList'
        resp = self.post_api(url, params=data, headers=self.headers)
        try:
            return resp['GetDomainListResponse']['result']
        except KeyError:
            return []

    def get_domain(self, domain_name):
        # // Used to get domain information given a specific domain name (useless).
        data = {'domainname': domain_name, 'token': self.token, 'response': 'json'}
        url = 'https://filter.com/api/GetDomain'
        resp = self.post_api(url, params=data, headers=self.headers)
        try:
            return resp['GetDomainResponse']['result']
        except KeyError:
            return None

    def enabled_products(self, domain_name):
        # // Used to get enabled products for a specific customer (I think - the API docs doesn't specify whether
        #    to provide a customer or domain name.
        data = {'domainname': domain_name, 'token': self.token, 'response': 'json'}
        url = 'https://filter.com/api/GetEnabledProducts'
        resp = self.post_api(url, params=data, headers=self.headers)
        try:
            return resp['GetEnabledProductsResponse']['result']
        except KeyError:
            return resp

    def get_mail_config(self, domain_name):
        # // Used to get enabled products for a specific customer (I think - the API docs doesn't specify whether
        #    to provide a customer or domain name.
        data = {'domainname': domain_name, 'token': self.token, 'response': 'json'}
        url = 'https://filter.com/api/GetConfigMailFiltering'
        resp = self.post_api(url, params=data, headers=self.headers)
        try:
            return resp['GetConfigMailFilteringResponse']['result']
        except KeyError:
            return resp
