# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime,timedelta ,date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError, ValidationError
import json

class purchase_tour(models.Model):
    _name = 'purchase.tour'

    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")
    ma_so_du_toan = fields.Char(string="Mã số dự toán")
    lich_trinh = fields.Char(string="Lịch trình")
    dieu_hanh = fields.Many2one('res.users', string="Người điều hành")
    purchase_tour_line = fields.One2many('purchase.tour.line','purchase_tour_line_id')
    detail_purchase_line = fields.One2many('detail.purchase','detail_purchase_id')
    tour_type = fields.Selection([('tour_ghep', 'Tour Ghép'), ('tour_tyc', 'Tour Theo Yêu Cầu')],string="Loại tour", default='tour_ghep', required=True)
    sale_order_tour = fields.Many2one('sale.order', domain=[('tour_type', '=', 'tour_tyc')], string='Đơn hàng')
    detail_purchase_tyc_ids = fields.One2many('detail.purchase.tyc','purchase_tour_id')
    tour_code = fields.Char(string='Mã đoàn', related='sale_order_tour.tour.default_code', readonly=1)
    product_tyc_id = fields.Many2one('product.product', string='Lịch Trình', related='sale_order_tour.tour', readonly=1)
    du_toan_line = fields.One2many('du.toan','du_toan_id',string="Dự toán")
    count_purchase_order = fields.Integer(compute="get_count_purchase_order")
    sale_order_ids = fields.Char()
    tong_tc = fields.Float(string="Tổng cộng",compute="get_purchase_tour_line",store=True)
    tong_du_toan = fields.Float(string="Tổng dự toán",compute="get_detail_purchase_line",store=True)
    tong_thuc_te = fields.Float(string="Tổng thực tế",compute="get_detail_purchase_line",store=True)
    tong_sale = fields.Float(string="Tổng Sale",compute="get_detail_purchase_tyc_ids",store=True)
    tong_dieu_hanh = fields.Float(string="Tổng điều hành",compute="get_detail_purchase_tyc_ids",store=True)
    tong_hdv_thu = fields.Float(string="Tổng HDV thu",compute="get_detail_purchase_line",store=True)

    @api.depends('detail_purchase_tyc_ids')
    def get_detail_purchase_tyc_ids(self):
        for rec in self:
            sum_sale = 0
            sum_dh = 0
            for r in rec.detail_purchase_tyc_ids:
                sum_sale += r.so_luong * r.so_pax * r.don_gia
                sum_dh += r.dieu_hanh_price
            rec.tong_sale = sum_sale
            rec.tong_dieu_hanh = sum_dh

    @api.depends('detail_purchase_line')
    def get_detail_purchase_line(self):
        for rec in self:
            sum_dt = 0
            sum_tt = 0
            sum_hdv_thu = 0
            for r in rec.detail_purchase_line:
                sum_dt += r.du_toan
                sum_tt += r.thuc_te
                sum_hdv_thu += r.hdv_thu
            rec.tong_du_toan = sum_dt
            rec.tong_thuc_te = sum_tt
            rec.tong_hdv_thu = sum_hdv_thu


    @api.depends('purchase_tour_line')
    def get_purchase_tour_line(self):
        for rec in self:
            sum = 0
            for r in rec.purchase_tour_line:
                sum += r.tc
            rec.tong_tc = sum

    @api.onchange('product_tyc_id')
    def onchange_product_tyc_id(self):
        for rec in self:
            rec.lich_trinh = rec.product_tyc_id.name

    @api.multi
    def get_count_purchase_order(self):
        for record in self:
            record.count_purchase_order = len(self.env['purchase.order'].search([('purchase_tour_id', '=', record.id)]))

    @api.multi
    def purchase_action(self):
        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['domain'] = [('purchase_tour_id', '=', self.id)]
        # action['context'] = {'default_tour': self.id, 'default_is_tour_booking': True}
        return action

    @api.multi
    def name_get(self):
        return [(purchase.id, purchase.ma_so_du_toan or '') for purchase in self]

    def xoa_po(self, po_line_id):
        po_id = po_line_id.order_id
        if po_id.state == 'purchase':
            raise UserError(_("Không thể xoá đơn mua hàng đã xác nhận."))
        if len(po_id.order_line) == 1:
            po_id.button_cancel()
            po_id.unlink()
        else:
            po_line_id.unlink()

    @api.multi
    def create_po(self, detail_purchase_ids):
        for detail_purchase_id in detail_purchase_ids:
            partner_id = detail_purchase_id.partner_id
            po_ids = self.env['purchase.order'].search([('purchase_tour_id', '=', self.id),('partner_id','=',partner_id.id)])
            if not po_ids:
                self.env['purchase.order'].create({
                    'partner_id': detail_purchase_id.partner_id.id,
                    'purchase_tour_id': self.id,
                    'order_line': [(0, 0, {
                        'product_id': detail_purchase_id.so_phong.id,
                        'name': detail_purchase_id.so_phong.name,
                        'product_qty': detail_purchase_id.sl,
                        'price_unit': detail_purchase_id.don_gia,
                        'detail_purchase_id': detail_purchase_id.id,
                        'product_uom': detail_purchase_id.so_phong.uom_po_id.id,
                        'date_planned': datetime.now(),
                        'so_pax': detail_purchase_id.so_pax,
                        'phu_thu': detail_purchase_id.phu_thu,

                    })]
                })
            else:
                po_id = po_ids[0]
                po_id.order_line += po_id.order_line.new({
                    'product_id': detail_purchase_id.so_phong.id,
                    'name': detail_purchase_id.so_phong.name,
                    'product_qty': detail_purchase_id.sl,
                    'price_unit': detail_purchase_id.don_gia,
                    'detail_purchase_id': detail_purchase_id.id,
                    'product_uom': detail_purchase_id.so_phong.uom_po_id.id,
                    'date_planned': datetime.now(),
                    'so_pax': detail_purchase_id.so_pax,
                    'phu_thu': detail_purchase_id.phu_thu,
                })


    # @api.multi
    # def button_confirm(self):
    #     for line in self.detail_purchase_line:
    #         purchase_line_id = self.env['purchase.order.line'].search([('detail_purchase_id', '=', line.id)])
    #         if not purchase_line_id:
    #             self.create_po(line)

    @api.multi
    def upadte_purchase_order(self):
        for line in self.detail_purchase_line:
            if line.partner_id:
                purchase_line_id = self.env['purchase.order.line'].search([('detail_purchase_id', '=', line.id)])
                if purchase_line_id:
                    if line.partner_id != purchase_line_id.order_id.partner_id:
                        self.xoa_po(purchase_line_id)
                        self.create_po(line)
                    else:
                        purchase_line_id.update({
                            'product_id': line.so_phong.id,
                            'name': line.so_phong.name,
                            'product_qty': line.sl,
                            'price_unit': line.don_gia,
                            'so_pax': line.so_pax,
                            'phu_thu': line.phu_thu,
                        })
                else:
                    self.create_po(line)

    @api.multi
    def create_po_tyc(self, detail_purchase_tyc_ids):
        for detail_purchase_tyc_id in detail_purchase_tyc_ids:
            partner_id = detail_purchase_tyc_id.partner_id
            po_ids = self.env['purchase.order'].search(
                [('purchase_tour_id', '=', self.id), ('partner_id', '=', partner_id.id)])
            if not po_ids:
                self.env['purchase.order'].create({
                    'partner_id': detail_purchase_tyc_id.partner_id.id,
                    'purchase_tour_id': self.id,
                    'order_line': [(0, 0, {
                        'product_id': detail_purchase_tyc_id.chi_tiet.id,
                        'name': detail_purchase_tyc_id.chi_tiet.name,
                        'product_qty': detail_purchase_tyc_id.so_luong,
                        'price_unit': detail_purchase_tyc_id.don_gia,
                        'detail_purchase_tyc_id': detail_purchase_tyc_id.id,
                        'product_uom': detail_purchase_tyc_id.chi_tiet.uom_po_id.id,
                        'date_planned': datetime.now(),
                        'so_pax': detail_purchase_tyc_id.so_pax,

                    })]
                })
            else:
                po_id = po_ids[0]
                po_id.order_line += po_id.order_line.new({
                    'product_id': detail_purchase_tyc_id.chi_tiet.id,
                    'name': detail_purchase_tyc_id.chi_tiet.name,
                    'product_qty': detail_purchase_tyc_id.so_luong,
                    'price_unit': detail_purchase_tyc_id.don_gia,
                    'detail_purchase_tyc_id': detail_purchase_tyc_id.id,
                    'product_uom': detail_purchase_tyc_id.chi_tiet.uom_po_id.id,
                    'date_planned': datetime.now(),
                    'so_pax': detail_purchase_tyc_id.so_pax,
                })

    @api.multi
    def upadte_purchase_order_tyc(self):
        for line in self.detail_purchase_tyc_ids:
            if line.partner_id:
                purchase_line_id = self.env['purchase.order.line'].search([('detail_purchase_tyc_id', '=', line.id)])
                if purchase_line_id:
                    if line.partner_id != purchase_line_id.order_id.partner_id:
                        self.xoa_po(purchase_line_id)
                        self.create_po_tyc(line)
                    else:
                        purchase_line_id.update({
                            'product_id': line.chi_tiet.id,
                            'name': line.chi_tiet.name,
                            'product_qty': line.so_luong,
                            'price_unit': line.don_gia,
                            'so_pax': line.so_pax,
                        })
                else:
                    self.create_po_tyc(line)

    @api.onchange('sale_order_tour')
    def onchange_sale_order_tour(self):
        if self.sale_order_tour:
            count = 1
            self.detail_purchase_tyc_ids = []
            for line in self.sale_order_tour.du_toan_sale_order_line:
                new_line = self.detail_purchase_tyc_ids.new({
                    'name' : line.name,
                    'partner_id' : line.partner_id.id,
                    'chi_tiet' : line.chi_tiet,
                    'so_luong': line.so_luong,
                    'so_pax': line.so_pax,
                    'du_toan_so_line_id' : line.id,
                })
                count += 1
                new_line.onchange_get_don_gia()
                self.detail_purchase_tyc_ids += new_line
            self.start_date = self.sale_order_tour.start_date
            self.end_date = self.sale_order_tour.end_date
        else:
            self.detail_purchase_tyc_ids = []
            self.start_date =""
            self.end_date =""

    @api.onchange('start_date','end_date','tour_type')
    def compute_start_end_date(self):
        if self.start_date and self.end_date and self.tour_type:
            self.purchase_tour_line = []
            sale_order_ids = []
            sale_order_have_dieu_hanh_ids = self.env['purchase.tour.line'].search(
                [('purchase_tour_line_id', '!=', False)])
            sale_order_have_dieu_hanh_ids = sale_order_have_dieu_hanh_ids.mapped('sale_tour_id')
            sale_order_id = self.env['sale.order'].search([('tour_type', '=', 'tour_ghep'),('id', 'not in', sale_order_have_dieu_hanh_ids.ids)])
            for rec in sale_order_id:
                if self.start_date <= rec.start_date and self.end_date >= rec.start_date:
                    new_line = self.purchase_tour_line.new({
                        'sale_tour_id': rec.id,
                        'slk': sum(rec.order_line.mapped('product_uom_qty')),
                        'dt' : sum(rec.order_line.mapped('price_unit')),

                        'thu_ho': rec.thu_ho,
                        'noi_dung': rec.ghi_chu,
                        'start_date': rec.start_date,
                        'end_date': rec.end_date,
                        'con_lai': rec.amount_total - rec.thu_ho,
                    })
                    self.purchase_tour_line += new_line
                    sale_order_ids.append(rec.id)

                    self.detail_purchase_tyc_ids = []
                    for line in self.sale_order_tour.tour.dinh_muc_tour_line:
                        new_line = self.detail_purchase_tyc_ids.new({
                            'name': line.name,
                            'partner_id': line.partner_id.id,
                            'so_phong': line.chi_tiet,
                            'so_luong': line.so_luong,
                            'so_pax': line.so_pax,
                        })
                        new_line.onchange_get_don_gia()
                        self.detail_purchase_tyc_ids += new_line

            self.sale_order_ids = str(sale_order_ids)
            start_date = datetime.strptime(self.start_date, DEFAULT_SERVER_DATE_FORMAT)
            end_date = datetime.strptime(self.end_date, DEFAULT_SERVER_DATE_FORMAT)
            data_du_toan_line = {
                'ngay_1' : start_date.strftime("%d/%m/%Y"),
                'check_line_header' : True
            }
            ngay_2 = (start_date + timedelta(days=1))
            if ngay_2 <= end_date:
                data_du_toan_line.update({
                    'ngay_2' : ngay_2.strftime("%d/%m/%Y")
                })
            ngay_3 = (start_date + timedelta(days=2))
            if ngay_3 <= end_date:
                data_du_toan_line.update({
                    'ngay_3' : ngay_3.strftime("%d/%m/%Y")
                })
            ngay_4 = (start_date + timedelta(days=3))
            if ngay_4 <= end_date:
                data_du_toan_line.update({
                    'ngay_4': ngay_4.strftime("%d/%m/%Y")
                })
            ngay_5 = (start_date + timedelta(days=4))
            if ngay_5 <= end_date:
                data_du_toan_line.update({
                    'ngay_5': ngay_5.strftime("%d/%m/%Y")
                })

            self.du_toan_line = self.du_toan_line.new(data_du_toan_line)

        else:
            self.purchase_tour_line = []
            self.du_toan_line = []

    # @api.onchange('purchase_tour_line')
    # def get_sale_order_dt_ids(self):
    #     sale_order_dt_ids = []
    #     for r in self.purchase_tour_line:
    #         sale_order_dt_ids.append(r.sale_tour_id.id)
    #     self.sale_order_dt_ids = str(sale_order_dt_ids)

class purchase_tour_line(models.Model):
    _name = 'purchase.tour.line'

    def _get_sale_tour_domain(self):
        sale_order_have_dieu_hanh_ids = self.env['purchase.tour.line'].search([('purchase_tour_line_id', '!=', False)])
        sale_order_have_dieu_hanh_ids = sale_order_have_dieu_hanh_ids.mapped('sale_tour_id')
        sale_order_ids = self.env['sale.order'].search([('tour_type', '=', 'tour_ghep'),('id', 'not in', sale_order_have_dieu_hanh_ids.ids)])
        return [('id', 'in', sale_order_ids.ids)]

    sale_tour_id = fields.Many2one('sale.order',string="SALE", domain=_get_sale_tour_domain)
    purchase_tour_line_id = fields.Many2one('purchase.tour')
    # slk = fields.Float(string="SLK")
    dt = fields.Float(string="DT",compute="_tc")
    giam_tru = fields.Float(string="Giảm trừ",related="sale_tour_id.tong_giam_tru")
    phu_thu = fields.Float(string="Phụ thu",related="sale_tour_id.tong_phu_thu")
    tc = fields.Float(string="TC",compute="_tc")
    thu_ho = fields.Float(string="Thu hộ",related="sale_tour_id.thu_ho")
    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")
    noi_dung = fields.Char(string="Nội dung")
    hdv = fields.Many2one('res.users', string='HDV')
    con_lai = fields.Float(string="Còn lại",compute="_tc")

    @api.multi
    def _tc(self):
        for rec in self:
            rec.dt = rec.sale_tour_id.amount_untaxed
            rec.tc = rec.sale_tour_id.amount_total
            # rec.tc = rec.dt * rec.slk + rec.ve_cap + rec.phu_thu
            rec.con_lai = rec.tc - rec.thu_ho


class detail_purchase(models.Model):
    _name = 'detail.purchase'
    _order = "sequence"


    sequence = fields.Integer('Sequence')
    muc = fields.Char(string="Mục")
    so_phong = fields.Many2one('product.product',string="Số phòng",domain=[('type_service', '!=', 'tour')])
    partner_id = fields.Many2one('res.partner', string="Nhà cung cấp", domain=[('supplier', '=', True)])
    sl = fields.Integer(string="SL")
    so_pax = fields.Integer(string="Số pax(đêm)")
    don_gia = fields.Float(string="Đơn giá")
    du_toan = fields.Float(string="Dự toán",compute="_get_du_toan", store=True)
    thuc_te = fields.Float(string="Thực tế")
    hdv_thu = fields.Float(string="HDV Thu")
    noi_dung = fields.Char(string="Nội dung")
    sale_purchase_id = fields.Many2many('sale.order','sale_purchase_detail',string="SALE")
    detail_purchase_id = fields.Many2one('purchase.tour')
    phu_thu = fields.Float(string="Phụ thu")

    @api.multi
    def unlink(self):
        for rec in self:
            po_line_id = self.env['purchase.order.line'].search([('detail_purchase_id', '=', rec.id)])
            self.env['purchase.tour'].xoa_po(po_line_id)
        res = super(detail_purchase, self).unlink()
        return res

    @api.depends('sl','so_pax','don_gia','phu_thu')
    def _get_du_toan(self):
        for rec in self:
            rec.du_toan = rec.sl * rec.so_pax * rec.don_gia + rec.phu_thu

    @api.onchange('du_toan')
    def onchange_du_toan(self):
        for rec in self:
            rec.thuc_te = rec.du_toan

    @api.onchange('partner_id', 'so_phong')
    def onchange_get_don_gia(self):
        supplierinfo_ids = self.env['product.supplierinfo'].search(
            [('product_tmpl_id', '=', self.so_phong.product_tmpl_id.id), ('name', '=', self.partner_id.id)])
        if supplierinfo_ids:
            self.don_gia = supplierinfo_ids[0].price

class detail_purchase_sale_order(models.Model):
    _inherit = 'sale.order'
    sale_purchase_detail = fields.Many2one()

class detail_purchase_tyc(models.Model):
    _name = 'detail.purchase.tyc'

    name = fields.Many2one('product.category', string="Mục phục vụ")
    partner_id = fields.Many2one('res.partner', string="Nhà cung cấp" , domain=[('supplier', '=', True)])
    chi_tiet = fields.Many2one('product.product', string="Chi tiết", domain=[('type_service', '!=', 'tour')])
    so_luong = fields.Integer(string="Số lượng")
    so_pax = fields.Integer(string="Số Đêm")
    don_gia = fields.Float(string="Đơn giá")
    sale_price = fields.Float(string="Sale",compute="get_sale_price",store=True)
    dieu_hanh_price = fields.Float(string="Điều Hành")
    note = fields.Text(string='Ghi chú')
    purchase_tour_id = fields.Many2one('purchase.tour')
    du_toan_so_line_id = fields.Many2one('du.toan.sale.order')


    @api.model
    def create(self, vals):
        res = super(detail_purchase_tyc, self).create(vals)
        if 'from_sale_order' not in self._context:
            if not res.du_toan_so_line_id and res.purchase_tour_id.sale_order_tour:
                du_toan_so_line_id = self.env['du.toan.sale.order'].with_context(from_purchase_tour=True).create({
                    'name': res.name.id,
                    'partner_id': res.partner_id.id,
                    'so_luong': res.so_luong,
                    'so_pax': res.so_pax,
                    'note' : res.note,
                    'du_toan_sale_order_id' : res.purchase_tour_id.sale_order_tour.id,
                    'chi_tiet' : res.chi_tiet.id,
                })
                res.du_toan_so_line_id = du_toan_so_line_id
        return res

    @api.multi
    def write(self, vals):
        res = super(detail_purchase_tyc, self).write(vals)
        if 'from_sale_order' not in self._context:
            for rec in self:
                if rec.du_toan_so_line_id:
                    rec.du_toan_so_line_id.with_context(from_purchase_tour=True).write({
                        'name': rec.name.id,
                        'partner_id': rec.partner_id.id,
                        'chi_tiet': rec.chi_tiet.id,
                        'so_luong': rec.so_luong,
                        'so_pax': rec.so_pax,
                        'don_gia': rec.don_gia,
                        'note' : rec.note,
                    })
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            po_line_id = self.env['purchase.order.line'].search([('detail_purchase_tyc_id', '=', rec.id)])
            self.env['purchase.tour'].xoa_po(po_line_id)
            if 'from_sale_order' not in self._context:
                if rec.du_toan_so_line_id:
                    rec.du_toan_so_line_id.with_context(from_purchase_tour=True).unlink()

        res = super(detail_purchase_tyc, self).unlink()
        return res

    @api.depends('so_pax','so_luong','don_gia')
    def get_sale_price(self):
        for rec in self:
            rec.sale_price = rec.so_pax * rec.don_gia * rec.so_luong

    @api.onchange('sale_price')
    def onchange_sale_price(self):
        self.dieu_hanh_price = self.sale_price

    @api.onchange('partner_id', 'chi_tiet')
    def onchange_get_don_gia(self):
        supplierinfo_ids = self.env['product.supplierinfo'].search([('product_tmpl_id', '=', self.chi_tiet.product_tmpl_id.id),('name', '=', self.partner_id.id)])
        if supplierinfo_ids:
            self.don_gia = supplierinfo_ids[0].price


class du_toan_tour(models.Model):
    _name = 'du.toan'

    du_toan_id = fields.Many2one('purchase.tour')
    nhom = fields.Many2one('sale.order',string="Nhóm")
    check_line_header = fields.Boolean(default=False)
    slk = fields.Float(string="SLK",compute="get_slk")
    ngay_1 = fields.Text(string="Ngày 1")
    ngay_2 = fields.Text(string="Ngày 2")
    ngay_3 = fields.Text(string="Ngày 3")
    ngay_4 = fields.Text(string="Ngày 4")
    ngay_5 = fields.Text(string="Ngày 5")

    @api.depends('nhom')
    def get_slk(self):
        for rec in self:
            sum = 0
            for order_line_id in rec.nhom.order_line:
                sum += order_line_id.product_uom_qty
            rec.slk = sum

class sale_order_tour_ihr(models.Model):
    _inherit = 'sale.order'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        sale_order_ids = self._context.get('sale_order_ids', False)
        if sale_order_ids:
            sale_order_ids = json.loads(sale_order_ids)
            args = [('id', 'in', sale_order_ids)]
        res = super(sale_order_tour_ihr, self).name_search(name=name, args=args, operator=operator, limit=limit)
        return res

