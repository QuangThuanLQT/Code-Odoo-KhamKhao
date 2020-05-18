# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class account_voucher_purchase(models.Model):
    _name = 'account.voucher.purchase'

    def get_account_id_331(self):
        account_id_331 = self.env['account.account'].search([('code', '=', 331)], limit=1)
        if account_id_331:
            return account_id_331.id

    account_id = fields.Many2one('account.account', string="Tài khoản", default=get_account_id_331, required = 1)
    purchase_order_id = fields.Many2one('purchase.order',string="Mã đơn hàng")
    invoice = fields.Many2one('account.invoice',string="Hoá đơn")
    invoice_line_id = fields.Many2one('account.voucher')
    amount_collected = fields.Float(string="Số tiền đã thu")
    amount_receivable = fields.Float(string="Số Tiền")
    amount_total = fields.Float(string="Tổng tiền")
    residual = fields.Float(string="Số tiền còn lại")
    date_invoice = fields.Date(string='Ngày')

class purchase_receipt_inherit(models.Model):
    _inherit = 'account.voucher'

    invoice_purchase_line = fields.One2many('account.voucher.purchase', 'invoice_line_id')
    add_price_purchase = fields.Float(string="Số tiền",states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]})
    so_tien_thua_purchase = fields.Float(string="Số tiền thừa",compute="compute_so_tien_thua_purchase")

    @api.onchange('partner_id')
    def onchange_partner_id_purchase(self):
        if self.partner_id:
            self.invoice_purchase_line = []
            invoice_ids = self.env['account.invoice'].search([
                ('type', 'in', ('in_invoice', 'in_refund')),
                ('partner_id', '=', self.partner_id.id),
                ('state', '=', 'open'),
            ])
            for invoice_id in invoice_ids:
                account_id_331 = self.env['account.account'].search([('code', '=', 331)], limit=1)
                source_purchase_id = self.env['purchase.order'].search([('name', '=', invoice_id.origin)])
                if invoice_id.invoice_line_ids and invoice_id.invoice_line_ids[0].purchase_id:
                    source_purchase_id = invoice_id.invoice_line_ids[0].purchase_id
                self.invoice_purchase_line += self.invoice_purchase_line.new({
                    'invoice': invoice_id.id,
                    'residual': invoice_id.residual,
                    'purchase_order_id': source_purchase_id.id,
                    'amount_collected': invoice_id.amount_total - invoice_id.residual,
                    'amount_total': invoice_id.amount_total,
                    'date_invoice': invoice_id.date_invoice,
                    'account_id' : account_id_331.id or False
                })

    @api.onchange('add_price_purchase')
    def onchange_add_price_purchase(self):
        total = self.add_price_purchase or 0
        for invoice_line_id in self.invoice_purchase_line:
            if total >= invoice_line_id.residual:
                invoice_line_id.amount_receivable = invoice_line_id.residual
                total = total - invoice_line_id.residual
            else:
                invoice_line_id.amount_receivable = total
                total = 0

    @api.multi
    @api.depends('tax_correction', 'line_ids.price_subtotal', 'add_price_purchase')
    def _compute_total(self):
        for voucher in self:
            if voucher.add_price_purchase:
                voucher.amount = voucher.add_price_purchase
                voucher.tax_amount = 0
            else:
                super(purchase_receipt_inherit, self)._compute_total()

    @api.multi
    @api.onchange('add_price_purchase', 'invoice_purchase_line')
    def compute_so_tien_thua_purchase(self):
        for rec in self:
            total = 0
            for invoice_line_id in rec.invoice_purchase_line:
                total += invoice_line_id.amount_receivable

            rec.so_tien_thua_purchase = rec.add_price_purchase - total
    @api.multi
    def voucher_move_line_create(self, line_total, move_id, company_currency, current_currency):
        res = super(purchase_receipt_inherit, self).voucher_move_line_create(line_total, move_id, company_currency,
                                                                         current_currency)
        for rec in self:
            for line in rec.invoice_purchase_line:
                move_line = {
                    'journal_id': rec.journal_id.id,
                    'name': '/',
                    'account_id': line.account_id.id,
                    'move_id': move_id,
                    'partner_id': rec.partner_id.commercial_partner_id.id,
                    'quantity': 1,
                    'credit': 0,
                    'debit': line.amount_receivable,
                    'date': rec.account_date,
                    'amount_currency': 0.0,
                    'currency_id': company_currency != current_currency and current_currency or False,
                    'payment_id': rec._context.get('payment_id'),
                    'voucher_invoice_id': line.invoice.id
                }
                self.env['account.move.line'].with_context(apply_taxes=True).create(move_line)

            if rec.so_tien_thua_purchase:
                move_line = {
                    'journal_id': rec.journal_id.id,
                    'name': '/',
                    'account_id': line.account_id.id,
                    'move_id': move_id,
                    'partner_id': rec.partner_id.commercial_partner_id.id,
                    'quantity': 1,
                    'credit': rec.so_tien_thua_purchase,
                    'debit': 0,
                    'date': rec.account_date,
                    'amount_currency': 0.0,
                    'currency_id': company_currency != current_currency and current_currency or False,
                    'payment_id': rec._context.get('payment_id'),
                }
                self.env['account.move.line'].with_context(apply_taxes=True).create(move_line)
        return res