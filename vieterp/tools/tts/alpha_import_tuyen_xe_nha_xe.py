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

transporter_ids = sock1.execute(dbname1, uid1, pwd1, 'tts.transporter', 'search', [])
for transporter_id in transporter_ids:
    copy_data = sock1.execute(dbname1, uid1, pwd1, 'tts.transporter', 'copy_data', [transporter_id])
    alpha_transporter_id = sock2.execute(dbname2, uid2, pwd2, 'tts.transporter', 'search',[('id', '=', transporter_id)])
    if alpha_transporter_id:
        pass
        # sock2.execute(dbname2, uid2, pwd2, 'tts.transporter', 'write', alpha_transporter_id, copy_data)
    else:
        sock2.execute(dbname2, uid2, pwd2, 'tts.transporter', 'create', copy_data)


