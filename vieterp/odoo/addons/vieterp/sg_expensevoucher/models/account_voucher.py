# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    account_id = fields.Many2one('account.account', 'Bank/Cash Account',
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        domain="[('deprecated', '=', False), ('internal_type','=', (pay_now == 'pay_now' and 'liquidity' or voucher_type == 'purchase' and 'payable' or 'receivable'))]")
    pay_now = fields.Selection([
            ('pay_now', 'Pay Directly'),
        ], 'Payment', index=True, readonly=True, states={'draft': [('readonly', False)]}, default='pay_now')

AccountVoucher()

class accountvoucherline(models.Model):
    _inherit='account.voucher.line'

    @api.onchange('product_id')
    def onchange_product(self):
        if self.product_id.default_code:
            self.name = self.product_id.default_code
        else:
            self.name = self.product_id.name

    @api.onchange('product_id')
    def onchange_product_account(self):
        if self.voucher_id.voucher_type == 'sale' and self.product_id.categ_id.property_account_income_categ_id:
            self.account_id = self.product_id.categ_id.property_account_income_categ_id.id

        if self.voucher_id.voucher_type == 'purchase' and self.product_id.categ_id.property_account_expense_categ_id:
            self.account_id = self.product_id.categ_id.property_account_expense_categ_id.id

accountvoucherline()