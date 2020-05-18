# -*- coding: utf-8 -*-

from odoo import models, fields, api

class product_template(models.Model):
    _inherit = 'product.template'

    type_service = fields.Selection([('tour', 'Tour'),('service_diff', 'Dịch vụ khác')], string='Loại dịch vụ')
    duration = fields.Integer(string='Thời gian (ngày)')
    location_start = fields.Char(string="Điểm đón")
    type_tour = fields.Char(string="Loại tour")
    ghi_chu = fields.Text(string="Ghi chú")
    khoi_hanh_type = fields.Many2many('khoi.hanh',string="Khởi hành")

    @api.onchange('type')
    def onchange_type_pt(self):
        if self.type == 'service':
            self.type_service = 'tour'
        else:
            self.type_service = ''


class sale_product(models.Model):
    _inherit = 'product.product'

    price_extra_tour = fields.Float()

    @api.depends('list_price', 'price_extra', 'price_extra_tour')
    def _compute_product_lst_price(self):
        for product in self:
            if product.price_extra_tour:
                product.lst_price = product.price_extra_tour
            else:
                to_uom = None
                if 'uom' in self._context:
                    to_uom = self.env['product.uom'].browse([self._context['uom']])

                if to_uom:
                    list_price = product.uom_id._compute_price(product.list_price, to_uom)
                else:
                    list_price = product.list_price
                product.lst_price = list_price + product.price_extra

class sale_type(models.Model):
    _inherit = 'res.partner'

    type = fields.Char(string="Loại hình kinh doanh")

class khoi_hanh(models.Model):
    _name = 'khoi.hanh'

    name = fields.Char()

