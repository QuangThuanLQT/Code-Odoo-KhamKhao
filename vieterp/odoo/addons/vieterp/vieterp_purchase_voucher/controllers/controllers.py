# -*- coding: utf-8 -*-
from odoo import http

# class VieterpPurchaseVoucher(http.Controller):
#     @http.route('/vieterp_purchase_voucher/vieterp_purchase_voucher/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vieterp_purchase_voucher/vieterp_purchase_voucher/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vieterp_purchase_voucher.listing', {
#             'root': '/vieterp_purchase_voucher/vieterp_purchase_voucher',
#             'objects': http.request.env['vieterp_purchase_voucher.vieterp_purchase_voucher'].search([]),
#         })

#     @http.route('/vieterp_purchase_voucher/vieterp_purchase_voucher/objects/<model("vieterp_purchase_voucher.vieterp_purchase_voucher"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vieterp_purchase_voucher.object', {
#             'object': obj
#         })