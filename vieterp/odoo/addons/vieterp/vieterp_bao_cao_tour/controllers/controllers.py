# -*- coding: utf-8 -*-
from odoo import http

# class VieterpBaoCaoTour(http.Controller):
#     @http.route('/vieterp_bao_cao_tour/vieterp_bao_cao_tour/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vieterp_bao_cao_tour/vieterp_bao_cao_tour/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vieterp_bao_cao_tour.listing', {
#             'root': '/vieterp_bao_cao_tour/vieterp_bao_cao_tour',
#             'objects': http.request.env['vieterp_bao_cao_tour.vieterp_bao_cao_tour'].search([]),
#         })

#     @http.route('/vieterp_bao_cao_tour/vieterp_bao_cao_tour/objects/<model("vieterp_bao_cao_tour.vieterp_bao_cao_tour"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vieterp_bao_cao_tour.object', {
#             'object': obj
#         })