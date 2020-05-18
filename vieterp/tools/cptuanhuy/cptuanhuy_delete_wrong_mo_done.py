#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nSTART time:", datetime.datetime.today()

url = 'http://cptuanhuy.konek.vn'
dbname = 'cptuanhuy'
username = 'admin'
pwd = 'admin'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

mo_ids = sock.execute(dbname, uid, pwd, 'mrp.production', 'search', [
    ('picking_type_id', '=', 4), # Xuat kho
    ('location_dest_id', '=', 9), # Xuat kho
    ('name', '=like', '%XK/OUT/%'),
], 0, 0)

mo_length = len(mo_ids)
mo_index  = 0

for mo_id in mo_ids:
    mo_index += 1
    print "Delete mrp.production - %s - %s / %s" %(mo_id, mo_index, mo_length)
    try:
        sock.execute(dbname, uid, pwd, 'mrp.production', 'action_delete_production', [mo_id])
    except Exception, e:
        print str(e)

print 'Done'