# -*- coding: utf-8 -*-

from odoo import models, fields, api

class tour_manager(models.Model):
    _inherit = 'bao.cao.tour'

    @api.model
    def get_domain_order_tour(self, start_date, end_date):
        domain = []
        context = {'hide_sale': True,'default_start_date': start_date,'default_end_date': end_date,'default_check_boolean': False}

        return domain, context

    @api.model
    def get_domain_order_tour_ghep(self, start_date, end_date):
        domain = []
        context = {'hide_sale': True, 'default_start_date': start_date, 'default_end_date': end_date,
                   'default_check_boolean_tour_ghep': False, 'default_check_boolean': False}

        return domain, context

    @api.model
    def get_domain_order_tour_tyc(self, start_date, end_date):
        domain = []
        context = {'hide_sale': True, 'default_start_date': start_date, 'default_end_date': end_date,
                   'default_check_boolean_tour_tyc': False, 'default_check_boolean': False}

        return domain, context

    @api.model
    def get_domain_order_spk(self, start_date, end_date):
        domain = []
        context = {'hide_sale': True, 'default_start_date': start_date, 'default_end_date': end_date,
                   'default_check_boolean_spk': False, 'default_check_boolean': False}

        return domain, context