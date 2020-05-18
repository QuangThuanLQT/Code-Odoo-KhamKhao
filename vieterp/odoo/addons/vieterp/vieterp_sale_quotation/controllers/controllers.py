# -*- coding: utf-8 -*-
from odoo import http

# class VieterpSaleQuotation(http.Controller):
#     @http.route('/vieterp_sale_quotation/vieterp_sale_quotation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vieterp_sale_quotation/vieterp_sale_quotation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vieterp_sale_quotation.listing', {
#             'root': '/vieterp_sale_quotation/vieterp_sale_quotation',
#             'objects': http.request.env['vieterp_sale_quotation.vieterp_sale_quotation'].search([]),
#         })

#     @http.route('/vieterp_sale_quotation/vieterp_sale_quotation/objects/<model("vieterp_sale_quotation.vieterp_sale_quotation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vieterp_sale_quotation.object', {
#             'object': obj
#         })