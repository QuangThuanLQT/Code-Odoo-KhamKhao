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

# dbname2 = 'danang'
username2 = 'thethaosi'
pwd2 = 'TTS2019'

sock_common2 = xmlrpclib.ServerProxy('http://danang.konek.vn/xmlrpc/common')
sock2 = xmlrpclib.ServerProxy('http://danang.konek.vn/xmlrpc/object')
uid2 = sock_common2.login(dbname2, username2, pwd2)

count = 0
# product_ids = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'search', ['|',('active', '=', False),('active', '=', True)])
# for product_id in product_ids:
#     count += 1
#     if count > 0:
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
#             'categ_id' : 637,
#             'public_categ_ids': [[6, 0, [2256]]],
#             'uom_po_id' : 29,
#             'uom_id' : 29,
#             'attribute_line_ids' : attribute_line_ids,
#         })
#         del product_data['alternative_product_ids']
#         new_product_id = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'create', product_data)
#     print count

# product_ids = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'search', [('purchase_code', 'like', 'SPV')])
# for product_id in product_ids:
#     purchase_code = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'read', product_id, ['purchase_code'])[0]
#     purchase_code = purchase_code.get('purchase_code', False)
#     purchase_code = purchase_code.replace('SPV','SP')
#
    # sock2.execute(dbname2, uid2, pwd2, 'product.template', 'write', product_id, {
    #     'purchase_code' : purchase_code
    # })

# product_ids = [62641,62643]
# default_code_list = ['SPV001885','SPV001888']
# for count in range(0,len(product_ids)):
#     product_id = product_ids[count]
#     default_code = default_code_list[count]
#     sock2.execute(dbname2, uid2, pwd2, 'product.product', 'write', [product_id], {
#                                 'default_code': default_code,
#                             })

# TODO update default code site 2
# product_ids = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'search', [])
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


# product_ids = sock1.execute(dbname1, uid1, pwd1, 'product.product', 'search', [('active', '=', False)])
# for product_id in product_ids:
#     product_data = sock1.execute(dbname1, uid1, pwd1, 'product.product', 'read', product_id, ['default_code'])[0]
#     default_code = product_data.get('default_code',False)
#     product_dn_id = sock2.execute(dbname2, uid2, pwd2, 'product.product', 'search', [('default_code', '=', default_code)])
#     if product_dn_id:
#         sock2.execute(dbname2, uid2, pwd2, 'product.product', 'write', product_dn_id, {
#             'active': False,
#         })

# product_ids = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'search', [('active', '=', False)])
# for product_id in product_ids:
#     product_data = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'read', product_id, ['default_code'])[0]
#     default_code = product_data.get('default_code',False)
#     product_dn_id = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'search', [('default_code', '=', default_code)])
#     if product_dn_id:
#         sock2.execute(dbname2, uid2, pwd2, 'product.template', 'write', product_dn_id, {
#             'active': False,
#         })


product_ids = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'search', ['|',('active', '=', False),('active', '=', True)])
for product_id in product_ids:
    count += 1
    product_data = sock1.execute(dbname1, uid1, pwd1, 'product.template', 'read', product_id, ['categ_id','default_code'])[0]
    categ_id = product_data.get('categ_id',False)
    if categ_id:
        categ_id = categ_id[0]
        categ_data = sock1.execute(dbname1, uid1, pwd1, 'product.category', 'read', categ_id, ['display_name'])[0]
        categ_name = categ_data.get('display_name', False)
        categ_list = categ_name.split('/')
        categ_curr_id = False
        for categ in categ_list:
            categ = categ.strip()
            if categ_curr_id:
                categ_search_id = sock2.execute(dbname2, uid2, pwd2, 'product.category', 'search', [('name', '=', categ),('parent_id', '=', categ_curr_id)])
                if categ_search_id:
                    categ_curr_id = categ_search_id[0]
                else:
                    categ_curr_id = sock2.execute(dbname2, uid2, pwd2, 'product.category', 'create', {
                        'name': categ,
                        'parent_id' : categ_curr_id,
                        'property_cost_method' : 'average',
                        'property_valuation' : 'real_time',
                        'property_account_income_categ_id' : 140,
                        'property_account_expense_categ_id' : 29,
                        'property_stock_account_input_categ_id' : 93,
                        'property_stock_account_output_categ_id' : 167,
                        'property_stock_valuation_account_id' : 29,
                        'property_stock_journal' : 7,
                    })

            else:
                categ_curr_id = sock2.execute(dbname2, uid2, pwd2, 'product.category', 'search',[('name', '=', categ)])
                if categ_curr_id:
                    categ_curr_id = categ_curr_id[0]
                else:
                    categ_curr_id = sock2.execute(dbname2, uid2, pwd2, 'product.category', 'create', {
                        'name' : categ,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time',
                        'property_account_income_categ_id': 140,
                        'property_account_expense_categ_id': 29,
                        'property_stock_account_input_categ_id': 93,
                        'property_stock_account_output_categ_id': 167,
                        'property_stock_valuation_account_id': 29,
                        'property_stock_journal': 7,
                    })
        default_code = product_data.get('default_code', False)
        product_dn_id = sock2.execute(dbname2, uid2, pwd2, 'product.template', 'search',[('default_code', '=', default_code),'|',('active', '=', False),('active', '=', True)])
        if product_dn_id:
            sock2.execute(dbname2, uid2, pwd2, 'product.template', 'write', product_dn_id, {
                'categ_id': categ_curr_id,
            })
        else:
            print "error product ---------------------%s" % (product_id)
    print count


print "\nDone time:",datetime.datetime.today()



