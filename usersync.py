import random, string
from filter import Filter
from apiserver import APIserver


fl = Filter()
apiserv = APIserver()


def main():
    fl.login()
    customers = apiserv.get_customers()
    for customer in customers:
        service_id = str(customer.get('service_id'))
        print('current customer ' + service_id)
        apiserv_id = customer[id]
        users_to_add = users_service(service_id, apiserv_id)
        apiserv_users = apiserv.get_users(apiserv_id)
        print(users_to_add)
        print(apiserv_users)
        compare = compare_users(apiserv_users, users_to_add)
        create_users(compare, service_id)


def users_service(customer, apiserv_id):
    print(fl.get_userlist(customer))
    try:
        response = fl.get_userlist(customer).get('result')['user']
        FL_users = []
        for each in response:
            FL_users.append(each.get('name').lower())
    except KeyError:
        apiserv_users = apiserv.get_users(apiserv_id)
        print(apiserv_users)
        create_users(apiserv_users, customer)
    return FL_users


def compare_users(o365users, FL_users):
    missing_users = list(set(o365users) - set(FL_users))
    if missing_users == []:
        print('No missing users')
    else:
        print('Missing users: ')
        print(missing_users)
    return missing_users


def create_users(missing_users, customer):
    randpass = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    for each in missing_users:
        try:
            resp = fl.create_user(each.lower(), randpass, customer)
            print(resp)
            if resp.get('status').get('content') == 'OK':
                print('user added:', each)
            elif resp.get('status').get('content') == 'AlreadyExists':
                print('User domain exists under a different customer:', each)
            else:
                print('could not create user:', each)
        except KeyError:
            print(resp)
            continue


if __name__ == '__main__':
    main()
