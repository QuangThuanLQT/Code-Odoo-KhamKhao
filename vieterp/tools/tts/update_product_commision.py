#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime

print "\nSTART time:", datetime.datetime.today()

url = 'http://localhost:8069'
dbname = 'tts_erp'
username = 'thethaosi'
pwd = 'ERPTTS2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

workbook = xlrd.open_workbook('/Users/vieterp/code/vieterp/tools/tts/Sales_Config_Commissions.xlsx')
worksheet = workbook.sheet_by_index(0)

num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = 0

while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)

    default_code = row[1].value.strip()
    commision = row[9].value * 100
    if default_code and commision:
        product_id = sock.execute(dbname, uid, pwd, 'product.product', 'search', [
                ('default_code', '=', default_code)
            ])
        if product_id:
            sock.execute(dbname, uid, pwd, 'product.product', 'write', product_id, {
                'commision': commision,
            })
    print curr_row

print 'Done'