#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nstart time:",datetime.datetime.today()

dbname1 = 'erp'
username1 = 'admin@thethaosi.vn'
pwd1 = 'AlphaAdmin2019'

sock_common1 = xmlrpclib.ServerProxy('http://erp.thethaosi.vn/xmlrpc/common')
sock1 = xmlrpclib.ServerProxy('http://erp.thethaosi.vn/xmlrpc/object')
uid1 = sock_common1.login(dbname1, username1, pwd1)

dbname2 = 'danang'
username2 = 'thethaosi'
pwd2 = 'TTS2019'

sock_common2 = xmlrpclib.ServerProxy('http://danang.konek.vn/xmlrpc/common')
sock2 = xmlrpclib.ServerProxy('http://danang.konek.vn/xmlrpc/object')
uid2 = sock_common2.login(dbname2, username2, pwd2)

supplierinfo_ids = sock1.execute(dbname1, uid1, pwd1, 'product.supplierinfo', 'search', [])
count = 0
for supplierinfo_id in supplierinfo_ids:
    count += 1
    supplierinfo_line_ids = sock1.execute(dbname1, uid1, pwd1, 'product.variants.line', 'search', [('line_id', '=', supplierinfo_id)])
    line_data = []
    for supplierinfo_line_id in supplierinfo_line_ids:
        supplierinfo_line_data = sock1.execute(dbname1, uid1, pwd1, 'product.variants.line', 'read', supplierinfo_line_id, ['product_id'])[0]
        product_erp_id = supplierinfo_line_data.get('product_id', False)[0]
        product_data = sock1.execute(dbname1, uid1, pwd1, 'product.product', 'read', product_erp_id, ['default_code'])[0]
        default_code = product_data.get('default_code',False)
        product_id = sock2.execute(dbname2, uid2, pwd2, 'product.product', 'search', [('default_code', '=', default_code),'|',('active', '=', False),('active', '=', True)])
        if product_id:
            line_data.append((0,0,{
                'product_id' : product_id[0],
            }))
        else:
            print "-------------------------- Product variant %s not found" % (default_code)
    supplierinfo_data = sock1.execute(dbname1, uid1, pwd1, 'product.supplierinfo', 'read', supplierinfo_id, ['product_tmpl_id','delay','min_qty'])[0]
    delay = supplierinfo_data.get('delay',False)
    min_qty = supplierinfo_data.get('min_qty', False)
    new_supplierinfo_data = {
        'product_variants_line': line_data,
        'name': 10108,
        'delay': delay,
        'min_qty': min_qty,
    }

    product_tmpl_erp_id = supplierinfo_data.get('product_tmpl_id', False)
    if product_tmpl_erp_id:
        product_tmp_data = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'read', product_tmpl_erp_id[0], ['default_code'])[0]
        tmpl_default_code = product_tmp_data.get('default_code')
        product_tmpl_id = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'search',
                                        [('default_code', '=', tmpl_default_code), '|', ('active', '=', False),
                                         ('active', '=', True)])
        if product_tmpl_id:
            new_supplierinfo_data.update({
                'product_tmpl_id': product_tmpl_id[0],
            })
        else:
            print "-------------------------- Product template %s not found" % (tmpl_default_code)
    sock2.execute(dbname2, uid2, pwd2, 'product.supplierinfo', 'create', new_supplierinfo_data)
    print count
