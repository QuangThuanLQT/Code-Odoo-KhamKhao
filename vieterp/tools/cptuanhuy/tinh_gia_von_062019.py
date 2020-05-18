#!/usr/bin/env python
# coding: utf-8
import xmlrpclib
import xlrd
import datetime
print "\nSTART time:", datetime.datetime.today()

# url = 'http://tuanhuy.konek.vn'
# dbname = 'tuanhuy'
url = 'http://localhost:8069'
dbname = 'tuan_huy'
username = 'admin'
pwd = 'admin'

sock_common = xmlrpclib.ServerProxy('%s/xmlrpc/common' %(url,))
sock = xmlrpclib.ServerProxy('%s/xmlrpc/object' %(url,))
uid = sock_common.login(dbname, username, pwd)

start_date = '2019-12-01 00:00:00'
# end_date = False
end_date = '2019-12-31 23:59:59'

# TODO: Optimize the performance by using sql query
# Step-1: Disable cron picking
query = "UPDATE ir_cron SET active=false WHERE name = '%s'" % ('Cron Create Picking From Sale',)
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "UPDATE ir_cron SET active=false WHERE name = '%s'" % ('Update Picking To Confirm',)
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "UPDATE ir_cron SET active=false WHERE name = '%s'" % ('Save Picking History',)
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# Step0: Get old data
print "Step0: Prepare data"
po_picking_dones = []
query = "SELECT origin FROM stock_picking WHERE state='%s' AND min_date >= '%s' AND origin LIKE '%s' ORDER BY min_date asc" %('done', start_date, 'PO%')
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        po_picking_dones.append(query_line[0])
print "po_picking_dones = %s - %s" % (po_picking_dones, len(po_picking_dones))

po_picking_assigned = []
query = "SELECT origin FROM stock_picking WHERE state IN ('assigned', 'partially_available') AND min_date >= '%s' AND origin LIKE '%s' ORDER BY min_date asc" %(start_date, 'PO%')
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        po_picking_assigned.append(query_line[0])
print "po_picking_assigned = %s - %s" % (po_picking_assigned, len(po_picking_assigned))

return_has_so = []
query = "SELECT DISTINCT so.name, so.date_order FROM sale_order_return_rel sr INNER JOIN sale_order so ON so.id = sr.order_id WHERE so.state = 'sale' AND so.date_order >= '%s' AND so.sale_order_return = true ORDER BY so.date_order asc" %(start_date,)
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        return_has_so.append(query_line[0])
print "return_has_so = %s - %s" % (return_has_so, len(return_has_so))

return_no_so = []
query = "SELECT DISTINCT so.name, so.date_order FROM sale_order so WHERE so.state = 'sale' AND so.sale_order_return = true AND so.name NOT IN ('%s') AND so.date_order >= '%s' ORDER BY so.date_order asc" %("','".join(return_has_so), start_date)
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        return_no_so.append(query_line[0])
print "return_no_so = %s - %s" % (return_no_so, len(return_no_so))

return_no_so_done = []
query = "SELECT origin FROM stock_picking WHERE state = 'done' AND origin IN ('%s') AND min_date >= '%s' ORDER BY min_date asc" %("','".join(return_no_so), start_date)
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        return_no_so_done.append(query_line[0])
print "return_no_so_done = %s - %s" % (return_no_so_done, len(return_no_so_done))

so_has_return = []
query = "SELECT DISTINCT so.name, so.date_order FROM sale_order_return_rel sr INNER JOIN sale_order so ON so.id = sr.sale_order_return_relation WHERE so.state = 'sale' AND so.date_order >= '%s' AND so.sale_order_return = false ORDER BY so.date_order asc" %(start_date)
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        so_has_return.append(query_line[0])
print "so_has_return = %s - %s" % (so_has_return, len(so_has_return))

so_has_return_done = []
query = "SELECT origin FROM stock_picking WHERE state = 'done' AND min_date >= '%s' AND origin IN ('%s') ORDER BY min_date asc" %(start_date, "','".join(so_has_return),)
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        so_has_return_done.append(query_line[0])
print "so_has_return_done = %s - %s" % (so_has_return_done, len(so_has_return_done))

return_has_so_done = []
query = "SELECT origin FROM stock_picking WHERE state = 'done' AND min_date >= '%s' AND origin IN ('%s') ORDER BY min_date asc" %(start_date, "','".join(return_has_so),)
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        return_has_so_done.append(query_line[0])
print "return_has_so_done = %s - %s" % (return_has_so_done, len(return_has_so_done))

rtp_picking_dones = []
query = "SELECT origin FROM stock_picking WHERE state = 'done' AND min_date >= '%s' AND origin LIKE '%s' ORDER BY min_date asc" %(start_date, 'RTP%')
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        rtp_picking_dones.append(query_line[0])
print "rtp_picking_dones = %s - %s" % (rtp_picking_dones, len(rtp_picking_dones))
#
rtp_picking_assigned = []
query = "SELECT origin FROM stock_picking WHERE state IN ('assigned', 'partially_available') AND min_date >= '%s' AND origin LIKE '%s' ORDER BY min_date asc" %(start_date, 'RTP%')
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        rtp_picking_assigned.append(query_line[0])
print "rtp_picking_assigned = %s - %s" % (rtp_picking_assigned, len(rtp_picking_assigned))

so_picking_dones = []
query = "SELECT origin FROM stock_picking WHERE state = 'done' AND min_date >= '%s' AND origin LIKE '%s' ORDER BY min_date asc" %(start_date, 'SO%')
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        so_picking_dones.append(query_line[0])
print "so_picking_dones = %s - %s" % (so_picking_dones, len(so_picking_dones))

so_picking_assigned = []
query = "SELECT origin FROM stock_picking WHERE state IN ('assigned', 'partially_available') AND min_date >= '%s' AND origin LIKE '%s' ORDER BY min_date asc" %(start_date, 'SO%')
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        so_picking_assigned.append(query_line[0])
print "so_picking_assigned = %s - %s" % (so_picking_assigned, len(so_picking_assigned))

so_picking_confirmed = []
query = "SELECT origin FROM stock_picking WHERE state = 'confirmed' AND min_date >= '%s' AND origin LIKE '%s' ORDER BY min_date asc" %(start_date, 'SO%')
print 'query - %s' %(query,)
query_result = sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query, True)
if query_result and len(query_result) > 0:
    for query_line in query_result:
        so_picking_confirmed.append(query_line[0])
print "so_picking_confirmed = %s - %s" % (so_picking_confirmed, len(so_picking_confirmed))

# Step 1: Reset assigned, partial available SO
print "Step 1: Reset returned has SO"
if return_has_so_done and len(return_has_so_done) > 0:
    picking_ids = sock.execute(dbname, uid, pwd, 'stock.picking', 'search', [
        ('origin', 'in', return_has_so_done),
    ], 0, 0, 'min_date desc')
    for picking_id in picking_ids:
        # picking = sock.execute(dbname, uid, pwd, 'stock.picking', 'read', [picking_id])[0]
        print "Reset picking: %s" % (picking_id)

        # confirm & validate the picking
        try:
            # confirm & validate the picking
            sock.execute(dbname, uid, pwd, 'stock.picking', 'do_reset_stock_picking', [picking_id])
        except Exception, e:
            # print e
            print "ERROR --------------- Reset picking: %s" % (picking_id)
            continue
        # sock.execute(dbname, uid, pwd, 'stock.picking', 'do_reset_stock_picking', [picking_id])

# Step 2: Reset confirmed SO
print "Step 2: Reset confirmed SO"
if so_picking_dones and len(so_picking_dones) > 0:
    picking_ids = sock.execute(dbname, uid, pwd, 'stock.picking', 'search', [
        ('origin', 'in', so_picking_dones),
    ], 0, 0, 'min_date desc')
    for picking_id in picking_ids:
        # picking = sock.execute(dbname, uid, pwd, 'stock.picking', 'read', [picking_id])[0]
        print "Reset picking: %s" %(picking_id)

        # confirm & validate the picking
        try:
            # confirm & validate the picking
            sock.execute(dbname, uid, pwd, 'stock.picking', 'do_reset_stock_picking', [picking_id])
        except Exception, e:
            # print e
            print "ERROR --------------- Reset picking: %s" % (picking_id)
            continue
        # sock.execute(dbname, uid, pwd, 'stock.picking', 'do_reset_stock_picking', [picking_id])

# Step 3: Reset assigned, partial available SO
print "Step 3: Reset assigned SO"
if so_picking_assigned and len(so_picking_assigned) > 0:
    picking_ids = sock.execute(dbname, uid, pwd, 'stock.picking', 'search', [
        ('origin', 'in', so_picking_assigned),
    ], 0, 0, 'min_date desc')
    for picking_id in picking_ids:
        # picking = sock.execute(dbname, uid, pwd, 'stock.picking', 'read', [picking_id])[0]
        print "Reset picking: %s" % (picking_id)

        try:
            # confirm & validate the picking
            sock.execute(dbname, uid, pwd, 'stock.picking', 'do_reset_stock_picking', [picking_id])
        except Exception, e:
            # print e
            print "ERROR --------------- Reset picking: %s" % (picking_id)
            continue

# Step 4: SO has return done
print "Step 4: SO has return done"
if so_has_return_done and len(so_has_return_done) > 0:
    picking_ids = sock.execute(dbname, uid, pwd, 'stock.picking', 'search', [
        ('origin', 'in', so_has_return_done),
    ], 0, 0, 'min_date asc')
    for picking_id in picking_ids:
        # picking = sock.execute(dbname, uid, pwd, 'stock.picking', 'read', [picking_id])[0]
        print "Reset picking: %s" %(picking_id)

        query = "UPDATE stock_move SET state='draft' WHERE picking_id = %s" %(picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        query = "UPDATE stock_picking SET state='draft' WHERE id = %s" % (picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        try:
            # Confirm the picking
            sock.execute(dbname, uid, pwd, 'stock.picking', 'action_confirm', [picking_id])
            sock.execute(dbname, uid, pwd, 'stock.picking', 'do_new_transfer', [picking_id])
        except Exception, e:
            # print e
            print "ERROR --------------- Reset picking: %s" % (picking_id)
            continue

# Step 5: return has so done
print "Step5: return has so done"
if return_has_so_done and len(return_has_so_done) > 0:
    picking_ids = sock.execute(dbname, uid, pwd, 'stock.picking', 'search', [
        ('origin', 'in', return_has_so_done),
    ], 0, 0, 'min_date asc')
    for picking_id in picking_ids:
        # picking = sock.execute(dbname, uid, pwd, 'stock.picking', 'read', [picking_id])[0]
        print "Reset picking: %s" %(picking_id)

        query = "UPDATE stock_move SET state='draft' WHERE picking_id = %s" %(picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        query = "UPDATE stock_picking SET state='draft' WHERE id = %s" % (picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        try:
            # Confirm the picking
            sock.execute(dbname, uid, pwd, 'stock.picking', 'action_confirm', [picking_id])
            sock.execute(dbname, uid, pwd, 'stock.picking', 'action_assign', [picking_id], {'sale_order_return': True})
            sock.execute(dbname, uid, pwd, 'stock.picking', 'do_new_transfer', [picking_id])
        except Exception, e:
            # print e
            print "ERROR --------------- Reset picking: %s" % (picking_id)
            continue

# Step6: Purchase return assigned
print "Step6: Purchase return assigned"
if rtp_picking_assigned and len(rtp_picking_assigned) > 0:
    picking_ids = sock.execute(dbname, uid, pwd, 'stock.picking', 'search', [
        ('origin', 'in', rtp_picking_assigned),
    ], 0, 0, 'min_date asc')
    for picking_id in picking_ids:
        # picking = sock.execute(dbname, uid, pwd, 'stock.picking', 'read', [picking_id])[0]
        print "Reset picking: %s" % (picking_id)

        query = "UPDATE stock_move SET state='draft' WHERE picking_id = %s" % (picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        query = "UPDATE stock_picking SET state='draft' WHERE id = %s" % (picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        try:
            # Confirm the picking
            sock.execute(dbname, uid, pwd, 'stock.picking', 'action_confirm', [picking_id])
        except Exception, e:
            # print e
            print "ERROR --------------- Reset picking: %s" % (picking_id)
            continue

# Step7: So picking done
print "Step7: So picking done"
if so_picking_dones and len(so_picking_dones) > 0:
    arguments = [
        ('origin', 'in', so_picking_dones),
    ]
    if so_has_return_done and len(so_has_return_done) > 0:
        arguments.append(('origin', 'not in', so_has_return_done))
    picking_ids = sock.execute(dbname, uid, pwd, 'stock.picking', 'search', arguments, 0, 0, 'min_date asc')
    for picking_id in picking_ids:
        # picking = sock.execute(dbname, uid, pwd, 'stock.picking', 'read', [picking_id])[0]
        print "Reset picking: %s" % (picking_id)

        query = "UPDATE stock_move SET state='draft' WHERE picking_id = %s" % (picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        query = "UPDATE stock_picking SET state='draft' WHERE id = %s" % (picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        try:
            # Confirm the picking
            sock.execute(dbname, uid, pwd, 'stock.picking', 'action_confirm', [picking_id])
            sock.execute(dbname, uid, pwd, 'stock.picking', 'do_new_transfer', [picking_id])
        except Exception, e:
            # print e
            print "ERROR --------------- Reset picking: %s" % (picking_id)
            continue

# Step8: So picking assign
print "Step8: So picking assign"
if so_picking_assigned and len(so_picking_assigned) > 0:
    picking_ids = sock.execute(dbname, uid, pwd, 'stock.picking', 'search', [
        ('origin', 'in', so_picking_assigned),
    ], 0, 0, 'min_date asc')
    for picking_id in picking_ids:
        # picking = sock.execute(dbname, uid, pwd, 'stock.picking', 'read', [picking_id])[0]
        print "Reset picking: %s" % (picking_id)

        query = "UPDATE stock_move SET state='draft' WHERE picking_id = %s" % (picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        query = "UPDATE stock_picking SET state='draft' WHERE id = %s" % (picking_id,)
        sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

        try:
            # Confirm the picking
            sock.execute(dbname, uid, pwd, 'stock.picking', 'action_confirm', [picking_id])
        except Exception, e:
            # print e
            print "ERROR --------------- Reset picking: %s" % (picking_id)
            continue

query = "UPDATE account_move SET date = stock_picking.min_date FROM stock_picking WHERE stock_picking.name = account_move.ref AND account_move.ref IS NOT NULL AND account_move.ref LIKE 'WH/OUT/%'"
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "UPDATE account_move_line SET date = account_move.date FROM account_move WHERE account_move.id = account_move_line.move_id AND account_move.ref IS NOT NULL AND account_move.ref LIKE 'WH/OUT/%'"
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "UPDATE account_move SET date = stock_picking.min_date FROM stock_picking WHERE stock_picking.name = account_move.ref AND account_move.ref IS NOT NULL AND account_move.ref LIKE 'WH/IN/%'"
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "UPDATE account_move_line SET date = account_move.date FROM account_move WHERE account_move.id = account_move_line.move_id AND account_move.ref IS NOT NULL AND account_move.ref LIKE 'WH/IN/%'"
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# Step-1: Enable cron picking
print "Step-1: Enable cron picking"
query = "UPDATE ir_cron SET active=true WHERE name = '%s'" % ('Cron Create Picking From Sale',)
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "UPDATE ir_cron SET active=true WHERE name = '%s'" % ('Update Picking To Confirm',)
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

query = "UPDATE ir_cron SET active=true WHERE name = '%s'" % ('Save Picking History',)
sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query)

# Final Step Set Done for Sale,Purchase
if start_date and end_date:
    query_update_so = "UPDATE sale_order SET state = 'done' where state = 'sale' and date_order >= '%s' and date_order <= '%s'" %(start_date,end_date)
    sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query_update_so)

    query_update_po = "UPDATE purchase_order SET state = 'done' where state = 'purchase' and date_order >= '%s' and date_order <= '%s'" %(start_date,end_date)
    sock.execute(dbname, uid, pwd, 'tuanhuy.base', 'execute_query', query_update_po)
print "\nEND time:", datetime.datetime.today()
