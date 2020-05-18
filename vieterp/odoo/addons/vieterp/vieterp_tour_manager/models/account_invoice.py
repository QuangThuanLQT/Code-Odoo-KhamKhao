# -*- coding: utf-8 -*-

from odoo import models, fields, api

class account_invoice_tour(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def get_domain_account_invoice_sale(self, start_date, end_date):
        domain = [('type','in',('out_invoice', 'out_refund'))]
        context = {'hide_sale': True}

        domain.append(('date_invoice', '>=', start_date))
        domain.append(('date_invoice', '<=', end_date))

        return domain, context

    @api.model
    def get_domain_account_invoice_purchase(self, start_date, end_date):
        domain = [('type','in',('in_invoice', 'in_refund'))]
        context = {'hide_sale': True}

        domain.append(('date_invoice', '>=', start_date))
        domain.append(('date_invoice', '<=', end_date))

        return domain, context