# -*- coding: utf-8 -*-

from odoo import models, fields, api

class vieterp_passport(models.Model):
    _name = 'passport'

    name = fields.Char(string='Số hộ chiếu')
    partner_id = fields.Many2one('res.partner', string='Người đứng tên')
    ngay_cap = fields.Date(string='Ngày cấp')
    ngay_het_han = fields.Date(string='Ngày hết hạn')
    image = fields.Binary(string='')
    state = fields.Selection([('available', 'Có hiệu lực'), ('expire', 'Hết hạn')], default='available',string="Trạng thái")

    _sql_constraints = [('passpor_number_uniq', 'unique (name)', "Số hộ chiếu đã tồn tại!")]

class passpor_booking(models.Model):
    _name = 'passport.booking'
    _inherit = "mail.thread"

    name = fields.Char(string='Mã đặt', default="/")
    customer_id = fields.Many2one('res.partner',string='Khách hàng')
    pricelist_id = fields.Many2one('product.pricelist', string='Bảng giá')
    email = fields.Char(string='Email')
    mobile = fields.Char(string='Số di động')
    ngay_dat = fields.Date(string='Ngày đặt')
    nguoi_phu_trach = fields.Many2one('res.users', string = 'Người phụ trách')
    holder_id = fields.Many2one('res.partner', string='Người đứng tên')
    passport_number = fields.Char(string='Số hộ chiếu')
    ngay_cap = fields.Date(string='Ngày cấp')
    ngay_het_han = fields.Date(string='Ngày hết hạn')
    product_id = fields.Many2one('product.product', string='Sản phẩm dịch vụ hộ chiếu')
    price = fields.Float(string='Phí dịch vụ')
    sale_ids = fields.One2many('sale.order','passport_booking_id')
    invoice_ids = fields.One2many('account.invoice','passport_booking_id')
    attachment_ids = fields.One2many('ir.attachment', 'passport_booking_id')
    docurement_ids = fields.One2many('passport.booking.docurement', 'passport_booking_id')
    state = fields.Selection([('draft', 'Dự thảo'), ('confirm', 'Đã xác nhận'),('verify','Đã thẩm định'),('approve','Đã phê duyệt'),('done','Đã cấp'),('cancel', 'Hủy')], default='draft',string="Trạng thái")

    _sql_constraints = [('passpor_number_uniq', 'unique (passpor_number)', "Số hộ chiếu đã tồn tại!")]

    @api.multi
    def confirm(self):
        if self.state == 'draft':
            self.state = 'confirm'

    @api.multi
    def verify(self):
        if self.state == 'confirm':
            self.state = 'verify'

    @api.multi
    def approve(self):
        if self.state == 'verify':
            self.state = 'approve'

    @api.multi
    def issue_passport(self):
        if self.state == 'approve':
            self.state = 'done'
            self.env['passport'].create({
                'name' : self.passport_number,
                'partner_id' : self.holder_id.id,
                'ngay_cap' : self.ngay_cap,
                'ngay_het_han' : self.ngay_het_han
            })



class passpor_booking_docurement(models.Model):
    _name = 'passport.booking.docurement'

    document_type_id = fields.Many2one('docurement_type', string="Loại tài liệu")
    description = fields.Text(string='Mô tả')
    qty_original = fields.Integer(string='Số lượng bản')
    passport_booking_id = fields.Many2one('passport.booking')

class ir_attachment_ihr(models.Model):
    _inherit = 'ir.attachment'

    document_type_id = fields.Many2one('docurement_type', string="Loại tài liệu")
    passport_booking_id = fields.Many2one('passport.booking')

class docurement_type(models.Model):
    _name = 'docurement_type'

    name = fields.Char(string='Tên')
    description = fields.Text(string='Mô tả')

class sale_order_ihr(models.Model):
    _inherit = 'sale.order'

    passport_booking_id = fields.Many2one('passport.booking')

class account_invoice_ihr(models.Model):
    _inherit = 'account.invoice'

    passport_booking_id = fields.Many2one('passport.booking')




