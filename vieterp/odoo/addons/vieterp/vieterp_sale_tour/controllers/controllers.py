# -*- coding: utf-8 -*-
from odoo import http

# class VieterpSaleTour(http.Controller):
#     @http.route('/vieterp_sale_tour/vieterp_sale_tour/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vieterp_sale_tour/vieterp_sale_tour/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vieterp_sale_tour.listing', {
#             'root': '/vieterp_sale_tour/vieterp_sale_tour',
#             'objects': http.request.env['vieterp_sale_tour.vieterp_sale_tour'].search([]),
#         })

#     @http.route('/vieterp_sale_tour/vieterp_sale_tour/objects/<model("vieterp_sale_tour.vieterp_sale_tour"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vieterp_sale_tour.object', {
#             'object': obj
#         })