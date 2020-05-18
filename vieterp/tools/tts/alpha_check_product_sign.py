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

dbname2 = 'alpha'
username2 = 'admin@thethaosi.vn'
pwd2 = 'AlphaAdmin2019'

sock_common2 = xmlrpclib.ServerProxy('http://alpha.konek.vn/xmlrpc/common')
sock2 = xmlrpclib.ServerProxy('http://alpha.konek.vn/xmlrpc/object')
uid2 = sock_common2.login(dbname2, username2, pwd2)

# product_ids = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'search', ['|',('active', '=', False),('active', '=', True)])
# for product_id in product_ids:
#     default_code = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'read', product_id, ['default_code','name'])[0]
#     name = default_code.get('name', False)
#     default_code = default_code.get('default_code',False)
#     if default_code:
#         alpha_product = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'search',
#                       [('default_code', '=', default_code),'|', ('active', '=', False), ('active', '=', True)])
#         if not alpha_product:
#             print "Product Template not found - %s" % (default_code)
#         else:
#             alpha_product = alpha_product[0]
#             sock2.execute(dbname2, uid2, pwd2, 'product.template', 'write', alpha_product, {
#                 'name': name,
#             })

# product_ids = sock1.execute(dbname1, uid1, pwd1, 'product.product', 'search', ['|',('active', '=', False),('active', '=', True)])
# for product_id in product_ids:
#     default_code = sock1.execute(dbname1, uid1, pwd1, 'product.product', 'read', product_id, ['default_code','active','name'])[0]
#     name = default_code.get('name', False)
#     active = default_code.get('active', False)
#     default_code = default_code.get('default_code',False)
#     if default_code:
#         alpha_product = sock2.execute(dbname2, uid2, pwd2, 'product.product', 'search',
#                       [('default_code', '=', default_code),'|', ('active', '=', False), ('active', '=', True)])
#         if not alpha_product:
#             print "Product Variant not found - %s" % (default_code)
#         else:
#             sock2.execute(dbname2, uid2, pwd2, 'product.product', 'write', alpha_product, {
#                 'active': active,
#                 'name' : name,
#             })


# product_ids = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'search', [('default_code', 'like', 'SPV'),'|', ('active', '=', False), ('active', '=', True)])
# for product_id in product_ids:
#     default_code = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'read', product_id, ['default_code'])[0]
#     default_code = default_code.get('default_code', False)
#     default_code = default_code.replace('SPV','SP')
#
#     sock2.execute(dbname2, uid2, pwd2, 'product.template', 'write', product_id, {
#         'purchase_code' : default_code,
#         'default_code' : default_code,
#     })

# count = 0
# default_code_list = ['SP002321','SP002322','SP002323','SP002353','SP002269','SP002265','SP002297','SP002273']
# product_ids = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'search', [('default_code', 'in', default_code_list),'|',('active', '=', False),('active', '=', True)])
# for product_id in product_ids:
#     count += 1
#     if count < 2:
#         attribute_line_ids = []
#         data_attribute_line_ids = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'read', product_id, ['attribute_line_ids'])[0]
#         data_attribute_line_ids = data_attribute_line_ids.get('attribute_line_ids', [])
#         for line in data_attribute_line_ids:
#             attribute_line_value = sock1.execute(dbname1, uid1, pwd1, 'product.attribute.line', 'read', line, ['value_ids','attribute_id'])[0]
#             value_ids = attribute_line_value.get('value_ids', False)
#             attribute_id = attribute_line_value.get('attribute_id', False)
#             if value_ids and attribute_id:
#                 attribute_line_ids.append((0,0,{
#                     'value_ids' : [(6, 0, value_ids)],
#                     'attribute_id' : attribute_id[0],
#                 }))
#         product_data = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'copy_data', [product_id])
#         product_data.update({
#             'attribute_line_ids' : attribute_line_ids,
#         })
#         new_product_id = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'create', product_data)
#     print count


#TODO update default code site 2
# count = 0
# # default_code_list = ['SP002213','SP000740']
# default_code_list = ['SP002164','SP000093','SP000637','SP000720']
# product_ids = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'search', [('purchase_code', 'in', default_code_list),'|',('active', '=', False),('active', '=', True)])
# for product_id in product_ids:
#     purchase_code = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'read', product_id, ['purchase_code'])[0]
#     purchase_code = purchase_code.get('purchase_code', False)
#     if purchase_code:
#         product_variant_erp_ids = sock1.execute(dbname1, uid1, pwd1, 'product.product', 'search', [('product_tmpl_id.default_code', '=', purchase_code),'|',('active', '=', False),('active', '=', True)])
#
#         if len(product_variant_erp_ids) == 1:
#             product_variant_inao_id = sock2.execute(dbname2, uid2, pwd2, 'product.product', 'search',
#                                                      [('product_tmpl_id', '=', product_id)])
#             if len(product_variant_inao_id) == 1:
#                 count += 1
#                 default_code = sock1.execute(dbname1, uid1, pwd1, 'product.product', 'read', product_variant_erp_ids[0], ['default_code','active'])[0]
#                 active = default_code.get('active', False)
#                 default_code = default_code.get('default_code', False)
#                 if default_code:
#                     sock2.execute(dbname2, uid2, pwd2, 'product.product', 'write', product_variant_inao_id, {
#                         'default_code' : default_code,
#                     })
#                 print count
#             else:
#                 print "error product ---------------------%s" % (product_id)
#         else:
#             for product_variant_erp_id in product_variant_erp_ids:
#                 product_variant_erp_data = sock1.execute(dbname1, uid1, pwd1, 'product.product', 'read', product_variant_erp_id,
#                                              ['default_code','attribute_value_ids','active'])[0]
#                 attribute_value_ids = product_variant_erp_data.get('attribute_value_ids', False)
#                 if attribute_value_ids:
#                     domain = [('product_tmpl_id', '=', product_id)]
#                     for attribute_value_id in attribute_value_ids:
#                         domain.append(('attribute_value_ids', 'in', attribute_value_id))
#                     product_variant_inao_id = sock2.execute(dbname2, uid2, pwd2, 'product.product', 'search', domain)
#                     if len(product_variant_inao_id) == 1:
#                         count += 1
#                         default_code = product_variant_erp_data.get('default_code', False)
#                         active = product_variant_erp_data.get('active', False)
#                         try:
#                             sock2.execute(dbname2, uid2, pwd2, 'product.product', 'write', product_variant_inao_id, {
#                                 'default_code': default_code,
#                             })
#                         except:
#                             pass
#                         print count
#                     else:
#                         print "error product ---------------------%s" % (product_id)

#TODO update default code site 2
# count = 0
# default_code_list = ['SP002213','SP000740']
# product_ids = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'search', [('purchase_code', 'in', default_code_list),'|',('active', '=', False),('active', '=', True)])
# for product_id in product_ids:
#     purchase_code = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'read', product_id, ['purchase_code'])[0]
#     purchase_code = purchase_code.get('purchase_code', False)
#     sock2.execute(dbname2, uid2, pwd2, 'product.template', 'write', product_id, {
#         'default_code': purchase_code,
#     })

print "\nDone time:",datetime.datetime.today()