# -*- coding: utf-8 -*-
from odoo import http

# class VieterpPurchaseTour(http.Controller):
#     @http.route('/vieterp_purchase_tour/vieterp_purchase_tour/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vieterp_purchase_tour/vieterp_purchase_tour/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vieterp_purchase_tour.listing', {
#             'root': '/vieterp_purchase_tour/vieterp_purchase_tour',
#             'objects': http.request.env['vieterp_purchase_tour.vieterp_purchase_tour'].search([]),
#         })

#     @http.route('/vieterp_purchase_tour/vieterp_purchase_tour/objects/<model("vieterp_purchase_tour.vieterp_purchase_tour"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vieterp_purchase_tour.object', {
#             'object': obj
#         })