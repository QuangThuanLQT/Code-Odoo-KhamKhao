# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class tour_manager(models.Model):
    _name = 'tour.manager'

    @api.model
    def get_sale_order_data(self, start_date, end_date):
        dashboard_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        dashboard_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        sale_order = self.env['sale.order'].search([('state', 'not in', ('draft', 'sent', 'cancel')),('start_date','>=',dashboard_start_date),('end_date','<=',dashboard_end_date),('is_tour_booking', '=', True)])
        sale_order_tour_ghep = self.env['sale.order'].search([('state', 'not in', ('draft', 'sent', 'cancel')),('start_date','>=',dashboard_start_date),('end_date','<=',dashboard_end_date)
                                                                 ,('tour_type','=','tour_ghep'),('is_tour_booking', '=', True)])
        sale_order_tour_tyc = self.env['sale.order'].search(
            [('state', 'not in', ('draft', 'sent', 'cancel')), ('start_date', '>=', dashboard_start_date),
             ('end_date', '<=', dashboard_end_date), ('tour_type', '=', 'tour_tyc'),('is_tour_booking', '=', True)])

        sale_order_tour_spk = self.env['sale.order'].search(
            [('state', 'not in', ('draft', 'sent', 'cancel')), ('start_date', '>=', dashboard_start_date),
             ('end_date', '<=', dashboard_end_date), ('is_tour_booking', '=', False)])

        purchase_tour = self.env['purchase.tour'].search([('start_date','>=',dashboard_start_date),('end_date','<=',dashboard_end_date)])
        purchase_tour_ghep = self.env['purchase.tour'].search([('start_date','>=',dashboard_start_date),('end_date','<=',dashboard_end_date),('tour_type','=','tour_ghep')])
        purchase_tour_tyc = self.env['purchase.tour'].search([('start_date','>=',dashboard_start_date),('end_date','<=',dashboard_end_date),('tour_type','=','tour_tyc')])
        chi_phi = sum(purchase_tour.mapped('tong_thuc_te'))+ sum(purchase_tour.mapped('tong_dieu_hanh'))
        loi_nhuan = sum(sale_order.mapped('amount_total')) - chi_phi
        ke_toan_thu = sum(purchase_tour.mapped('tong_thuc_te')) - sum(purchase_tour.mapped('tong_hdv_thu'))

        hoa_don_ban_hang = self.env['account.invoice'].search([('type','in',('out_invoice', 'out_refund')),('date_invoice','>=',dashboard_start_date),('date_invoice','<=',dashboard_end_date)])
        hoa_don_mua_hang = self.env['account.invoice'].search([('type','in',('in_invoice', 'in_refund')),('date_invoice','>=',dashboard_start_date),('date_invoice','<=',dashboard_end_date)])


        return [{
            'tong_don_ban': len(sale_order),
            'tong_don_tour_ghep': len(sale_order_tour_ghep),
            'tong_don_tour_tyc': len(sale_order_tour_tyc),
            'tong_don_spk': len(sale_order_tour_spk),
            'tong_doanh_thu': "%s đ" % ('{:,}'.format(int(sum(sale_order.mapped('amount_total'))))),
            'tong_dieu_hanh': len(purchase_tour),
            'tong_dieu_hanh_ghep': len(purchase_tour_ghep),
            'tong_dieu_hanh_tyc': len(purchase_tour_tyc),
            'tong_chi_phi': "%s đ" % ('{:,}'.format(int(chi_phi))),
            'tong_loi_nhuan': "%s đ" % ('{:,}'.format(int(loi_nhuan))),
            'tong_hoa_don_ban_hang': len(hoa_don_ban_hang),
            'tong_hoa_don_mua_hang': len(hoa_don_mua_hang),
            'tong_hdv_thu': "%s đ" % ('{:,}'.format(int(sum(purchase_tour.mapped('tong_hdv_thu'))))),
            'tong_ke_toan_thu': "%s đ" % ('{:,}'.format(int(ke_toan_thu))),
        }]

