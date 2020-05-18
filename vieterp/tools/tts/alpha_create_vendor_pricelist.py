#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nSTART time:", datetime.datetime.today()

# url = 'http://alpha.konek.vn'
# dbname = 'alpha'
# username = 'admin@thethaosi.vn'
# pwd = 'AlphaAdmin2019'

url = 'http://localhost:8069'
dbname = 'tts_alpha'
username = 'admin@thethaosi.vn'
pwd = 'AlphaAdmin2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

product_ids = sock.execute(dbname, uid, pwd, 'product.template', 'search', [])
count = 0
for product_id in product_ids:
    count += 1
    supplierinfo_data = {
        'product_tmpl_id': product_id,
        'name': 9116,
        'delay': 1,
        'min_qty': 0,
    }
    supplierinfo_id = sock.execute(dbname, uid, pwd, 'product.supplierinfo', 'create', supplierinfo_data)
    sock.execute(dbname, uid, pwd, 'product.supplierinfo', 'create_product_supplierinfo_line', supplierinfo_id)
    print count

print "\nDone time:",datetime.datetime.today()