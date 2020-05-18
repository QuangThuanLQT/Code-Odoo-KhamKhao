# -*- coding: utf-8 -*-

from odoo import models, fields, api

class purchase_order_line(models.Model):
    _inherit = 'account.invoice.line'

    so_pax = fields.Float(string="Số pax(đêm)")
    phu_thu = fields.Float(string="Phụ thu")
    tong_phu_thu = fields.Float(string="Tổng phụ thu")
    tong_giam_tru = fields.Float(string="Tổng giảm trừ")

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date','tong_phu_thu','tong_giam_tru')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id,
                                                          partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] + self.tong_phu_thu - self.tong_giam_tru if taxes  else self.quantity * price + self.tong_phu_thu - self.tong_giam_tru
        if self.invoice_id.currency_id and self.invoice_id.company_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(
                date=self.invoice_id._get_currency_rate_date()).compute(price_subtotal_signed,
                                                                        self.invoice_id.company_id.currency_id)
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign

class account_invoice_ihr(models.Model):
    _inherit = 'account.invoice'


    def _prepare_invoice_line_from_po_line(self, line):
        data = super(account_invoice_ihr, self)._prepare_invoice_line_from_po_line(line)
        data.update({
            'so_pax': line.so_pax,
            'phu_thu': line.phu_thu
        })
        return data






