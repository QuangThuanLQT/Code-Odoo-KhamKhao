from odoo import models, fields, api

class purchase_request(models.Model):
    _inherit = 'purchase.request'

    tour = fields.Many2one('sale.tour')