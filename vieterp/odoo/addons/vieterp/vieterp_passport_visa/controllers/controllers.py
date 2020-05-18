# -*- coding: utf-8 -*-
from odoo import http

# class VieterpPassportVisa(http.Controller):
#     @http.route('/vieterp_passport_visa/vieterp_passport_visa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vieterp_passport_visa/vieterp_passport_visa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vieterp_passport_visa.listing', {
#             'root': '/vieterp_passport_visa/vieterp_passport_visa',
#             'objects': http.request.env['vieterp_passport_visa.vieterp_passport_visa'].search([]),
#         })

#     @http.route('/vieterp_passport_visa/vieterp_passport_visa/objects/<model("vieterp_passport_visa.vieterp_passport_visa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vieterp_passport_visa.object', {
#             'object': obj
#         })