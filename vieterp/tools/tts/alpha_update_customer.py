#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nstart time:",datetime.datetime.today()

dbname1 = 'alpha'
username1 = 'admin@thethaosi.vn'
pwd1 = 'AlphaAdmin2019'

sock_common1 = xmlrpclib.ServerProxy('http://alpha.beta2.konek.vn/xmlrpc/common')
sock1 = xmlrpclib.ServerProxy('http://alpha.beta2.konek.vn/xmlrpc/object')
uid1 = sock_common1.login(dbname1, username1, pwd1)

dbname2 = 'alpha'
username2 = 'admin@thethaosi.vn'
pwd2 = 'AlphaAdmin2019'

sock_common2 = xmlrpclib.ServerProxy('http://alpha.konek.vn/xmlrpc/common')
sock2 = xmlrpclib.ServerProxy('http://alpha.konek.vn/xmlrpc/object')
uid2 = sock_common2.login(dbname2, username2, pwd2)

# customer_ids = sock1.execute(dbname1, uid1, pwd1, 'res.partner', 'search', [('customer', '=', True)])
# count = 0
# for customer_id in customer_ids:
#     count += 1
#     customer_data = sock1.execute(dbname1, uid1, pwd1, 'res.partner', 'read', customer_id, ['ref','user_id','name'])[0]
#     ref = customer_data.get('ref', False)
#     name = customer_data.get('name', False)
#     user_id = customer_data.get('user_id', False)
#     customer_alpha_id = sock2.execute(dbname2, uid2, pwd2, 'res.partner', 'search', [('name', '=', name),('ref', '=', ref)])
#     if not customer_alpha_id:
#         print "not found customer - %s" % (ref)
    # if customer_alpha_id and user_id:
    #     user_id = user_id[0]
    #     user_data = sock1.execute(dbname1, uid1, pwd1, 'res.users', 'read', user_id, ['login'])[0]
    #     login = user_data.get('login', False)
    #     user_alpha_id = sock2.execute(dbname2, uid2, pwd2, 'res.users', 'search', [('login', '=', login)])
    #     if user_alpha_id:
    #         user_alpha_id = user_alpha_id[0]
    #     else:
    #         print "not found user - %s" % (login)
    # else:
    #     print "not found customer - %s" % (login)

    # print count

account_ids = sock2.execute(dbname2, uid2, pwd2, 'account.account', 'search', [])
account_need_remove = []
count = 0
for account_id in account_ids:
    count += 1
    account_data = sock2.execute(dbname2, uid2, pwd2, 'account.account', 'read', account_id,['code'])[0]
    code = account_data.get('code', False)
    account_beta2_id = sock1.execute(dbname1, uid1, pwd1, 'account.account', 'search', [('code', '=', code)])
    if not account_beta2_id:
        account_need_remove.append(account_id)
    print count
sock2.execute(dbname2, uid2, pwd2, 'account.account', 'unlink', account_need_remove)


# for account_id in account_ids:
#     count += 1
#     account_data = sock1.execute(dbname1, uid1, pwd1, 'account.account', 'read', account_id, ['code','group_level_1','group_level_2','group_level_3'])[0]
#     # name = account_data.get('name', False)
#     code = account_data.get('code', False)
#     # user_type_id = account_data.get('user_type_id', False)
#     # domain = [('name', '=', name), ('code', '=', code)]
#     # if user_type_id:
#     #     domain.append(('user_type_id', '=',user_type_id[0]))
#     domain = [('code', '=', code)]
#     account_live_id = sock2.execute(dbname2, uid2, pwd2, 'account.account', 'search',domain)
#     if account_live_id:
#         group_level_1 = account_data.get('group_level_1', False)
#         group_level_2 = account_data.get('group_level_2', False)
#         group_level_3 = account_data.get('group_level_3', False)
#         if group_level_1:
#             domain.append(
#                 ('group_level_1.name', '=', group_level_1[1])
#             )
#         else:
#             domain.append(
#                 ('group_level_1', '=', False)
#             )
#
#         if group_level_2:
#             domain.append(
#                 ('group_level_2.name', '=', group_level_2[1])
#             )
#         else:
#             domain.append(
#                 ('group_level_2', '=', False)
#             )
#
#         if group_level_3:
#             domain.append(
#                 ('group_level_3.name', '=', group_level_3[1])
#             )
#         else:
#             domain.append(
#                 ('group_level_3', '=', False)
#             )
#         check_account_live_id = sock2.execute(dbname2, uid2, pwd2, 'account.account', 'search', domain)
#         if not check_account_live_id:
#             print "account diff group level - %s" % (code)
#
#     if not account_live_id:
#         print "account not found - %s" % (code)
        # account_data_copy = sock1.execute(dbname1, uid1, pwd1, 'account.account', 'copy_data', [account_id])
        # group_level_1 = account_data.get('group_level_1', False)
        # group_level_2 = account_data.get('group_level_2', False)
        # group_level_3 = account_data.get('group_level_3', False)
        #
        # if group_level_1:
        #     group_level_1 = group_level_1[0]
        #     group_level_1_data = sock1.execute(dbname1, uid1, pwd1, 'journal.entry.category', 'read', group_level_1,['name'])[0]
        #     group_level_1_name = group_level_1_data.get('name', False)
        #     group_level_1_live_id = sock2.execute(dbname2, uid2, pwd2, 'journal.entry.category', 'search', [('level','=','level_1'),('name', '=', group_level_1_name)])
        #     if group_level_1_live_id:
        #         group_level_1_live_id = group_level_1_live_id[0]
        #     else:
        #         print "create group level_1 - %s" % (group_level_1_name)
        #         group_level_1_live_id = sock2.execute(dbname2, uid2, pwd2, 'journal.entry.category', 'create', {
        #             'level' : 'level_1',
        #             'name' : group_level_1_name,
        #         })
        #
        #     account_data_copy.update({
        #         'group_level_1' : group_level_1_live_id,
        #     })
        # if group_level_2:
        #     group_level_2 = group_level_2[0]
        #     group_level_2_data = sock1.execute(dbname1, uid1, pwd1, 'journal.entry.category', 'read', group_level_2,['name'])[0]
        #     group_level_2_name = group_level_2_data.get('name', False)
        #     group_level_2_live_id = sock2.execute(dbname2, uid2, pwd2, 'journal.entry.category', 'search', [('level','=','level_2'),('name', '=', group_level_2_name)])
        #     if group_level_2_live_id:
        #         group_level_2_live_id = group_level_2_live_id[0]
        #     else:
        #         print "create group level_2 - %s" % (group_level_2_name)
        #         group_level_2_live_id = sock2.execute(dbname2, uid2, pwd2, 'journal.entry.category', 'create', {
        #             'level' : 'level_2',
        #             'name' : group_level_2_name,
        #         })
        #
        #     account_data_copy.update({
        #         'group_level_2' : group_level_2_live_id,
        #     })
        # if group_level_3:
        #     group_level_3 = group_level_3[0]
        #     group_level_3_data = sock1.execute(dbname1, uid1, pwd1, 'journal.entry.category', 'read', group_level_3,['name'])[0]
        #     group_level_3_name = group_level_3_data.get('name', False)
        #     group_level_3_live_id = sock2.execute(dbname2, uid2, pwd2, 'journal.entry.category', 'search', [('level','=','level_3'),('name', '=', group_level_3_name)])
        #     if group_level_3_live_id:
        #         group_level_3_live_id = group_level_3_live_id[0]
        #     else:
        #         print "create group level_3 - %s" % (group_level_3_name)
        #         group_level_3_live_id = sock2.execute(dbname2, uid2, pwd2, 'journal.entry.category', 'create', {
        #             'level' : 'level_3',
        #             'name' : group_level_3_name,
        #         })
        #
        #     account_data_copy.update({
        #         'group_level_3' : group_level_3_live_id,
        #     })
        # sock2.execute(dbname2, uid2, pwd2, 'account.account', 'create', account_data_copy)
    # print count

