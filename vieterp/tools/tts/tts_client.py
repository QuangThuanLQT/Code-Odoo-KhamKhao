# -*- coding: utf-8 -*-
import json
import gearman

queue_server = 'vieterp-vn.local:4730'

gm_client = gearman.GearmanClient([queue_server])

values = json.dumps({
    'sale_id': 9483
})
gm_client.submit_job('tts_sale_order_read', values, priority=gearman.PRIORITY_HIGH, background=True)