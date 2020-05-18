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

move_line_ids = sock.execute(dbname, uid, pwd, 'account.move.line', 'search', [
    ('analytic_tag_ids', '=', False)
])
count = 0
for move_line_id in move_line_ids:
    count += 1
    move_line_data = sock.execute(dbname, uid, pwd, 'account.move.line', 'read', move_line_id, ['ref_sale_order'])[0]
    ref_sale_order = move_line_data.get('ref_sale_order', False)
    if ref_sale_order:
        ref_sale_order = ref_sale_order[0]
        so_data = sock.execute(dbname, uid, pwd, 'sale.order', 'read', ref_sale_order, ['so_type_id'])[0]
        so_type_id = so_data.get('so_type_id', False)
        if so_type_id:
            so_type_id = so_type_id[0]
            so_type_data = sock.execute(dbname, uid, pwd, 'sale.order.type', 'read', so_type_id, ['account_analytic_tag_ids'])[0]
            account_analytic_tag_ids = so_type_data.get('account_analytic_tag_ids', False)
            if account_analytic_tag_ids:
                account_analytic_tag_ids = account_analytic_tag_ids[0]
                query = "INSERT INTO public.account_analytic_tag_account_move_line_rel(account_move_line_id, account_analytic_tag_id) VALUES (%s, %s);"% (move_line_id,account_analytic_tag_ids)
                sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
    print count


