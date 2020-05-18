# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api

class vieterp_sale_quotation(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def write(self, vals):
        product_list_ext = []
        product_list_new = []
        if "order_line" in vals.keys():
            new_list = vals['order_line']
            pro_list = []
            for att in new_list:
                if att[0] == 4:
                    s = self.order_line.browse(att[1])
                    if s.product_id and s.product_id.id not in product_list_ext:
                        product_list_ext.append(s.product_id.id)
                if att[0] == 1:
                    s = self.order_line.browse(att[1])
                    if s.product_id and s.product_id.id not in product_list_ext:
                        product_list_ext.append(s.product_id.id)
                if att[0] == 0:
                    if att[2]['product_id'] not in product_list_new:
                        product_list_new.append(att[2]['product_id'])
            if not product_list_ext and self.order_line:
                for line in self.order_line:
                    if line.product_id.id and line.product_id.id not in product_list_ext:
                        product_list_ext.append(line.product_id.id)
            for obj in product_list_new:
                pro_qty = 0
                if obj in product_list_ext:
                    for att in new_list:
                        if att[0] == 4:
                            o = self.order_line.browse(att[1])
                            if o.product_id.id == obj:
                                pro_qty += o.product_uom_qty
                        if att[0] == 1:
                            o = self.order_line.browse(att[1])
                            if o.product_id.id == obj:
                                pro_qty += att[2].get('product_uom_qty', False) or 1
                        if att[1] == 0:
                            if att[2] and att[2]['product_id'] == obj:
                                pro_qty += att[2].get('product_uom_qty', False) or 1
                                if self.order_line:
                                    for line in self.order_line:
                                        if (line.product_id and line.product_id.id == obj) and att[2].get(
                                                'product_uom_qty') == None:
                                            pro_qty += line.product_uom_qty

                    for att1 in new_list:
                        if att1[0] == 4:
                            o = self.order_line.browse(att1[1])
                            if o.product_id.id == obj:
                                o.product_uom_qty = pro_qty
                                # o.product_uos_qty = pro_qty
                        if att1[0] == 1:
                            o = self.order_line.browse(att1[1])
                            if o.product_id.id == obj:
                                att1[2]['product_uom_qty'] = pro_qty
                                o.product_uom_qty = pro_qty
                        if att1[0] == 0 and self:
                            for line in self.order_line:
                                if line.product_id and line.product_id.id == obj:
                                    line.product_uom_qty = pro_qty
                                    # line.product_uos_qty = pro_qty
            for obj1 in product_list_new:
                pro_qty = 0
                count = 0
                if obj1 not in product_list_ext:
                    for att1 in new_list:
                        if att1[0] == 0:
                            if att1[2]['product_id'] == obj1:
                                pro_qty += att1[2].get('product_uom_qty') if 'product_uom_qty' in att1[2] else 1
                    for att2 in new_list:
                        if att2[0] == 0:
                            if att2[2]['product_id'] == obj1:
                                count += 1
                                if count == 1:
                                    att2[2]['product_uom_qty'] = pro_qty
                                    pro_list.append(att2)

            for obj2 in product_list_ext:
                if obj2 not in product_list_new:
                    for att2 in new_list:
                        if att2[0] == 4:
                            o = self.order_line.browse(att2[1])
                            if o.product_id.id == obj2:
                                pro_list.append(att2)
            for att3 in new_list:
                if att3[0] == 2:
                    pro_list.append(att3)
                if att3[0] == 1:
                    check = False
                    if att3[2].get('product_id', False):
                        for line in pro_list:
                            o = self.order_line.browse(line[1])
                            if o.product_id.id == att3[2].get('product_id'):
                                o.product_uom_qty += att3[2].get('product_uom_qty') or self.order_line.browse(
                                    att3[1]).product_uom_qty
                                new_line = att3
                                new_line[0] = 2
                                pro_list.append(new_line)
                                check = True
                    if not check:
                        pro_list.append(att3)

            vals['order_line'] = pro_list
        res = super(vieterp_sale_quotation, self).write(vals)

        return res



class product_multi_select(models.TransientModel):
    _name = 'product.multi.select.quotation'

    product_ids = fields.Many2many('product.product', string='Products')


    @api.multi
    def add_product_to_line(self):
        for record in self:
            if 'active_id' in self.env.context:
                sales_order_id = self.env['sale.order'].search([('id', '=', self.env.context.get('active_id'))])
                list_product = []
                for product in record.product_ids:
                    list_product.append((0, 0, {
                        'product_id': product.id,
                        'product_uom': product.uom_id.id
                    }))
                sales_order_id.write({
                    'order_line': list_product
                })
