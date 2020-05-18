#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime

print "\nstart time:", datetime.datetime.today()

dbname1 = 'erp'
username1 = 'admin@thethaosi.vn'
pwd1 = 'AlphaAdmin2019'

sock_common1 = xmlrpclib.ServerProxy('http://erp.thethaosi.vn/xmlrpc/common')
sock1 = xmlrpclib.ServerProxy('http://erp.thethaosi.vn/xmlrpc/object')
uid1 = sock_common1.login(dbname1, username1, pwd1)

dbname2 = 'alpha'
username2 = 'admin@thethaosi.vn'
pwd2 = 'AlphaAdmin2019'

sock_common2 = xmlrpclib.ServerProxy('http://alpha.konek.vn/xmlrpc/common')
sock2 = xmlrpclib.ServerProxy('http://alpha.konek.vn/xmlrpc/object')
uid2 = sock_common2.login(dbname2, username2, pwd2)

count = 0
customer_ids = sock1.execute(dbname1, uid1, pwd1, 'res.partner', 'search', [
    '|',
    ('active', '=', False),
    ('active', '=', True),
    ('customer', '=', True)
])
for customer_id in customer_ids:
    count += 1

    customer_data = sock1.execute(dbname1, uid1, pwd1, 'res.partner', 'copy_data', [customer_id])

    if customer_data['ref']:
        a_customer_id = sock2.execute(dbname2, uid2, pwd2, 'res.partner', 'search', [
            '|',
            ('active', '=', False),
            ('active', '=', True),
            ('customer', '=', True),
            ('ref', '=', customer_data['ref'])
        ])
        # del customer_data['user_id']
        # del customer_data['transport_route_id']
        if a_customer_id:
            if customer_data['user_id']:
                user_data = sock1.execute(dbname1, uid1, pwd1, 'res.users', 'read', [customer_data['user_id']])[0]

                a_user_id = sock2.execute(dbname2, uid2, pwd2, 'res.users', 'search', [
                    # '|',
                    ('active', '=', False),
                    # ('active', '=', True),
                    ('login', '=', user_data['login'])
                ])

                if a_user_id:
                    sock2.execute(dbname2, uid2, pwd2, 'res.partner', 'write', a_customer_id[0], {
                        'user_id': a_user_id[0],
                    })
                else:
                    print 'login not exists - %s' % (user_data['login'])
            else:
                sock2.execute(dbname2, uid2, pwd2, 'res.partner', 'write', a_customer_id[0], {
                    'user_id': False,
                })
            print 'write - %s' % (a_customer_id[0])
        else:
            new_customer_id = sock2.execute(dbname2, uid2, pwd2, 'res.partner', 'create', customer_data)
            print 'create - %s' % (new_customer_id)
        # pass
    else:
        print 'customer do not have ref - %s' % (customer_id)
    print "%s / %s " %(count, len(customer_ids),)
