# -*- coding: utf-8 -*-

from odoo import models, fields, api

class tour_manager(models.Model):
    _inherit = 'purchase.tour'

    @api.model
    def get_domain_purchase_tour(self, start_date, end_date):
        domain = []
        context = {'hide_sale': True}

        domain.append(('start_date', '>=', start_date))
        domain.append(('end_date', '<=', end_date))

        return domain, context

    @api.model
    def get_domain_purchase_tour_ghep(self, start_date, end_date):
        domain = [('tour_type', '=', 'tour_ghep')]
        context = {'hide_sale': True}

        domain.append(('start_date', '>=', start_date))
        domain.append(('end_date', '<=', end_date))

        return domain, context

    @api.model
    def get_domain_purchase_tour_tyc(self, start_date, end_date):
        domain = [('tour_type', '=', 'tour_tyc')]
        context = {'hide_sale': True}

        domain.append(('start_date', '>=', start_date))
        domain.append(('end_date', '<=', end_date))

        return domain, context