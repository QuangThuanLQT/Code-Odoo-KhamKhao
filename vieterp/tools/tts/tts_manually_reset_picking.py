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

picking_id = 28555 #
# print "do_reset_stock_picking - %s" %(picking_id,)
# sock.execute(dbname, uid, pwd, 'stock.picking', 'do_reset_stock_picking', picking_id)

print "delete stock_pack_operation - %s" %(picking_id,)
query = "DELETE FROM stock_pack_operation WHERE picking_id = %s" % (picking_id,)
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

print "unlink.stock.picking - %s" %(picking_id,)
sock.execute(dbname, uid, pwd, 'stock.picking', 'unlink', picking_id)

print 'Done'