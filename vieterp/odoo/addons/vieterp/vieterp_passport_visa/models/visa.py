# -*- coding: utf-8 -*-

from odoo import models, fields, api

class vieterp_visa(models.Model):
    _name = 'visa'

    name = fields.Char(string='Số visa')
    partner_id = fields.Many2one('res.partner', string='Người đứng tên')
    ngay_cap = fields.Date(string='Ngày cấp')
    ngay_het_han = fields.Date(string='Ngày hết hạn')
    image = fields.Binary(string='')
    state = fields.Selection([('expire', 'Hết hạn'), ('available', 'Có hiệu lực')], default='available',string="Trạng thái")
    country_id = fields.Many2one('res.country', string="Quốc gia")
    passport_id = fields.Many2one('passport', string="Số hộ chiếu")
    type_visa = fields.Char(string="Loại visa")

class visa_booking(models.Model):
    _name = 'visa.booking'
    _inherit = "mail.thread"

    name = fields.Char(string='Mã đặt', default="/")
    customer_id = fields.Many2one('res.partner',string='Khách hàng')
    pricelist_id = fields.Many2one('product.pricelist', string='Bảng giá')
    email = fields.Char(string='Email')
    mobile = fields.Char(string='Số di động')
    ngay_dat = fields.Date(string='Ngày đặt')
    nguoi_phu_trach = fields.Many2one('res.users', string = 'Người phụ trách')
    holder_id = fields.Many2one('res.partner', string='Người đứng tên')
    visa_number = fields.Char(string='Số visa')
    ngay_cap = fields.Date(string='Ngày cấp')
    ngay_het_han = fields.Date(string='Ngày hết hạn')
    country_id = fields.Many2one('res.country', string="Quốc gia")
    passport_id = fields.Many2one('passport', string="Số hộ chiếu")
    type_visa = fields.Char(string="Loại visa")
    product_id = fields.Many2one('product.product', string='Sản phẩm dịch vụ visa')
    price = fields.Float(string='Phí dịch vụ')
    # sale_ids = fields.One2many('sale.order','visa_booking_id')
    # invoice_ids = fields.One2many('account.invoice','visa_booking_id')
    # attachment_ids = fields.One2many('ir.attachment', 'visa_booking_id')
    # docurement_ids = fields.One2many('visa.booking.docurement', 'visa_booking_id')
    state = fields.Selection([('draft', 'Dự thảo'), ('confirm', 'Đã xác nhận'),('verify','Đã thẩm định'),('approve','Đã phê duyệt'),('done','Đã cấp'),('cancel', 'Hủy')], default='draft',string="Trạng thái")

    _sql_constraints = [('visa_number_uniq', 'unique (visa_number)', "Số visa đã tồn tại!")]

    @api.onchange('holder_id')
    def onchange_holder_id(self):
        res = {}
        res['domain'] = {'passport_id': [('partner_id', '=', self.holder_id.id)]}
        return res

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
    def issue_visa(self):
        if self.state == 'approve':
            self.state = 'done'
            self.env['visa'].create({
                'name': self.visa_number,
                'partner_id': self.holder_id.id,
                'ngay_cap': self.ngay_cap,
                'ngay_het_han': self.ngay_het_han
            })


# class visa_booking_docurement(models.Model):
#     _name = 'visa.booking.docurement'
#
#     document_type_id = fields.Many2one('docurement_type', string="Loại tài liệu")
#     description = fields.Text(string='Mô tả')
#     qty_original = fields.Integer(string='Số lượng bản')
#     visa_booking_id = fields.Many2one('visa.booking')
#
#
# class ir_attachment_visa_ihr(models.Model):
#     _inherit = 'ir.attachment'
#
#     document_type_id = fields.Many2one('docurement_type', string="Loại tài liệu")
#     visa_booking_id = fields.Many2one('visa.booking')
#
#
# class docurement_type(models.Model):
#     _name = 'docurement_type'
#
#     name = fields.Char(string='Tên')
#     description = fields.Text(string='Mô tả')
#
#
# class sale_order_ihr(models.Model):
#     _inherit = 'sale.order'
#
#     visa_booking_id = fields.Many2one('visa.booking')
#
#
# class account_invoice_ihr(models.Model):
#     _inherit = 'account.invoice'
#
#     visa_booking_id = fields.Many2one('visa.booking')