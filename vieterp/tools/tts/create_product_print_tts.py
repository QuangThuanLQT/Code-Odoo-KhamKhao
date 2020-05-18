#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nSTART time:", datetime.datetime.today()

url = 'http://alpha.konek.vn'
dbname = 'alpha'
username = 'admin@thethaosi.vn'
pwd = 'AlphaAdmin2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

product_ids = sock.execute(dbname, uid, pwd, 'product.template', 'search', ['|',('active', '=', False),('active', '=', True)])
# sock.execute(dbname, uid, pwd, 'product.template', 'create_product_print', product_ids)
sock.execute(dbname, uid, pwd, 'product.template', 'create_config_product_print', product_ids)
