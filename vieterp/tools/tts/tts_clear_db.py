#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nSTART time:", datetime.datetime.today()

url = 'http://localhost:8069'
dbname = 'tts_danang'
username = 'thethaosi'
pwd = 'TTS2019'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

query = "DELETE FROM sale_order_line;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM sale_order;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM stock_move;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM stock_pack_operation;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM stock_picking;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM purchase_order_line;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM purchase_order;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM account_invoice_line;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM account_invoice;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# query = "DELETE FROM account_move_line;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM account_partial_reconcile;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM account_reconcile;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM account_move_line;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM account_move;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM account_voucher_line;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM account_voucher;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM res_partner WHERE id NOT IN (SELECT partner_id FROM res_users) AND id NOT IN (SELECT partner_id FROM res_company);"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# query = "DELETE FROM brand_name;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM procurement_order;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM stock_inventory_line;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM stock_inventory;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM stock_quant;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM product_barcode_generator_line;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM product_barcode;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM stock_landed_cost_lines;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM stock_scrap;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM stock_production_lot;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM config_product_print;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM product_print;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM product_template;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM product_product;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM account_payment_unc;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "DELETE FROM account_payment_gbn;"
print query
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# query = "DELETE FROM tts_delivery_scope;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM tts_transporter_route;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM tts_transporter;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# query = "DELETE FROM feosco_ward;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM feosco_district;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)
#
# query = "DELETE FROM feosco_city;"
# print query
# sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

print 'Done'