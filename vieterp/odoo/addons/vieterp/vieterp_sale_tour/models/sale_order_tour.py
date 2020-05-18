# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import json
from odoo.tools import float_compare, float_is_zero

class account_move_line(models.Model):
    _inherit = "account.move.line"

    def update_open_amount_residual(self,credit,debit):
        for line in self:
            if not line.account_id.reconcile:
                self._cr.execute("""UPDATE account_move_line SET reconciled=FALSE, amount_residual=0,amount_residual_currency=0
                                                                    WHERE id=%s""" % (line.id))
                continue
            #amounts in the partial reconcile table aren't signed, so we need to use abs()
            amount = abs(debit - credit)
            amount_residual_currency = abs(line.amount_currency) or 0.0
            sign = 1 if (debit - credit) > 0 else -1
            if not debit and not credit and line.amount_currency and line.currency_id:
                #residual for exchange rate entries
                sign = 1 if float_compare(line.amount_currency, 0, precision_rounding=line.currency_id.rounding) == 1 else -1

            for partial_line in (line.matched_debit_ids + line.matched_credit_ids):
                # If line is a credit (sign = -1) we:
                #  - subtract matched_debit_ids (partial_line.credit_move_id == line)
                #  - add matched_credit_ids (partial_line.credit_move_id != line)
                # If line is a debit (sign = 1), do the opposite.
                sign_partial_line = sign if partial_line.credit_move_id == line else (-1 * sign)

                amount += sign_partial_line * partial_line.amount
                #getting the date of the matched item to compute the amount_residual in currency
                if line.currency_id:
                    if partial_line.currency_id and partial_line.currency_id == line.currency_id:
                        amount_residual_currency += sign_partial_line * partial_line.amount_currency
                    else:
                        if line.balance and line.amount_currency:
                            rate = line.amount_currency / line.balance
                        else:
                            date = partial_line.credit_move_id.date if partial_line.debit_move_id == line else partial_line.debit_move_id.date
                            rate = line.currency_id.with_context(date=date).rate
                        amount_residual_currency += sign_partial_line * line.currency_id.round(partial_line.amount * rate)

            #computing the `reconciled` field. As we book exchange rate difference on each partial matching,
            #we can only check the amount in company currency
            reconciled = False
            digits_rounding_precision = line.company_id.currency_id.rounding
            if float_is_zero(amount, precision_rounding=digits_rounding_precision):
                if line.currency_id and line.amount_currency:
                    if float_is_zero(amount_residual_currency, precision_rounding=line.currency_id.rounding):
                        reconciled = True
                else:
                    reconciled = True
            self._cr.execute("""UPDATE account_move_line SET reconciled=%s, amount_residual=%s,amount_residual_currency=%s
                                            WHERE id=%s""" % (reconciled,line.company_id.currency_id.round(amount * sign),
                                                              line.currency_id and line.currency_id.round(
                                                              amount_residual_currency * sign) or 0.0,line.id))
            return line.company_id.currency_id.round(amount * sign)

class account_invoice_ihr(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def get_move_line_from_inv(self):
        for inv in self:
            if not inv.journal_id.sequence_id:
                raise UserError(_('Please define sequence on the journal related to this invoice.'))
            if not inv.invoice_line_ids:
                raise UserError(_('Please create some invoice lines.'))

            ctx = dict(self._context, lang=inv.partner_id.lang)

            if not inv.date_invoice:
                inv.with_context(ctx).write({'date_invoice': fields.Date.context_today(self)})
            company_currency = inv.company_id.currency_id

            # create move lines (one per invoice line + eventual taxes and analytic lines)
            iml = inv.invoice_line_move_line_get()
            iml += inv.tax_line_move_line_get()

            diff_currency = inv.currency_id != company_currency
            # create one move line for the total and possibly adjust the other lines amount
            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, iml)

            name = inv.name or '/'
            if inv.payment_term_id:
                totlines = \
                    inv.with_context(ctx).payment_term_id.with_context(currency_id=company_currency.id).compute(total,
                                                                                                                inv.date_invoice)[
                        0]
                res_amount_currency = total_currency
                ctx['date'] = inv._get_currency_rate_date()
                for i, t in enumerate(totlines):
                    if inv.currency_id != company_currency:
                        amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
                    else:
                        amount_currency = False

                    # last line: add the diff
                    res_amount_currency -= amount_currency or 0
                    if i + 1 == len(totlines):
                        amount_currency += res_amount_currency

                    iml.append({
                        'type': 'dest',
                        'name': name,
                        'price': t[1],
                        'account_id': inv.account_id.id,
                        'date_maturity': t[0],
                        'amount_currency': diff_currency and amount_currency,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'invoice_id': inv.id
                    })
            else:
                iml.append({
                    'type': 'dest',
                    'name': name,
                    'price': total,
                    'account_id': inv.account_id.id,
                    'date_maturity': inv.date_due,
                    'amount_currency': diff_currency and total_currency,
                    'currency_id': diff_currency and inv.currency_id.id,
                    'invoice_id': inv.id
                })
            part = self.env['res.partner']._find_accounting_partner(inv.partner_id)
            line = [(0, 0, self.line_get_convert(l, part.id)) for l in iml]
            line = inv.group_lines(iml, line)

            journal = inv.journal_id.with_context(ctx)
            line = inv.finalize_invoice_move_lines(line)

        return line

class sale_order(models.Model):
    _inherit = 'sale.order'

    tour = fields.Many2one('product.product',domain="[('type_service', '=', 'tour')]")
    tour_type = fields.Selection([('tour_ghep', 'Tour Ghép'),('tour_tyc', 'Tour Theo Yêu Cầu')], compute='_get_tour_type', store=True)
    is_tour_booking = fields.Boolean('Đặt Tour')
    so_tien_da_thu = fields.Float(string="Số tiền đã thu",compute="get_so_tien_da_thu")
    so_tien_can_thu = fields.Float(string="Số tiền cần phải thu",compute="get_so_tien_da_thu")
    thu_ho = fields.Float(string="Thu hộ")
    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")
    sale_name = fields.Char(string="Mã số sale",compute="compute_sale_name",store=True)
    ghi_chu = fields.Text(string="Nội dung")
    ve_cap = fields.Float(string="Vé cáp")
    phu_thu = fields.Float(string="Phụ thu")
    phu_thu_line = fields.One2many('phu.thu.line','phu_thu_line_id')
    giam_tru_line = fields.One2many('giam.tru.line','giam_tru_line_id')
    tong_phu_thu = fields.Float(string="Tổng phụ thu",compute="get_tong_phu_thu",store=True)
    tong_giam_tru = fields.Float(string="Tổng giảm trừ",compute="get_tong_giam_tru",store=True)
    danh_sach_khach = fields.Text(string="Danh sách khách")
    khach_san = fields.Text(string="Khách sạn")
    type_san_pham_khac = fields.Many2one('san.pham.khac',string="Loại dịch vụ")
    du_toan_sale_order_line = fields.One2many('du.toan.sale.order','du_toan_sale_order_id')


    @api.multi
    def update_invoice_sale_tour(self):
        for order in self:
            if len(order.invoice_ids) == 1:
                check = False
                invoice_line_ids = order.invoice_ids.mapped('invoice_line_ids')
                for invoice_line_id in invoice_line_ids:
                    if not invoice_line_id.sale_line_ids:
                        self._cr.execute("""DELETE FROM account_invoice_line WHERE id=%s""" % (invoice_line_id.id))
                    else:
                        order_line_id = invoice_line_id.sale_line_ids[0]
                        if order_line_id:
                            if not check:
                                invoice_line_id.write({
                                    'quantity': order_line_id.product_uom_qty,
                                    'price_unit': order_line_id.price_unit,
                                    'tong_phu_thu': order.tong_phu_thu,
                                    'tong_giam_tru': order.tong_giam_tru,
                                })
                            else:
                                invoice_line_id.write({
                                    'quantity': order_line_id.product_uom_qty,
                                    'price_unit': order_line_id.price_unit,
                                })
                            invoice_line_id._compute_price()
                            if order_line_id.product_id != invoice_line_id.product_id:
                                invoice_line_id.product_id = order_line_id.product_id
                                invoice_line_id.name = order_line_id.name
                            check = True
                for invoice_id in order.invoice_ids.filtered(lambda inv: inv.move_id):
                    move_line = self.env['account.move.line']
                    line_not_ext = self.env['account.move.line']
                    move_line_data = invoice_id.get_move_line_from_inv()
                    for line_data in move_line_data:
                        line_data = line_data[2]
                        move_line_change = (invoice_id.move_id.mapped('line_ids') - move_line).filtered(
                            lambda mvl: mvl.product_id.id == line_data.get('product_id', False)
                                        and mvl.account_id.id == line_data.get('account_id', False))
                        if move_line_change:
                            for line in move_line_change:
                                if line.id not in line_not_ext.ids:
                                    line_not_ext += line
                                if line.credit != line_data.get('credit', 0) or line.debit != line_data.get('debit', 0):
                                    self._cr.execute("""UPDATE account_move_line SET credit=%s, debit=%s
                                                    WHERE id=%s""" % (
                                    line_data.get('credit', 0) or 0, line_data.get('debit', 0) or 0, line.id))
                                    self._cr.commit()
                                    order.invoice_ids.residual = line.update_open_amount_residual(line_data.get('credit', 0),line_data.get('debit', 0))
                                    move_line += line
                                    break

    @api.multi
    def open_validate(self):
        action = self.env.ref('vieterp_sale_tour.validate_sale_action').read()[0]
        action['context'] = "{'default_sale_order_id': %s,'default_partner_id': %s}" % (self.id, self.partner_id.id)
        return action

    @api.multi
    def get_so_tien_da_thu(self):
        for rec in self:
            invoices = self.mapped('invoice_ids')
            if invoices:
                for r in invoices:
                    rec.so_tien_can_thu += r.residual
                rec.so_tien_da_thu = rec.amount_total - rec.so_tien_can_thu
            else:
                rec.so_tien_can_thu = rec.amount_total

    @api.depends('phu_thu_line')
    def get_tong_phu_thu(self):
        for rec in self:
            sum = 0
            for r in rec.phu_thu_line:
                sum += r.thanh_tien
            rec.tong_phu_thu = sum

    @api.depends('giam_tru_line')
    def get_tong_giam_tru(self):
        for rec in self:
            sum = 0
            for r in rec.giam_tru_line:
                sum += r.thanh_tien
            rec.tong_giam_tru = sum

    @api.depends('order_line.price_total','tong_phu_thu','tong_giam_tru')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                                    product=line.product_id, partner=order.partner_shipping_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax + order.tong_phu_thu - order.tong_giam_tru,
            })


    @api.depends('tour')
    def _get_tour_type(self):
        for rec in self:
            theo_yeu_cau = self.env.ref('vieterp_sale_tour.theo_yeu_cau')
            if rec.tour and theo_yeu_cau.id in rec.tour.khoi_hanh_type.ids:
                rec.tour_type = 'tour_tyc'
            else:
                rec.tour_type = 'tour_ghep'
    @api.multi
    def name_get(self):
        return [(sale.id, sale.sale_name or '') for sale in self]

    @api.onchange('is_tour_booking')
    def onchange_is_tour_booking(self):
        if not self.is_tour_booking:
            self.tour = False

    @api.onchange('tour')
    def onchange_tour(self):
        self.order_line = []
        for product_id in self.tour.product_variant_ids:
            new_order_line = self.order_line.new({
                'product_id': product_id.id,
                'description': product_id.name,
                'price_unit': product_id.lst_price,
            })
            new_order_line.product_id_change()
            self.order_line += new_order_line

        self.du_toan_sale_order_line = []
        for line in self.tour.dinh_muc_tour_line:
            new_line = self.du_toan_sale_order_line.new({
                'name': line.name,
                'partner_id': line.partner_id.id,
                'so_phong': line.chi_tiet,
                'so_luong': line.so_luong,
                'so_pax': line.so_pax,

            })
            self.du_toan_sale_order_line += new_line

    @api.depends('tour', 'user_id')
    def compute_sale_name(self):
        user_name = ''
        if self.user_id.name:
            user_name = self.user_id.name.split(' ')
            user_name = user_name[len(user_name) - 1]
        self.sale_name = user_name + ' ' + str(self.tour.default_code or '')


class phu_thu_line_ihr(models.Model):
    _name = 'phu.thu.line'

    thong_tin = fields.Char(string="Thông tin")
    so_luong = fields.Integer(string="Số lượng")
    don_gia = fields.Float(string="Đơn giá")
    thanh_tien = fields.Float(string="Thành tiền",compute="get_thanh_tien",store=True)
    phu_thu_line_id = fields.Many2one('sale.order')

    @api.depends('so_luong','don_gia')
    def get_thanh_tien(self):
        for rec in self:
            rec.thanh_tien = rec.so_luong * rec.don_gia

class giam_tru_line_ihr(models.Model):
    _name = 'giam.tru.line'

    thong_tin = fields.Char(string="Thông tin")
    so_luong = fields.Integer(string="Số lượng")
    don_gia = fields.Float(string="Đơn giá")
    thanh_tien = fields.Float(string="Thành tiền",compute="get_thanh_tien",store=True)
    giam_tru_line_id = fields.Many2one('sale.order')

    @api.depends('so_luong','don_gia')
    def get_thanh_tien(self):
        for rec in self:
            rec.thanh_tien = rec.so_luong * rec.don_gia

class validate_sale(models.TransientModel):
    _name = 'validate.sale'

    sale_order_id = fields.Many2one('sale.order')
    partner_id = fields.Many2one('res.partner',string="Khách hàng", required=True)
    payment_method = fields.Many2one('account.journal',string="Phương thức thanh toán", domain="[('type', 'in', ['cash', 'bank'])]", required=True)
    so_tien = fields.Float(string="Số tiền", required=True)

    @api.multi
    def create_sale_receipt(self):
        sale_receipt_id = self.env['account.voucher'].with_context({'default_voucher_type': 'sale', 'voucher_type': 'sale'}).create({
            'partner_id' : self.partner_id.id,
            'payment_journal_id' : self.payment_method.id,
            'add_price' : self.so_tien,
            'account_id' : self.payment_method.default_debit_account_id.id,
        })
        invoice_ids = self.sale_order_id.invoice_ids
        for invoice_id in invoice_ids:
            account_id_131 = self.env['account.account'].search([('code', '=', 131)], limit=1)
            order_id = self.sale_order_id
            sale_receipt_id.invoice_line += sale_receipt_id.invoice_line.new({
                'invoice': invoice_id.id,
                'residual': invoice_id.residual,
                'sale_order_id': order_id.id,
                'amount_collected': invoice_id.amount_total - invoice_id.residual,
                'amount_total': invoice_id.amount_total,
                'date_invoice': invoice_id.date_invoice,
                'account_id': account_id_131.id or False
            })
        sale_receipt_id.onchange_add_price()
        sale_receipt_id.proforma_voucher()

class sale_advance_payment_inv_ihr(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    @api.multi
    def create_invoices(self):
        res = super(sale_advance_payment_inv_ihr, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        invoice_ids = sale_orders.mapped('invoice_ids')
        invoice_ids.action_invoice_open()
        for sale_id in sale_orders:
            if len(sale_id.invoice_ids) == 1:
                if sale_id.invoice_ids.invoice_line_ids:
                    sale_id.invoice_ids.invoice_line_ids[0].write({
                    'tong_phu_thu': sale_id.tong_phu_thu,
                    'tong_giam_tru': sale_id.tong_giam_tru,
                })
        return res

class du_toan_sale_order(models.Model):
    _name = 'du.toan.sale.order'

    name = fields.Many2one('product.category', string="Mục phục vụ")
    partner_id = fields.Many2one('res.partner', string="Nhà cung cấp", domain=[('supplier', '=', True)])
    chi_tiet = fields.Many2one('product.product', string="Chi tiết", domain=[('type_service', '!=', 'tour')])
    so_luong = fields.Integer(string="Số lượng")
    so_pax = fields.Integer(string="Số Đêm")
    don_gia = fields.Float(string="Đơn giá")
    sale_price = fields.Float(string="Sale", compute="get_sale_price", store=True)
    note = fields.Text(string='Ghi chú')
    du_toan_sale_order_id = fields.Many2one('sale.order')


    @api.depends('so_pax', 'so_luong', 'don_gia')
    def get_sale_price(self):
        for rec in self:
            rec.sale_price = rec.so_pax * rec.don_gia * rec.so_luong

    @api.model
    def create(self, vals):
        res = super(du_toan_sale_order, self).create(vals)
        if 'from_purchase_tour' not in self._context:
            purchase_tour_ids = self.env['purchase.tour'].search([('sale_order_tour', '=', res.du_toan_sale_order_id.id)])
            for purchase_tour_id in purchase_tour_ids:
                self.env['detail.purchase.tyc'].with_context(from_sale_order=True).create({
                    'name': res.name.id,
                    'partner_id': res.partner_id.id,
                    'so_luong': res.so_luong,
                    'so_pax': res.so_pax,
                    'note': res.note,
                    'purchase_tour_id': purchase_tour_id.id,
                    'chi_tiet': res.chi_tiet.id,
                    'du_toan_so_line_id' : res.id
                })
        return res

    @api.multi
    def write(self, vals):
        res = super(du_toan_sale_order, self).write(vals)
        if 'from_purchase_tour' not in self._context:
            for rec in self:
                detail_purchase_tyc_ids = self.env['detail.purchase.tyc'].search([('du_toan_so_line_id', '=', rec.id)])
                if detail_purchase_tyc_ids:
                    detail_purchase_tyc_ids.with_context(from_sale_order=True).write({
                        'name': rec.name.id,
                        'partner_id': rec.partner_id.id,
                        'chi_tiet': rec.chi_tiet.id,
                        'so_luong': rec.so_luong,
                        'so_pax': rec.so_pax,
                        'don_gia': rec.don_gia,
                        'note': rec.note,
                        'don_gia' : rec.don_gia
                    })
        return res

    @api.multi
    def unlink(self):
        for rec in self:
            if 'from_purchase_tour' not in self._context:
                detail_purchase_tyc_ids = self.env['detail.purchase.tyc'].search([('du_toan_so_line_id', '=', rec.id)])
                if detail_purchase_tyc_ids:
                    detail_purchase_tyc_ids.with_context(from_sale_order=True).unlink()

        res = super(du_toan_sale_order, self).unlink()
        return res



