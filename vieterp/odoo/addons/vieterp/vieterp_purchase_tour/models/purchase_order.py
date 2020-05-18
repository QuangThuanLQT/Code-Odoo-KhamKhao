# -*- coding: utf-8 -*-

from odoo import models, fields, api

class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    so_pax = fields.Float(string="Số pax(đêm)")
    phu_thu = fields.Float(string="Phụ thu")
    detail_purchase_id = fields.Many2one('detail.purchase')
    detail_purchase_tyc_id = fields.Many2one('detail.purchase.tyc')


    @api.depends('product_qty', 'price_unit', 'taxes_id','so_pax','phu_thu')
    def _compute_amount(self):
        for line in self:
            taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty,
                                              product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'] * line.so_pax + line.phu_thu,
            })

class purchase_order(models.Model):
    _inherit = 'purchase.order'

    purchase_tour_id = fields.Many2one('purchase.tour')


