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

picking_id = 28693 #
print "pick_action_do_new_transfer - %s" %(picking_id,)
sock.execute(dbname, uid, pwd, 'stock.picking', 'pick_action_do_new_transfer', picking_id)

print 'Done'