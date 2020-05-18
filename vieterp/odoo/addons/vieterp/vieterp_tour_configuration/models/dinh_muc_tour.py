# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class dinh_muc_tour(models.Model):
    _name='dinh.muc.tour'

    name = fields.Many2one('product.category',string="Mục phục vụ")
    partner_id = fields.Many2one('res.partner', string="Nhà cung cấp")
    chi_tiet = fields.Many2one('product.product',string="Chi tiết")
    so_luong = fields.Integer(string="Số lượng")
    so_pax = fields.Integer(string="Số Pax")
    dinh_muc_tour_line_id = fields.Many2one('product.template')

class dinh_muc_tour_ihr(models.Model):
    _inherit = 'product.template'

    dinh_muc_tour_line = fields.One2many('dinh.muc.tour', 'dinh_muc_tour_line_id', string="Hành trình")

class purchase_request_form_ihr(models.Model):
    _inherit = 'purchase.request.line'

    partner_id = fields.Many2one('res.partner', string="Nhà cung cấp")
    muc_phuc_vu = fields.Many2one('product.category', string="Mục phục vụ")
    sale_ids = fields.Many2many('sale.order', string='Đơn hàng')

class purchase_request_ihr(models.Model):
    _inherit = 'purchase.request'

    @api.onchange('tour')
    def onchange_tour_create_prl(self):
        if self.tour:
            list_sp = {}
            sale_ids = self.env['sale.order'].search([('tour', '=', self.tour.id)])
            for sale_id in sale_ids:
                for line in sale_id.order_line:
                    list_sp.update({
                        line.product_id.id : list_sp.get(line.product_id.id, 0) + line.product_uom_qty
                    })

            self.line_ids = []
            for product_id, qty in list_sp.items():
                if product_id and qty:
                    product_line_id = self.env['product.product'].browse(product_id)
                    sale_line_ids = self.env['sale.order.line'].search([('order_id', 'in', sale_ids.ids),('product_id', '=', product_line_id.id)])
                    for dinh_muc_line in product_line_id.dinh_muc_tour_line:
                         new_purchase_request_line = self.line_ids.new({
                            'product_id' : dinh_muc_line.chi_tiet.id,
                            'muc_phuc_vu' : dinh_muc_line.name,
                            'partner_id' : dinh_muc_line.partner_id.id,
                            'sale_ids' : sale_line_ids.mapped('order_id').ids,
                        })
                         new_purchase_request_line.onchange_product_id()
                         new_purchase_request_line.product_qty = dinh_muc_line.so_luong * dinh_muc_line.so_pax
                         new_purchase_request_line.date_required = datetime.now()
                         self.line_ids += new_purchase_request_line
