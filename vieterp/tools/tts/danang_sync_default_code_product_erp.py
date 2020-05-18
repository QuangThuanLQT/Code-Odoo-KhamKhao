#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime

print "\nSTART time:", datetime.datetime.today()

url = 'http://danang.konek.vn'
dbname = 'danang'
username = 'admin@thethaosi.vn'
pwd = 'AlphaAdmin2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

workbook = xlrd.open_workbook('/Users/telephony/code/vieterp-10/addons/equip/vieterp/tools/tts/dong_bo_default_code_danang_erp.xlsx')
worksheet = workbook.sheet_by_index(0)

num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = 0
curr_row_1 = 0
list_product_edit = []
while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)

    default_code = row[1].value.strip()
    erp_default_code = row[0].value.strip()
    if default_code:
        product_id = sock.execute(dbname, uid, pwd, 'product.product', 'search', [
            '|', ('active', '=', True),
             ('active', '=', False),
            ('default_code', '=', default_code),
            ('id', 'not in', list_product_edit)
        ])
        if product_id:
            sock.execute(dbname, uid, pwd, 'product.product', 'write', product_id, {
                'default_code': 'D' + default_code,
            })
            print 'edit %s' % default_code
    print curr_row
while curr_row_1 < num_rows:
    curr_row_1 += 1
    row = worksheet.row(curr_row_1)

    ddefault_code = 'D' + row[1].value.strip()
    erp_default_code = row[0].value.strip()
    if erp_default_code:
        product_id = sock.execute(dbname, uid, pwd, 'product.product', 'search', [
            '|', ('active', '=', True),
             ('active', '=', False),
            ('default_code', '=', ddefault_code),
            ('id', 'not in', list_product_edit)
        ])
        if product_id:
            sock.execute(dbname, uid, pwd, 'product.product', 'write', product_id, {
                'default_code': erp_default_code,
            })
            print '%s' % erp_default_code
    print curr_row_1
print 'Done'