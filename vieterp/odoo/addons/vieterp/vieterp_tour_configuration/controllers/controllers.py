# -*- coding: utf-8 -*-
from odoo import http

# class VieterpTourConfiguration(http.Controller):
#     @http.route('/vieterp_tour_configuration/vieterp_tour_configuration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vieterp_tour_configuration/vieterp_tour_configuration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vieterp_tour_configuration.listing', {
#             'root': '/vieterp_tour_configuration/vieterp_tour_configuration',
#             'objects': http.request.env['vieterp_tour_configuration.vieterp_tour_configuration'].search([]),
#         })

#     @http.route('/vieterp_tour_configuration/vieterp_tour_configuration/objects/<model("vieterp_tour_configuration.vieterp_tour_configuration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vieterp_tour_configuration.object', {
#             'object': obj
#         })