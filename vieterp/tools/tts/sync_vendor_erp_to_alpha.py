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
vendor_ids = sock1.execute(dbname1, uid1, pwd1, 'res.partner', 'search', [
    '|',
    ('active', '=', False),
    ('active', '=', True),
    ('supplier', '=', True)
])
for vendor_id in vendor_ids:
    count += 1
    if count > 0:
        product_data = sock1.execute(dbname1, uid1, pwd1, 'res.partner', 'copy_data', [vendor_id])
        # new_product_id = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'create', product_data)
        a_vendor_id = sock2.execute(dbname2, uid2, pwd2, 'res.partner', 'search',
                                    ['|', ('active', '=', False), ('active', '=', True), ('supplier', '=', True),
                                     ('ref', '=', product_data['ref'])])
        if a_vendor_id:
            sock2.execute(dbname2, uid2, pwd2, 'res.partner', 'write', a_vendor_id[0], product_data)
            print 'write - %s' % (a_vendor_id[0])
        else:
            new_vendor_id = sock2.execute(dbname2, uid2, pwd2, 'res.partner', 'create', product_data)
            print 'create - %s' % (new_vendor_id)
    print count
