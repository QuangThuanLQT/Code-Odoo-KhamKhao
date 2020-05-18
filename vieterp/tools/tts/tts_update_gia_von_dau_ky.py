#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime

print "\nSTART time:", datetime.datetime.today()

url = 'http://localhost:8069'
dbname = 'tts_live_test'
username = 'admin@thethaosi.vn'
pwd = 'AlphaAdmin2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

workbook = xlrd.open_workbook('/Users/vieterp/code/vieterp/tools/tts/product_cost_update.xlsx')
worksheet = workbook.sheet_by_index(0)

num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = 0

while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)

    default_code = row[0].value.strip()
    cost = row[3].value or 0
    if default_code:
        product_id = sock.execute(dbname, uid, pwd, 'product.product', 'search', [
            '|', ('active', '=', True),
             ('active', '=', False),
            ('default_code', '=', default_code)
        ])
        if product_id:
            sock.execute(dbname, uid, pwd, 'product.price.history', 'create', {
                'product_id': product_id[0],
                'cost': cost,
                'company_id': 1,
                'datetime': "2019-08-01 00:00:00",
            })

            history_ids = sock.execute(dbname, uid, pwd, 'product.price.history', 'search', [
                ('product_id', '=', product_id[0]),
                ('datetime','<', "2019-08-01 00:00:00")
            ])

            sock.execute(dbname, uid, pwd, 'product.price.history', 'write', history_ids, {
                'cost': cost,
            })
    print curr_row

print 'Done'