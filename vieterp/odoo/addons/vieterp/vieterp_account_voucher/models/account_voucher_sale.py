# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class account_voucher_sale(models.Model):
    _name = 'account.voucher.sale'

    def get_account_id_131(self):
        account_id_131 = self.env['account.account'].search([('code', '=', 131)], limit=1)
        if account_id_131:
            return account_id_131.id

    account_id = fields.Many2one('account.account', string="Tài khoản", default=get_account_id_131, required = 1)
    sale_order_id = fields.Many2one('sale.order',string="Mã đơn hàng")
    invoice = fields.Many2one('account.invoice',string="Hoá đơn")
    invoice_line_id = fields.Many2one('account.voucher')
    amount_collected = fields.Float(string="Số tiền đã thu")
    amount_receivable = fields.Float(string="Số tiền thanh toán")
    amount_total = fields.Float(string="Tổng tiền ban đầu")
    residual = fields.Float(string="Số tiền còn phải thu")
    date_invoice = fields.Date(string='Ngày')



class sale_receipt_inherit(models.Model):
    _inherit = 'account.voucher'

    invoice_line = fields.One2many('account.voucher.sale', 'invoice_line_id')
    add_price = fields.Float(string="Số tiền",states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]})
    so_tien_thua = fields.Float(string="Số tiền thừa", compute="_compute_so_tien_thua")
    pay_now = fields.Selection(default='pay_now')

    @api.onchange('payment_journal_id')
    def onchange_payment_journal_id(self):
        for voucher in self:
            if voucher.pay_now == 'pay_now':
                if voucher.voucher_type == 'sale':
                    voucher.account_id = voucher.payment_journal_id.default_debit_account_id
                else:
                    voucher.account_id = voucher.payment_journal_id.default_credit_account_id


    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.invoice_line = []
            invoice_ids = self.env['account.invoice'].search([
                ('type','in',('out_invoice', 'out_refund')),
                ('partner_id', '=', self.partner_id.id),
                ('state', '=', 'open'),
            ])
            for invoice_id in invoice_ids:
                account_id_131 = self.env['account.account'].search([('code', '=', 131)], limit=1)
                order_id = self.env['sale.order'].search([('name', '=', invoice_id.origin)])
                if invoice_id.invoice_line_ids and invoice_id.invoice_line_ids[0].sale_line_ids:
                    order_id = invoice_id.invoice_line_ids[0].sale_line_ids[0].order_id
                self.invoice_line += self.invoice_line.new({
                    'invoice' : invoice_id.id,
                    'residual' : invoice_id.residual,
                    'sale_order_id' : order_id.id,
                    'amount_collected' : invoice_id.amount_total - invoice_id.residual,
                    'amount_total' : invoice_id.amount_total,
                    'date_invoice' : invoice_id.date_invoice,
                    'account_id' : account_id_131.id or False
                })

    @api.onchange('add_price')
    def onchange_add_price(self):
        total = self.add_price or 0
        for invoice_line_id in self.invoice_line:
            if total >= invoice_line_id.residual:
                invoice_line_id.amount_receivable = invoice_line_id.residual
                total = total - invoice_line_id.residual
            else:
                invoice_line_id.amount_receivable = total
                total = 0

    @api.multi
    @api.depends('tax_correction', 'line_ids.price_subtotal', 'add_price')
    def _compute_total(self):
        for voucher in self:
            if voucher.add_price:
                voucher.amount = voucher.add_price
                voucher.tax_amount = 0
            else:
                super(sale_receipt_inherit, self)._compute_total()

    @api.multi
    @api.onchange('add_price','invoice_line')
    def _compute_so_tien_thua(self):
        for rec in self:
            total = 0
            for invoice_line_id in rec.invoice_line:
                total += invoice_line_id.amount_receivable

            rec.so_tien_thua = rec.add_price - total

    @api.multi
    def voucher_move_line_create(self, line_total, move_id, company_currency, current_currency):
        res = super(sale_receipt_inherit, self).voucher_move_line_create(line_total, move_id, company_currency, current_currency)
        for rec in self:
            for line in rec.invoice_line:
                if line.amount_receivable:
                    move_line = {
                        'journal_id': rec.journal_id.id,
                        'name': '/',
                        'account_id': line.account_id.id,
                        'move_id': move_id,
                        'partner_id': rec.partner_id.commercial_partner_id.id,
                        'quantity': 1,
                        'credit': line.amount_receivable,
                        'debit': 0,
                        'date': rec.account_date,
                        'amount_currency': 0.0,
                        'currency_id': company_currency != current_currency and current_currency or False,
                        'payment_id': rec._context.get('payment_id'),
                        'voucher_invoice_id' : line.invoice.id
                    }
                    self.env['account.move.line'].with_context(apply_taxes=True).create(move_line)

            if rec.so_tien_thua:
                move_line = {
                    'journal_id': rec.journal_id.id,
                    'name': '/',
                    'account_id': line.account_id.id,
                    'move_id': move_id,
                    'partner_id': rec.partner_id.commercial_partner_id.id,
                    'quantity': 1,
                    'credit': rec.so_tien_thua,
                    'debit': 0,
                    'date': rec.account_date,
                    'amount_currency': 0.0,
                    'currency_id': company_currency != current_currency and current_currency or False,
                    'payment_id': rec._context.get('payment_id'),
                }
                self.env['account.move.line'].with_context(apply_taxes=True).create(move_line)
        return res

    @api.multi
    def proforma_voucher(self):
        super(sale_receipt_inherit, self).proforma_voucher()
        for rec in self:
            if rec.move_id:
                for line in rec.move_id.line_ids:
                    if line.voucher_invoice_id:
                        line.voucher_invoice_id.assign_outstanding_credit(line.id)





