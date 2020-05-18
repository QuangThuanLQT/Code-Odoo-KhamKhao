# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_tour(models.Model):
    _name = 'sale.tour'

    name = fields.Char(string="Tên Tour")
    tour_code = fields.Char(string="Mã Tour")
    tour_id = fields.Many2one('product.template', domain=[('type_service', '=', 'tour')], string='Tour', required=1)
    type_tour = fields.Char(string="Loại tour", related='tour_id.type_tour')
    duration = fields.Integer(string='Thời gian (ngày)', related='tour_id.duration')
    total_seat = fields.Integer(string='Số người tối đa')
    available_seat = fields.Integer(string='Số chỗ còn', compute="get_available_seat")
    lich_trinh = fields.Many2one('sale.schedule', string="Lịch trình")
    start_date = fields.Date(string="Ngày khởi hành")
    end_date = fields.Date(string="Ngày kết thúc")
    book_date = fields.Date(string="Hạn chót đặt tour")
    dieu_hanh = fields.Many2one('res.users',string="Điều hành")
    hdv = fields.Many2one('res.users',string="HDV")
    email = fields.Char(string="Email")
    sdt = fields.Char(string="Số Điện Thoại")
    count_sale_order = fields.Integer(compute="get_count_sale_order")
    state = fields.Selection([('draft', 'Bản thảo'),('confirm', 'Mở bán') , ('waiting', 'Đang thực thiện'), ('done', 'Hoàn thành'),('cancel', 'Huỷ')], default='draft')
    sale_tour_variant_ids = fields.One2many('sale.tour.variant', 'sale_tour_id')

    @api.onchange('tour_id')
    def onchange_tour_id(self):
        self.name = self.tour_id.name
        self.sale_tour_variant_ids = []
        for product_id in self.tour_id.product_variant_ids:
            self.sale_tour_variant_ids += self.sale_tour_variant_ids.new({
                'product_id' : product_id.id,
                'description' : product_id.name,
                'price' : product_id.lst_price,
            })

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_waiting(self):
        self.state = 'waiting'

    @api.multi
    def action_confirm(self):
        self.state = 'confirm'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'

    @api.onchange('hdv')
    def onchange_hdv(self):
        self.email = self.hdv.login
        self.sdt = self.hdv.mobile or self.hdv.phone

    @api.multi
    def get_available_seat(self):
        total = 0
        for record in self:
            record.sale_order = self.env['sale.order'].search([('tour', '=', record.id)])
            for rec in record.sale_order:
                for r in rec.order_line:
                    total += r.product_uom_qty
        self.available_seat = self.total_seat - total


    @api.multi
    def get_count_sale_order(self):
        for record in self:
            record.count_sale_order = len(self.env['sale.order'].search([('tour', '=', record.id)]))
    @api.multi
    def sale_action(self):
        action = self.env.ref('sale.action_orders').read()[0]
        action['domain'] = [('tour', '=', self.id)]
        action['context'] = {'default_tour' : self.id, 'default_is_tour_booking' : True}
        return action

    @api.model
    def create(self, vals):
        prefix = self.env['ir.sequence'].next_by_code('sale.tour') or ''
        vals['tour_code'] = '%s%s' % (prefix and '%s ' % prefix or '', vals.get('tour_code', ''))
        sale_code = super(sale_tour, self).create(vals)
        return sale_code

class sale_tour_variant(models.Model):
    _name = 'sale.tour.variant'

    product_id = fields.Many2one('product.product', string="Sản phẩm")
    description = fields.Char(string='Mô tả')
    price = fields.Float(string='Giá bán')
    qty_booked = fields.Integer(string='Số lượng đã bán')
    sale_tour_id = fields.Many2one('sale.tour')
