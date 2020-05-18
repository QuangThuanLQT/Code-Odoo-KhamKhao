# -*- coding: utf-8 -*-
from odoo import http

# class VieterpAccountVoucher(http.Controller):
#     @http.route('/vieterp_account_voucher/vieterp_account_voucher/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vieterp_account_voucher/vieterp_account_voucher/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vieterp_account_voucher.listing', {
#             'root': '/vieterp_account_voucher/vieterp_account_voucher',
#             'objects': http.request.env['vieterp_account_voucher.vieterp_account_voucher'].search([]),
#         })

#     @http.route('/vieterp_account_voucher/vieterp_account_voucher/objects/<model("vieterp_account_voucher.vieterp_account_voucher"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vieterp_account_voucher.object', {
#             'object': obj
#         })