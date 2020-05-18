#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nSTART time:", datetime.datetime.today()

url = 'http://alpha.konek.vn'
dbname = 'alpha'
username = 'admin@thethaosi.vn'
pwd = 'AlphaAdmin2019'

# url = 'http://localhost:8069'
# dbname = 'tts_alpha'
# username = 'admin@thethaosi.vn'
# pwd = 'AlphaAdmin2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

# product_ids = sock.execute(dbname, uid, pwd, 'product.product', 'search', ['|',('active', '=', False),('active', '=', True)])
# sock.execute(dbname, uid, pwd, 'product.product', 'write', product_ids, {
#         'standard_price' : 0
#     })

# query = "DELETE FROM product_price_history;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE procurement_order DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM procurement_order;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE procurement_order ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_move DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM stock_move;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_move ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_pack_operation DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM stock_pack_operation;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_pack_operation ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_picking DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM stock_picking;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_picking ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE sale_order_line DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM sale_order_line"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE sale_order_line ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE sale_order DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM sale_order;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE sale_order ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE purchase_order_line DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM purchase_order_line;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE purchase_order_line ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE purchase_order DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM purchase_order;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE purchase_order ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_invoice_line DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM account_invoice_line;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_invoice_line ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_invoice DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM account_invoice;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_invoice ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM account_partial_reconcile;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_move_line DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM account_move_line;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_move_line ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_move DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM account_move;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_move ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_voucher_line DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM account_voucher_line;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_voucher_line ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_voucher DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM account_voucher;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE account_voucher ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_inventory_line DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM stock_inventory_line;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_inventory_line ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM stock_inventory;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_quant DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM stock_quant;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_quant ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE income_inventory DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM income_inventory;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE income_inventory ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# query = "ALTER TABLE stock_picking_history DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM stock_picking_history;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE stock_picking_history ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# query = "ALTER TABLE product_variants_line DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM product_variants_line;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE product_variants_line ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE product_supplierinfo DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM product_supplierinfo;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE product_supplierinfo ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# query = "ALTER TABLE inventory_history DISABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM inventory_history;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "ALTER TABLE inventory_history ENABLE TRIGGER all"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "UPDATE product_product SET quantity_sold = 0;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "UPDATE product_product SET amount = 0;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)


print "\nDone time:",datetime.datetime.today()
