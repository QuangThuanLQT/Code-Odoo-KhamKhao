# -*- coding: utf-8 -*-
from odoo import models, fields, api

class account_move_line(models.Model):
    _inherit = 'account.move.line'

    voucher_invoice_id = fields.Many2one('account.invoice')