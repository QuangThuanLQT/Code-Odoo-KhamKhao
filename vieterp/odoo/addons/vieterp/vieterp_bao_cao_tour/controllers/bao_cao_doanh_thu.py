# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class bao_cao_doanh_thu(http.Controller):
    @http.route('/print_sale_order_excel', type='http', auth='user')
    def report_sale_return(self, token, **post):
        sale_return_obj = request.env['sale.order']
        action = post.get('action', False)
        domain = post.get('domain', False) and json.loads(post.get('domain', False))
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', 'attachment; filename=' + 'Quotations overview' + '.xlsx;')
            ]
        )
        sale_return_obj.print_sale_order_excel(response, 'return')

        response.set_cookie('fileToken', token)
        return response