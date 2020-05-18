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

workbook = xlrd.open_workbook('/Users/vieterp/code/vieterp/tools/tts/Danh_sach_SO_chua_co_Invoice.xlsx')
worksheet = workbook.sheet_by_index(0)

num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = 0

while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)

    if len(row) > 2:
        sale_name = row[0].value
        sale_ids  = sock.execute(dbname, uid, pwd, 'sale.order', 'search', [
            ('name', '=', sale_name)
        ])
        print "order_name: %s - %s" % (sale_name, sale_ids,)

        for sale_id in sale_ids:
            sale = sock.execute(dbname, uid, pwd, 'sale.order', 'read', sale_id, ['invoice_count', 'trang_thai_dh'])[0]
            print 'sale - %s - %s' % (sale['invoice_count'], sale['trang_thai_dh'],)
            if sale['invoice_count'] == 0 and sale['trang_thai_dh'] in ['done', 'delivery']:
                print 'action_picking_create_so_invoice - %s' %(sale_id)
                sock.execute(dbname, uid, pwd, 'stock.picking', 'action_picking_create_so_invoice', sale_id, sale_id, [sale_id])
                print 'done - %s' % (sale_id)

print 'Done'