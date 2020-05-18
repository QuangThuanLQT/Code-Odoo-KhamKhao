#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime

print "\nSTART time:", datetime.datetime.today()

url = 'http://danang.konek.vn'
dbname = 'danang'
username = 'thethaosi'
pwd = 'ERPTTS2019'


sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

res_users = sock.execute(dbname, uid, pwd, 'res.users', 'search', [('id', '=', 1)])
print res_users

#
# workbook = xlrd.open_workbook('/Users/vieterp/code/vieterp/tools/tts/product_attribute_value.xls')
# worksheet = workbook.sheet_by_index(0)
#
# num_rows = worksheet.nrows - 1
# num_cells = worksheet.ncols - 1
# curr_row = 0
#
# while curr_row < num_rows:
#     curr_row += 1
#     row = worksheet.row(curr_row)
#
#     attribute_name = row[0].value.strip()
#     product_attribute_name = row[1].value.strip()
#     phi_in = row[2].value
#     he_so_dien_tich = row[3].value
#
#     attribute_id = sock.execute(dbname, uid, pwd, 'prinizi.product.attribute', 'search', [
#         ('name', '=', attribute_name)
#     ])
#     if not attribute_id:
#         attribute_id = sock.execute(dbname, uid, pwd, 'prinizi.product.attribute', 'create', {
#             'name': attribute_name,
#         })
#     else:
#         attribute_id = attribute_id[0]
#
#     sock.execute(dbname, uid, pwd, 'prinizi.product.attribute.value', 'create', {
#         'attribute': attribute_id,
#         'name' : product_attribute_name,
#         'phi_in' : phi_in,
#         'he_so_dien_tich' : he_so_dien_tich,
#     })
#
# print "\nDone time:",datetime.datetime.today()
