# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api
import StringIO
import xlsxwriter


class bao_cao_tour(models.Model):
    _name = 'bao.cao.tour'

    start_date = fields.Date(string="Ngày bắt đầu")
    end_date = fields.Date(string="Ngày kết thúc")
    user_id = fields.Many2many('res.users',string="Nhân viên bán hàng")
    report_tour_land_id = fields.One2many('report.tour.land','bao_cao_tour_id')
    count_report_land = fields.Float()
    report_tour_ghep_id = fields.One2many('report.tour.ghep', 'bao_cao_tour_id')
    count_report_ghep = fields.Float()
    report_tour_xe_id = fields.One2many('report.tour.xe', 'bao_cao_tour_id')
    count_report_xe = fields.Float()
    report_tour_ba_na_id = fields.One2many('report.tour.ba.na', 'bao_cao_tour_id')
    count_report_ba_na = fields.Float()
    report_tour_ve_bn_id = fields.One2many('report.tour.ve.bn', 'bao_cao_tour_id')
    count_report_ve_bn = fields.Float()

    tong_cong_xe = fields.Float(string="Tổng Cộng")
    tong_hdv_xe = fields.Float(string="Tổng HDV Thu")
    tong_tm_xe = fields.Float(string="Tổng TM")
    tong_ck_xe = fields.Float(string="Tổng CK")
    tong_con_du_xe = fields.Float(string="Tổng Còn Dư")
    tong_con_no_xe = fields.Float(string="Tổng Còn Nợ")

    tong_cong_land = fields.Float(string="Tổng Cộng")
    tong_hdv_land = fields.Float(string="Tổng HDV Thu")
    tong_tm_land = fields.Float(string="Tổng TM")
    tong_ck_land = fields.Float(string="Tổng CK")
    tong_con_du_land = fields.Float(string="Tổng Còn Dư")
    tong_con_no_land = fields.Float(string="Tổng Còn Nợ")

    tong_cong_ghep = fields.Float(string="Tổng Cộng")
    tong_hdv_ghep = fields.Float(string="Tổng HDV Thu")
    tong_tm_ghep = fields.Float(string="Tổng TM")
    tong_ck_ghep = fields.Float(string="Tổng CK")
    tong_con_du_ghep = fields.Float(string="Tổng Còn Dư")
    tong_con_no_ghep = fields.Float(string="Tổng Còn Nợ")

    tong_cong_ba_na = fields.Float(string="Tổng Cộng")
    tong_hdv_ba_na = fields.Float(string="Tổng HDV Thu")
    tong_tm_ba_na = fields.Float(string="Tổng TM")
    tong_ck_ba_na = fields.Float(string="Tổng CK")
    tong_con_du_ba_na = fields.Float(string="Tổng Còn Dư")
    tong_con_no_ba_na = fields.Float(string="Tổng Còn Nợ")

    tong_cong_ve_bn = fields.Float(string="Tổng Cộng")
    tong_hdv_ve_bn = fields.Float(string="Tổng HDV Thu")
    tong_tm_ve_bn = fields.Float(string="Tổng TM")
    tong_ck_ve_bn = fields.Float(string="Tổng CK")
    tong_con_du_ve_bn = fields.Float(string="Tổng Còn Dư")
    tong_con_no_ve_bn = fields.Float(string="Tổng Còn Nợ")

    tong_cong_all = fields.Float(string="Tổng Cộng")
    tong_hdv_all = fields.Float(string="Tổng HDV Thu")
    tong_tm_all = fields.Float(string="Tổng TM")
    tong_ck_all = fields.Float(string="Tổng CK")
    tong_con_du_all = fields.Float(string="Tổng Còn Dư")
    tong_con_no_all = fields.Float(string="Tổng Còn Nợ")

    count_report_all = fields.Float()

    check_boolean = fields.Boolean(default=True)
    check_boolean_tour_ghep = fields.Boolean(default=True)
    check_boolean_tour_tyc = fields.Boolean(default=True)
    check_boolean_spk = fields.Boolean(default=True)

    @api.onchange('start_date','end_date','user_id')
    def onchange_bc(self):
        domain = [('start_date', '>=', self.start_date),('state', 'not in', ('draft', 'sent', 'cancel'))]
        if self.end_date:
            domain.append(('end_date', '<=', self.end_date))
        if self.user_id:
            domain.append(('user_id', 'in', self.user_id.ids))
        sale_order_ids = self.env['sale.order'].search(domain)

        sale_order_xe_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids), ('type_san_pham_khac', '=', self.env.ref('vieterp_sale_tour.xe').id)])
        sale_order_ba_na_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids), ('type_san_pham_khac', '=', self.env.ref('vieterp_sale_tour.ba_na').id)])
        sale_order_ve_ba_na_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids), ('type_san_pham_khac', '=', self.env.ref('vieterp_sale_tour.ve_ba_na').id)])
        sale_order_land_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids), ('tour_type', '=', 'tour_tyc')])
        sale_order_ghep_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids), ('tour_type', '=', 'tour_ghep')])

        sum_amount_xe = 0; ck_xe = 0; tm_xe = 0; hdv_thu_xe = 0; sum_con_du_xe = 0; sum_con_no_xe = 0
        sum_amount_land = 0; ck_land = 0; tm_land = 0; hdv_thu_land = 0; sum_con_du_land = 0; sum_con_no_land = 0
        sum_amount_ghep = 0; ck_ghep = 0; tm_ghep = 0; hdv_thu_ghep = 0; sum_con_du_ghep = 0; sum_con_no_ghep = 0
        sum_amount_ba_na = 0; ck_ba_na = 0; tm_ba_na = 0; hdv_thu_ba_na = 0; sum_con_du_ba_na = 0; sum_con_no_ba_na = 0
        sum_amount_ve_bn = 0; ck_ve_bn = 0; tm_ve_bn = 0; hdv_thu_ve_bn = 0; sum_con_du_ve_bn = 0; sum_con_no_ve_bn = 0

        self.report_tour_xe_id = []
        for sale_order_xe_id in sale_order_xe_ids:
            cash = 0; bank = 0; con_du = 0; con_no = 0; sum = 0

            for order_line in sale_order_xe_id.order_line:
                sum += order_line.product_uom_qty
            invoices = sale_order_xe_id.mapped('invoice_ids')
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_xe_id.thu_ho

            if sale_order_xe_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_xe_id.amount_total - cash - bank)
            else:
                con_no = sale_order_xe_id.amount_total - cash - bank

            sum_amount_xe += sale_order_xe_id.amount_total
            ck_xe += bank
            tm_xe += cash_tm
            hdv_thu_xe += sale_order_xe_id.thu_ho
            sum_con_du_xe += con_du
            sum_con_no_xe += con_no

            new_line = self.report_tour_xe_id.new({
                'user_id': sale_order_xe_id.user_id.id,
                'partner_id': sale_order_xe_id.partner_id.id,
                'code_dh': sale_order_xe_id.name,
                'code_sale': sale_order_xe_id.id,
                'sl': sum,
                'tong_tien': sale_order_xe_id.amount_total,
                'hdv_thu': sale_order_xe_id.thu_ho,
                'tm': cash_tm,
                'ck': bank,
                'con_du': con_du,
                'con_no': con_no,
                'chi_tiet_tt': sale_order_xe_id.ghi_chu
            })
            self.report_tour_xe_id += new_line

        self.report_tour_land_id = []
        for sale_order_land_id in sale_order_land_ids:
            cash = 0; bank = 0; con_du = 0; con_no = 0; sum = 0

            for order_line in sale_order_land_id.order_line:
                sum += order_line.product_uom_qty
            invoices = sale_order_land_id.mapped('invoice_ids')
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_land_id.thu_ho

            if sale_order_land_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_land_id.amount_total - cash - bank)
            else:
                con_no = sale_order_land_id.amount_total - cash - bank

            sum_amount_land += sale_order_land_id.amount_total
            ck_land += bank
            tm_land += cash_tm
            hdv_thu_land += sale_order_land_id.thu_ho
            sum_con_du_land += con_du
            sum_con_no_land += con_no

            new_line = self.report_tour_land_id.new({
                'user_id': sale_order_land_id.user_id.id,
                'partner_id' : sale_order_land_id.partner_id.id,
                'code_dh': sale_order_land_id.name,
                'code_sale': sale_order_land_id.id,
                'sl': sum,
                'tong_tien' : sale_order_land_id.amount_total,
                'hdv_thu': sale_order_land_id.thu_ho,
                'tm': cash_tm,
                'ck': bank,
                'con_du': con_du,
                'con_no': con_no,
                'chi_tiet_tt': sale_order_land_id.ghi_chu
            })
            self.report_tour_land_id += new_line

        self.report_tour_ghep_id = []
        for sale_order_ghep_id in sale_order_ghep_ids:
            cash = 0; bank = 0; con_du = 0; con_no = 0; sum = 0

            for order_line in sale_order_ghep_id.order_line:
                sum += order_line.product_uom_qty
            invoices = sale_order_ghep_id.mapped('invoice_ids')
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_ghep_id.thu_ho

            if sale_order_ghep_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_ghep_id.amount_total - cash - bank)
            else:
                con_no = sale_order_ghep_id.amount_total - cash - bank

            sum_amount_ghep += sale_order_ghep_id.amount_total
            ck_ghep += bank
            tm_ghep += cash_tm
            hdv_thu_ghep += sale_order_ghep_id.thu_ho
            sum_con_du_ghep += con_du
            sum_con_no_ghep += con_no

            new_line = self.report_tour_ghep_id.new({
                'user_id': sale_order_ghep_id.user_id.id,
                'partner_id': sale_order_ghep_id.partner_id.id,
                'code_dh': sale_order_ghep_id.name,
                'code_sale': sale_order_ghep_id.id,
                'sl': sum,
                'tong_tien': sale_order_ghep_id.amount_total,
                'hdv_thu': sale_order_ghep_id.thu_ho,
                'tm': cash_tm,
                'ck': bank,
                'con_du': con_du,
                'con_no': con_no,
                'chi_tiet_tt': sale_order_ghep_id.ghi_chu
            })
            self.report_tour_ghep_id += new_line

        self.report_tour_ba_na_id = []
        for sale_order_ba_na_id in sale_order_ba_na_ids:
            cash = 0; bank = 0; con_du = 0; con_no = 0; sum = 0

            for order_line in sale_order_ba_na_id.order_line:
                sum += order_line.product_uom_qty
            invoices = sale_order_ba_na_id.mapped('invoice_ids')
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_ba_na_id.thu_ho

            if sale_order_ba_na_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_ba_na_id.amount_total - cash - bank)
            else:
                con_no = sale_order_ba_na_id.amount_total - cash - bank

            sum_amount_ba_na += sale_order_ba_na_id.amount_total
            ck_ba_na += bank
            tm_ba_na += cash_tm
            hdv_thu_ba_na += sale_order_ba_na_id.thu_ho
            sum_con_du_ba_na += con_du
            sum_con_no_ba_na += con_no

            new_line = self.report_tour_ba_na_id.new({
                'user_id': sale_order_ba_na_id.user_id.id,
                'partner_id': sale_order_ba_na_id.partner_id.id,
                'code_dh': sale_order_ba_na_id.name,
                'code_sale': sale_order_ba_na_id.id,
                'sl': sum,
                'tong_tien': sale_order_ba_na_id.amount_total,
                'hdv_thu': sale_order_ba_na_id.thu_ho,
                'tm': cash_tm,
                'ck': bank,
                'con_du': con_du,
                'con_no': con_no,
                'chi_tiet_tt': sale_order_ba_na_id.ghi_chu
            })
            self.report_tour_ba_na_id += new_line

        self.report_tour_ve_bn_id = []
        for sale_order_ve_ba_na_id in sale_order_ve_ba_na_ids:
            cash = 0; bank = 0; con_du = 0; con_no = 0; sum = 0

            for order_line in sale_order_ve_ba_na_id.order_line:
                sum += order_line.product_uom_qty
            invoices = sale_order_ve_ba_na_id.mapped('invoice_ids')
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_ve_ba_na_id.thu_ho

            if sale_order_ve_ba_na_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_ve_ba_na_id.amount_total - cash - bank)
            else:
                con_no = sale_order_ve_ba_na_id.amount_total - cash - bank

            sum_amount_ve_bn += sale_order_ve_ba_na_id.amount_total
            ck_ve_bn += bank
            tm_ve_bn += cash_tm
            hdv_thu_ve_bn += sale_order_ve_ba_na_id.thu_ho
            sum_con_du_ve_bn += con_du
            sum_con_no_ve_bn += con_no

            new_line = self.report_tour_ve_bn_id.new({
                'user_id': sale_order_ve_ba_na_id.user_id.id,
                'partner_id': sale_order_ve_ba_na_id.partner_id.id,
                'code_dh': sale_order_ve_ba_na_id.name,
                'code_sale': sale_order_ve_ba_na_id.id,
                'sl': sum,
                'tong_tien': sale_order_ve_ba_na_id.amount_total,
                'hdv_thu': sale_order_ve_ba_na_id.thu_ho,
                'tm': cash_tm,
                'ck': bank,
                'con_du': con_du,
                'con_no': con_no,
                'chi_tiet_tt': sale_order_ve_ba_na_id.ghi_chu
            })
            self.report_tour_ve_bn_id += new_line

        self.count_report_xe = len(sale_order_xe_ids)
        self.count_report_land = len(sale_order_land_ids)
        self.count_report_ghep = len(sale_order_ghep_ids)
        self.count_report_ba_na = len(sale_order_ba_na_ids)
        self.count_report_ve_bn = len(sale_order_ve_ba_na_ids)
        self.count_report_all = self.count_report_xe + self.count_report_land + self.count_report_ghep + self.count_report_ba_na + self.count_report_ve_bn

        self.tong_cong_xe = sum_amount_xe ; self.tong_hdv_xe = hdv_thu_xe ; self.tong_tm_xe = tm_xe
        self.tong_ck_xe = ck_xe ; self.tong_con_du_xe = sum_con_du_xe ; self.tong_con_no_xe = sum_con_no_xe
        self.tong_cong_land = sum_amount_land ; self.tong_hdv_land = hdv_thu_land ; self.tong_tm_land = tm_land
        self.tong_ck_land = ck_land ; self.tong_con_du_land = sum_con_du_land ; self.tong_con_no_land = sum_con_no_land
        self.tong_cong_ghep = sum_amount_ghep ; self.tong_hdv_ghep = hdv_thu_ghep ; self.tong_tm_ghep = tm_ghep
        self.tong_ck_ghep = ck_ghep ; self.tong_con_du_ghep = sum_con_du_ghep ; self.tong_con_no_ghep = sum_con_no_ghep
        self.tong_cong_ba_na = sum_amount_ba_na ; self.tong_hdv_ba_na = hdv_thu_ba_na ; self.tong_tm_ba_na = tm_ba_na
        self.tong_ck_ba_na = ck_ba_na ; self.tong_con_du_ba_na = sum_con_du_ba_na ; self.tong_con_no_ba_na = sum_con_no_ba_na
        self.tong_cong_ve_bn = sum_amount_ve_bn ; self.tong_hdv_ve_bn = hdv_thu_ve_bn ; self.tong_tm_ve_bn = tm_ve_bn
        self.tong_ck_ve_bn = ck_ve_bn ; self.tong_con_du_ve_bn = sum_con_du_ve_bn ; self.tong_con_no_ve_bn = sum_con_no_ve_bn

        self.tong_cong_all = self.tong_cong_xe + self.tong_cong_land + self.tong_cong_ghep + self.tong_cong_ba_na + self.tong_cong_ve_bn
        self.tong_hdv_all = self.tong_hdv_xe + self.tong_hdv_land + self.tong_hdv_ghep + self.tong_hdv_ba_na + self.tong_hdv_ve_bn
        self.tong_tm_all = self.tong_tm_xe + self.tong_tm_land + self.tong_tm_ghep + self.tong_tm_ba_na + self.tong_tm_ve_bn
        self.tong_ck_all = self.tong_ck_xe + self.tong_ck_land + self.tong_ck_ghep + self.tong_ck_ba_na + self.tong_ck_ve_bn
        self.tong_con_du_all = self.tong_con_du_xe + self.tong_con_du_land + self.tong_con_du_ghep + self.tong_con_du_ba_na + self.tong_con_du_ve_bn
        self.tong_con_no_all = self.tong_con_no_xe + self.tong_con_no_land + self.tong_con_no_ghep + self.tong_con_no_ba_na + self.tong_con_no_ve_bn

    @api.multi
    def print_sale_order_excel(self):
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Báo cáo doanh thu')

        body_bold_color = workbook.add_format(
            {'bold': True, 'font_size': '12', 'align': 'left', 'valign': 'vcenter' ,'border': 1,})
        text_style = workbook.add_format(
            {'bold': True, 'font_size': '12', 'align': 'center', 'valign': 'vcenter', 'border': 1,})
        body_bold_color_number = workbook.add_format(
            {'bold': False, 'font_size': '11', 'align': 'left', 'valign': 'vcenter' ,'border': 1,})
        body_bold_color_number.set_num_format('#,##0')
        body_l = workbook.add_format({
            'border': 1,
        })
        money_sum = workbook.add_format({
            'num_format': '#,##0',
            'bold': True,
            'font_size': '12',
            'border': 1,
        })
        money = workbook.add_format({
            'num_format': '#,##0',
            'border': 1,
        })

        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 28)
        worksheet.set_column('K:K', 16)
        worksheet.set_column('L:L', 16)
        worksheet.set_column('M:M', 35)
        worksheet.set_column('F:R', 16)
        summary_header = ['DV','Nhân viên bán hàng','Đối tác', 'Code ĐH', 'Code Sale', 'SL',
                          'Tổng tiền', 'HDV Thu', 'TM', 'CK', 'Còn dư','Còn nợ','Chi tiết thanh toán']

        row = 0
        [worksheet.write(row, header_cell, unicode(summary_header[header_cell], "utf-8"), body_bold_color) for
         header_cell in range(0, len(summary_header)) if summary_header[header_cell]]


        sale_order_ids = self.env['sale.order'].search(
            [('confirmation_date', '>=', self.start_date), ('confirmation_date', '<=', self.end_date),
             ('user_id', 'in', self.user_id.ids)])

        sale_order_xe_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids),('type_san_pham_khac','=', self.env.ref('vieterp_sale_tour.xe').id)])
        sale_order_ba_na_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids), ('type_san_pham_khac', '=', self.env.ref('vieterp_sale_tour.ba_na').id)])
        sale_order_ve_ba_na_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids), ('type_san_pham_khac', '=', self.env.ref('vieterp_sale_tour.ve_ba_na').id)])
        sale_order_land_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids), ('tour_type', '=', 'tour_tyc')])
        sale_order_ghep_ids = self.env['sale.order'].search([('id', 'in', sale_order_ids.ids), ('tour_type', '=', 'tour_ghep')])

        row += 1
        f = row
        worksheet.merge_range('B%s:F%s' % (row + 1, row + 1), 'Tổng DT Xe',text_style)

        sum_amount_xe = 0 ; ck_xe = 0 ; tm_xe = 0 ; hdv_thu_xe = 0 ; sum_con_du_xe = 0 ; sum_con_no_xe = 0

        for sale_order_xe_id in sale_order_xe_ids:
            row += 1

            invoices = sale_order_xe_id.mapped('invoice_ids')
            cash = 0
            bank = 0
            con_du = 0
            con_no = 0
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_xe_id.thu_ho

            if sale_order_xe_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_xe_id.amount_total - cash - bank)
            else:
                con_no = sale_order_xe_id.amount_total - cash - bank

            sum = 0
            for order_line in sale_order_xe_id.order_line:
                sum += order_line.product_uom_qty

            sum_amount_xe += sale_order_xe_id.amount_total
            ck_xe += bank
            tm_xe += cash_tm
            hdv_thu_xe += sale_order_xe_id.thu_ho
            sum_con_du_xe += con_du
            sum_con_no_xe += con_no

            worksheet.write(row, 1, sale_order_xe_id.user_id.name,body_l)
            worksheet.write(row, 2, sale_order_xe_id.partner_id.display_name or '',body_l)
            worksheet.write(row, 3, sale_order_xe_id.name or '',body_l)
            worksheet.write(row, 4, sale_order_xe_id.sale_name or '',body_l)
            worksheet.write(row, 5, sum or '',body_l)
            worksheet.write(row, 6, sale_order_xe_id.amount_total or '', money)
            worksheet.write(row, 7, sale_order_xe_id.thu_ho or '', money)
            worksheet.write(row, 8, cash_tm or '', money)
            worksheet.write(row, 9, bank or '', money)
            worksheet.write(row, 10, con_du or '', money)
            worksheet.write(row, 11, con_no or 0, money)
            worksheet.write(row, 12, sale_order_xe_id.ghi_chu or '',body_l)

        worksheet.write('G%s' % (f + 1), sum_amount_xe, money_sum)
        worksheet.write('H%s' % (f + 1), hdv_thu_xe, money_sum)
        worksheet.write('I%s' % (f + 1), tm_xe, money_sum)
        worksheet.write('J%s' % (f + 1), ck_xe, money_sum)
        worksheet.write('K%s' % (f + 1), sum_con_du_xe, money_sum)
        worksheet.write('L%s' % (f + 1), sum_con_no_xe, money_sum)
        worksheet.write('M%s' % (f + 1), '', money_sum)

        if f < row:
            worksheet.merge_range('A%s:A%s' % (f + 1, row + 1), 'XE',text_style)
        else:
            worksheet.write('A%s' % (row + 1), 'XE',text_style)

        row += 1
        f = row
        worksheet.merge_range('B%s:F%s' % (row + 1, row + 1), 'Tổng DT Land',text_style)

        sum_amount_land = 0; ck_land = 0; tm_land = 0; hdv_thu_land = 0; sum_con_du_land = 0; sum_con_no_land = 0

        for sale_order_land_id in sale_order_land_ids:
            row += 1

            invoices = sale_order_land_id.mapped('invoice_ids')
            cash = 0
            bank = 0
            con_du = 0
            con_no = 0
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_land_id.thu_ho

            if sale_order_land_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_land_id.amount_total - cash - bank)
            else:
                con_no = sale_order_land_id.amount_total - cash - bank

            sum = 0
            for order_line in sale_order_land_id.order_line:
                sum += order_line.product_uom_qty

            sum_amount_land += sale_order_land_id.amount_total
            ck_land += bank
            tm_land += cash_tm
            hdv_thu_land += sale_order_land_id.thu_ho
            sum_con_du_land += con_du
            sum_con_no_land += con_no

            worksheet.write(row, 1, sale_order_land_id.user_id.name or '',body_l)
            worksheet.write(row, 2, sale_order_land_id.partner_id.display_name or '',body_l)
            worksheet.write(row, 3, sale_order_land_id.name or '',body_l)
            worksheet.write(row, 4, sale_order_land_id.sale_name or '',body_l)
            worksheet.write(row, 5, sum or '',body_l)
            worksheet.write(row, 6, sale_order_land_id.amount_total or '', money)
            worksheet.write(row, 7, sale_order_land_id.thu_ho or '', money)
            worksheet.write(row, 8, cash_tm or '', money)
            worksheet.write(row, 9, bank or '', money)
            worksheet.write(row, 10, con_du or '', money)
            worksheet.write(row, 11, con_no or 0, money)
            worksheet.write(row, 12, sale_order_land_id.ghi_chu or '',body_l)

        worksheet.write('G%s' % (f + 1), sum_amount_land, money_sum)
        worksheet.write('H%s' % (f + 1), hdv_thu_land, money_sum)
        worksheet.write('I%s' % (f + 1), tm_land, money_sum)
        worksheet.write('J%s' % (f + 1), ck_land, money_sum)
        worksheet.write('K%s' % (f + 1), sum_con_du_land, money_sum)
        worksheet.write('L%s' % (f + 1), sum_con_no_land, money_sum)
        worksheet.write('M%s' % (f + 1), '', money_sum)

        if f < row:
            worksheet.merge_range('A%s:A%s' % (f + 1, row + 1), 'LAND',text_style)
        else:
            worksheet.write('A%s' % (row + 1), 'LAND',text_style)

        row += 1
        f = row
        worksheet.merge_range('B%s:F%s' % (row + 1, row + 1), 'Tổng DT Ghép',text_style)

        sum_amount_ghep = 0; ck_ghep = 0; tm_ghep = 0; hdv_thu_ghep = 0; sum_con_du_ghep = 0; sum_con_no_ghep = 0

        for sale_order_ghep_id in sale_order_ghep_ids:
            row += 1

            invoices = sale_order_ghep_id.mapped('invoice_ids')
            cash = 0
            bank = 0
            con_du = 0
            con_no = 0
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_ghep_id.thu_ho

            if sale_order_ghep_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_ghep_id.amount_total - cash - bank)
            else:
                con_no = sale_order_ghep_id.amount_total - cash - bank

            sum = 0
            for order_line in sale_order_ghep_id.order_line:
                sum += order_line.product_uom_qty

            sum_amount_ghep += sale_order_ghep_id.amount_total
            ck_ghep += bank
            tm_ghep += cash_tm
            hdv_thu_ghep += sale_order_ghep_id.thu_ho
            sum_con_du_ghep += con_du
            sum_con_no_ghep += con_no

            worksheet.write(row, 1, sale_order_ghep_id.user_id.name or '',body_l)
            worksheet.write(row, 2, sale_order_ghep_id.partner_id.display_name or '',body_l)
            worksheet.write(row, 3, sale_order_ghep_id.name or '',body_l)
            worksheet.write(row, 4, sale_order_ghep_id.sale_name or '',body_l)
            worksheet.write(row, 5, sum or '',body_l)
            worksheet.write(row, 6, sale_order_ghep_id.amount_total or '', money)
            worksheet.write(row, 7, sale_order_ghep_id.thu_ho or '', money)
            worksheet.write(row, 8, cash_tm or '', money)
            worksheet.write(row, 9, bank or '', money)
            worksheet.write(row, 10, con_du or '', money)
            worksheet.write(row, 11, con_no or 0, money)
            worksheet.write(row, 12, sale_order_ghep_id.ghi_chu or '',body_l)

        worksheet.write('G%s' % (f + 1), sum_amount_ghep, money_sum)
        worksheet.write('H%s' % (f + 1), hdv_thu_ghep, money_sum)
        worksheet.write('I%s' % (f + 1), tm_ghep, money_sum)
        worksheet.write('J%s' % (f + 1), ck_ghep, money_sum)
        worksheet.write('K%s' % (f + 1), sum_con_du_ghep, money_sum)
        worksheet.write('L%s' % (f + 1), sum_con_no_ghep, money_sum)
        worksheet.write('M%s' % (f + 1), '', money_sum)

        if f < row:
            worksheet.merge_range('A%s:A%s' % (f + 1, row + 1), 'GHÉP',text_style)
        else:
            worksheet.write('A%s' % (row + 1), 'GHÉP',text_style)

        row += 1
        f = row
        worksheet.merge_range('B%s:F%s' % (row + 1, row + 1), 'Tổng DT Bà Nà 1%',text_style)

        sum_amount_ba_na = 0; ck_ba_na = 0; tm_ba_na = 0; hdv_thu_ba_na = 0; sum_con_du_ba_na = 0; sum_con_no_ba_na = 0

        for sale_order_ba_na_id in sale_order_ba_na_ids:
            row += 1

            invoices = sale_order_ba_na_id.mapped('invoice_ids')
            cash = 0
            bank = 0
            con_du = 0
            con_no = 0
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_ba_na_id.thu_ho

            if sale_order_ba_na_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_ba_na_id.amount_total - cash - bank)
            else:
                con_no = sale_order_ba_na_id.amount_total - cash - bank

            sum = 0
            for order_line in sale_order_ba_na_id.order_line:
                sum += order_line.product_uom_qty

            sum_amount_ba_na += sale_order_ba_na_id.amount_total
            ck_ba_na += bank
            tm_ba_na += cash_tm
            hdv_thu_ba_na += sale_order_ba_na_id.thu_ho
            sum_con_du_ba_na += con_du
            sum_con_no_ba_na += con_no

            worksheet.write(row, 1, sale_order_ba_na_id.user_id.name or '',body_l)
            worksheet.write(row, 2, sale_order_ba_na_id.partner_id.display_name or '',body_l)
            worksheet.write(row, 3, sale_order_ba_na_id.name or '',body_l)
            worksheet.write(row, 4, sale_order_ba_na_id.sale_name or '',body_l)
            worksheet.write(row, 5, sum or '',body_l)
            worksheet.write(row, 6, sale_order_ba_na_id.amount_total or '', money)
            worksheet.write(row, 7, sale_order_ba_na_id.thu_ho or '', money)
            worksheet.write(row, 8, cash_tm or '', money)
            worksheet.write(row, 9, bank or '', money)
            worksheet.write(row, 10, con_du or '', money)
            worksheet.write(row, 11, con_no or 0, money)
            worksheet.write(row, 12, sale_order_ba_na_id.ghi_chu or '',body_l)

        worksheet.write('G%s' % (f + 1), sum_amount_ba_na, money_sum)
        worksheet.write('H%s' % (f + 1), hdv_thu_ba_na, money_sum)
        worksheet.write('I%s' % (f + 1), tm_ba_na, money_sum)
        worksheet.write('J%s' % (f + 1), ck_ba_na, money_sum)
        worksheet.write('K%s' % (f + 1), sum_con_du_ba_na, money_sum)
        worksheet.write('L%s' % (f + 1), sum_con_no_ba_na, money_sum)
        worksheet.write('M%s' % (f + 1), '', money_sum)

        if f < row:
            worksheet.merge_range('A%s:A%s' % (f + 1, row + 1), 'BN',text_style)
        else:
            worksheet.write('A%s' % (row + 1), 'BN',text_style)

        row += 1
        f = row
        worksheet.merge_range('B%s:F%s' % (row + 1, row + 1), 'Tổng DT Vé Bà Nà 0%',text_style)

        sum_amount_ve_bn = 0; ck_ve_bn = 0; tm_ve_bn = 0; hdv_thu_ve_bn = 0; sum_con_du_ve_bn = 0; sum_con_no_ve_bn = 0

        for sale_order_ve_ba_na_id in sale_order_ve_ba_na_ids:
            row += 1

            invoices = sale_order_ve_ba_na_id.mapped('invoice_ids')
            cash = 0
            bank = 0
            con_du = 0
            con_no = 0
            for payment_id in invoices.mapped('payment_ids'):
                if payment_id.journal_id.type == 'cash':
                    cash += payment_id.amount
                if payment_id.journal_id.type == 'bank':
                    bank += payment_id.amount
            cash_tm = cash - sale_order_ve_ba_na_id.thu_ho

            if sale_order_ve_ba_na_id.amount_total - cash - bank < 0:
                con_du = abs(sale_order_ve_ba_na_id.amount_total - cash - bank)
            else:
                con_no = sale_order_ve_ba_na_id.amount_total - cash - bank

            sum = 0
            for order_line in sale_order_ve_ba_na_id.order_line:
                sum += order_line.product_uom_qty

            sum_amount_ve_bn += sale_order_ve_ba_na_id.amount_total
            ck_ve_bn += bank
            tm_ve_bn += cash_tm
            hdv_thu_ve_bn += sale_order_ve_ba_na_id.thu_ho
            sum_con_du_ve_bn += con_du
            sum_con_no_ve_bn += con_no

            worksheet.write(row, 1, sale_order_ve_ba_na_id.user_id.name or '',body_l)
            worksheet.write(row, 2, sale_order_ve_ba_na_id.partner_id.display_name or '',body_l)
            worksheet.write(row, 3, sale_order_ve_ba_na_id.name or '',body_l)
            worksheet.write(row, 4, sale_order_ve_ba_na_id.sale_name or '',body_l)
            worksheet.write(row, 5, sum or '',body_l)
            worksheet.write(row, 6, sale_order_ve_ba_na_id.amount_total or '', money)
            worksheet.write(row, 7, sale_order_ve_ba_na_id.thu_ho or '', money)
            worksheet.write(row, 8, cash_tm or '', money)
            worksheet.write(row, 9, bank or '', money)
            worksheet.write(row, 10, con_du or '', money)
            worksheet.write(row, 11, con_no or 0, money)
            worksheet.write(row, 12, sale_order_ve_ba_na_id.ghi_chu or '',body_l)

        worksheet.write('G%s' % (f + 1), sum_amount_ve_bn, money_sum)
        worksheet.write('H%s' % (f + 1), hdv_thu_ve_bn, money_sum)
        worksheet.write('I%s' % (f + 1), tm_ve_bn, money_sum)
        worksheet.write('J%s' % (f + 1), ck_ve_bn, money_sum)
        worksheet.write('K%s' % (f + 1), sum_con_du_ve_bn, money_sum)
        worksheet.write('L%s' % (f + 1), sum_con_no_ve_bn, money_sum)
        worksheet.write('M%s' % (f + 1), '', money_sum)

        if f < row:
            worksheet.merge_range('A%s:A%s' % (f + 1, row + 1), 'VBN',text_style)
        else:
            worksheet.write('A%s' % (row + 1), 'VBN',text_style)

        row += 1
        sum_all_amount = sum_amount_xe + sum_amount_land + sum_amount_ghep + sum_amount_ba_na + sum_amount_ve_bn
        sum_all_hdv_thu = hdv_thu_xe + hdv_thu_land + hdv_thu_ghep + hdv_thu_ba_na + hdv_thu_ve_bn
        sum_all_tm = tm_xe + tm_land + tm_ghep + tm_ba_na + tm_ve_bn
        sum_all_ck = ck_xe + ck_land + ck_ghep + ck_ba_na + ck_ve_bn
        sum_all_con_du = sum_con_du_xe + sum_con_du_land + sum_con_du_ghep + sum_con_du_ba_na + sum_con_du_ve_bn
        sum_all_con_no = sum_con_no_xe + sum_con_no_land + sum_con_no_ghep + sum_con_no_ba_na + sum_con_no_ve_bn
        worksheet.merge_range('A%s:F%s' % (row + 1, row + 1), 'Tổng Doanh Thu', text_style)
        worksheet.write('G%s' % (row + 1), sum_all_amount, money_sum)
        worksheet.write('H%s' % (row + 1), sum_all_hdv_thu, money_sum)
        worksheet.write('I%s' % (row + 1), sum_all_tm, money_sum)
        worksheet.write('J%s' % (row + 1), sum_all_ck, money_sum)
        worksheet.write('K%s' % (row + 1), sum_all_con_du, money_sum)
        worksheet.write('L%s' % (row + 1), sum_all_con_no, money_sum)


        row += 1
        worksheet.merge_range('A%s:F%s' % (row + 1, row + 1), 'Tổng Doanh Thu Tính Hoa Hồng', text_style)

        workbook.close()
        output.seek(0)
        result = base64.b64encode(output.read())
        attachment_obj = self.env['ir.attachment']
        attachment_id = attachment_obj.create(
            {'name': 'Báo cáo doanh thu.xlsx', 'datas_fname': 'Báo cáo doanh thu.xlsx', 'datas': result})
        download_url = '/web/content/' + str(attachment_id.id) + '?download=True'
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')

        return {"type": "ir.actions.act_url",
                "url": str(base_url) + str(download_url)}

class report_tour_land(models.Model):
    _name = 'report.tour.land'

    bao_cao_tour_id = fields.Many2one('bao.cao.tour')
    user_id = fields.Many2one('res.users', string="Nhân viên bán hàng")
    partner_id = fields.Many2one('res.partner',string="Đối tác")
    code_dh = fields.Char(string="Code ĐH")
    code_sale = fields.Many2one('sale.order', string="Code Sale")
    sl = fields.Float(string="SL")
    tong_tien = fields.Float(string="Tổng tiền")
    hdv_thu = fields.Float(string="HDV Thu")
    tm = fields.Float(string="TM")
    ck = fields.Float(string="CK")
    con_du = fields.Float(string="Còn dư")
    con_no = fields.Float(string="Còn nợ")
    chi_tiet_tt = fields.Text(string="Chi tiết thanh toán")

class report_tour_ghep(models.Model):
    _name = 'report.tour.ghep'

    bao_cao_tour_id = fields.Many2one('bao.cao.tour')
    user_id = fields.Many2one('res.users', string="Nhân viên bán hàng")
    partner_id = fields.Many2one('res.partner',string="Đối tác")
    code_dh = fields.Char(string="Code ĐH")
    code_sale = fields.Many2one('sale.order', string="Code Sale")
    sl = fields.Float(string="SL")
    tong_tien = fields.Float(string="Tổng tiền")
    hdv_thu = fields.Float(string="HDV Thu")
    tm = fields.Float(string="TM")
    ck = fields.Float(string="CK")
    con_du = fields.Float(string="Còn dư")
    con_no = fields.Float(string="Còn nợ")
    chi_tiet_tt = fields.Text(string="Chi tiết thanh toán")

class report_tour_xe(models.Model):
    _name = 'report.tour.xe'

    bao_cao_tour_id = fields.Many2one('bao.cao.tour')
    user_id = fields.Many2one('res.users', string="Nhân viên bán hàng")
    partner_id = fields.Many2one('res.partner',string="Đối tác")
    code_dh = fields.Char(string="Code ĐH")
    code_sale = fields.Many2one('sale.order', string="Code Sale")
    sl = fields.Float(string="SL")
    tong_tien = fields.Float(string="Tổng tiền")
    hdv_thu = fields.Float(string="HDV Thu")
    tm = fields.Float(string="TM")
    ck = fields.Float(string="CK")
    con_du = fields.Float(string="Còn dư")
    con_no = fields.Float(string="Còn nợ")
    chi_tiet_tt = fields.Text(string="Chi tiết thanh toán")

class report_tour_ba_na(models.Model):
    _name = 'report.tour.ba.na'

    bao_cao_tour_id = fields.Many2one('bao.cao.tour')
    user_id = fields.Many2one('res.users', string="Nhân viên bán hàng")
    partner_id = fields.Many2one('res.partner',string="Đối tác")
    code_dh = fields.Char(string="Code ĐH")
    code_sale = fields.Many2one('sale.order', string="Code Sale")
    sl = fields.Float(string="SL")
    tong_tien = fields.Float(string="Tổng tiền")
    hdv_thu = fields.Float(string="HDV Thu")
    tm = fields.Float(string="TM")
    ck = fields.Float(string="CK")
    con_du = fields.Float(string="Còn dư")
    con_no = fields.Float(string="Còn nợ")
    chi_tiet_tt = fields.Text(string="Chi tiết thanh toán")

class report_tour_ve_bn(models.Model):
    _name = 'report.tour.ve.bn'

    bao_cao_tour_id = fields.Many2one('bao.cao.tour')
    user_id = fields.Many2one('res.users',string="Nhân viên bán hàng")
    partner_id = fields.Many2one('res.partner',string="Đối tác")
    code_dh = fields.Char(string="Code ĐH")
    code_sale = fields.Many2one('sale.order',string="Code Sale")
    sl = fields.Float(string="SL")
    tong_tien = fields.Float(string="Tổng tiền")
    hdv_thu = fields.Float(string="HDV Thu")
    tm = fields.Float(string="TM")
    ck = fields.Float(string="CK")
    con_du = fields.Float(string="Còn dư")
    con_no = fields.Float(string="Còn nợ")
    chi_tiet_tt = fields.Text(string="Chi tiết thanh toán")