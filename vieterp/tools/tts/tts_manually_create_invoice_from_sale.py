#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import datetime
print "\nSTART time:", datetime.datetime.today()

url = 'http://localhost:8069'
dbname = 'thethaosi'
username = 'thethaosi'
pwd = 'ERPTTS2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

sale_ids = sock.execute(dbname, uid, pwd, 'sale.order', 'search', [('confirmation_date', '>=', '2019-10-10 00:00:00')])
# sale_ids = [11003, 11001]

# product_id = sock.execute(dbname, uid, pwd, 'ir.values', 'get_default', ['sale.config.settings', 'deposit_product_id_setting'])
# print product_id

for sale_id in sale_ids:
    sale = sock.execute(dbname, uid, pwd, 'sale.order', 'read', sale_id, ['invoice_count', 'trang_thai_dh'])[0]
    print 'sale - %s - %s' % (sale['invoice_count'], sale['trang_thai_dh'],)
    if sale['invoice_count'] == 0 and sale['trang_thai_dh'] in ['done', 'delivery']:
        print 'action_picking_create_so_invoice - %s' %(sale_id)
        sock.execute(dbname, uid, pwd, 'sale.order', 'directly_create_inv', [sale_id], {'no_qty_invoiced': True})
        print 'invoiced - %s' % (sale_id)
        sock.execute(dbname, uid, pwd, 'sale.order', 'update_line_qty_invoiced', [sale_id])
        print 'done - %s' % (sale_id)

print 'Done'