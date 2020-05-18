#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nSTART time:", datetime.datetime.today()

# url = 'http://erp.thethaosi.vn'
dbname = 'erp'
username = 'admin@thethaosi.vn'
pwd = 'AlphaAdmin2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

# domain_sale = [('confirmation_date', '>=', '2019-10-01 00:00:00'),('confirmation_date', '<=', '2019-11-01 00:00:00'),('state', '=', 'sale'),('sale_order_return', '!=', True)]
domain_sale = [('confirmation_date', '>', '2019-11-01 00:00:00'),('state', '=', 'sale'),('sale_order_return', '!=', True)]
sale_ids = sock.execute(dbname, uid, pwd, 'sale.order', 'search', domain_sale)
print "Tổng đơn hàng %s" % (len(sale_ids))
count = 0
for sale_id in sale_ids:
    count += 1
    state_log_id = sock.execute(dbname, uid, pwd, 'state.log', 'search',
                                 [('state', '=', 'done'), ('sale_id', '=', sale_id), ('date', '!=', False)])
    if state_log_id:
        state_log_id = state_log_id[0]
        state_log_date = sock.execute(dbname, uid, pwd, 'state.log', 'read', state_log_id, ['date'])[0]
        state_log_date = state_log_date.get('date', False)
        sale_name = sock.execute(dbname, uid, pwd, 'sale.order', 'read', sale_id, ['name'])[0]
        sale_name = sale_name.get('name', False)
        invoice_ids = sock.execute(dbname, uid, pwd, 'account.invoice', 'search', [('origin', '=', sale_name)])
        if invoice_ids:
            sock.execute(dbname, uid, pwd, 'account.invoice', 'write', invoice_ids, {
                'date_invoice': state_log_date
            })
    print count
