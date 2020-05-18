# coding: utf-8
import xmlrpclib
import gearman
import json
import datetime
import logging

LOG_FILENAME = '/var/log/odoo/worker-invoice.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logger = logging.getLogger('picking')
logger.debug("Sync Data start time: %s" %(datetime.datetime.today(),))

url = 'localhost:8069'
db = 'inao'
username = 'thethaosi'
pwd = 'TTS2019'

url_obj = 'http://%s/xmlrpc/object' % (url)
url_common = 'http://%s/xmlrpc/common' % (url)
sock_common = xmlrpclib.ServerProxy(url_common)
sock = xmlrpclib.ServerProxy(url_obj)

uid = sock_common.login(db, username, pwd)
logger.debug("UID: - %s" %(uid,))
queue_server_ids = sock.execute(db, uid, pwd, 'setting.queue.server', 'search', [('active', '=', True)])
if len(queue_server_ids) > 0:
    try:
        queue_server = sock.execute(db, uid, pwd, 'setting.queue.server', 'read', [queue_server_ids[0]], ['queue_server', 'prefix'])[0]

        def sale_order_create_invoice(worker, data):
            if data:
                values = json.loads(data.data)
                logger.debug("sale_order_create_invoice - %s" % (data.data))
                sale_id = values.get('sale_id', False)
                active_id = values.get('active_id', False)
                active_ids = values.get('active_ids', [])
                if sale_id:
                    try:
                        sock_client = xmlrpclib.ServerProxy(url_obj)
                        sock_client.execute(db, uid, pwd, 'sale.order', 'directly_create_inv', [sale_id], {'no_qty_invoiced': True})
                        logger.debug("Invoiced - %s" %(sale_id,))
                        sock_client.execute(db, uid, pwd, 'sale.order', 'update_line_qty_invoiced', [sale_id])
                        logger.debug("Done - %s" % (sale_id,))
                    except Exception, e:
                        logger.debug("Error - %s" %(str(e),))
                        return 'ko'
            return 'ok'

        def check_connect(worker, data):
            return 'ok'

        gm_worker = gearman.GearmanWorker([queue_server.get('queue_server')])
        gm_worker.set_client_id('%s-worker-invoice' %(queue_server.get('prefix'),))
        gm_worker.register_task('%s_picking_create_so_invoice' %(queue_server.get('prefix'),), sale_order_create_invoice)
        gm_worker.register_task('%s_check_connect' %(queue_server.get('prefix'),), check_connect)
        gm_worker.work()
    except Exception, e:
        print e
        pass
