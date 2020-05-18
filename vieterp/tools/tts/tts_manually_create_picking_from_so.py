#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nSTART time:", datetime.datetime.today()

url = 'http://erp.kapp.vn'
dbname = 'erp'
username = 'thethaosi'
pwd = 'ERPTTS2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

sale_id = 9947
sock.execute(dbname, uid, pwd, 'sale.order', 'create_so_picking_from_queue', sale_id)

print 'Done'