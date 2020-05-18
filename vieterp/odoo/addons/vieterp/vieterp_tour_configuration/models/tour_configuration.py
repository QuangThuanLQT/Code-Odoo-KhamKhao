# -*- coding: utf-8 -*-

from odoo import models, fields, api

class chuong_trinh_tour(models.Model):
    _name='chuong.trinh.tour'

    name = fields.Char(string="Tiêu đề")
    breakfast = fields.Boolean(string="Bao gồm ăn sáng?")
    lunch = fields.Boolean(string="Bao gồm ăn trưa?")
    dinner = fields.Boolean(string="Bao gồm ăn tối?")
    description = fields.Text(string="Mô tả")
    day = fields.Char(string="Ngày", default=1)

class chuong_trinh_tour_line(models.Model):
    _name='chuong.trinh.tour.line'

    hanh_trinh_id = fields.Many2one('chuong.trinh.tour',string="Chương trình tour")
    breakfast = fields.Boolean(string="Bao gồm ăn sáng?", related="hanh_trinh_id.breakfast")
    lunch = fields.Boolean(string="Bao gồm ăn trưa?" , related="hanh_trinh_id.lunch")
    dinner = fields.Boolean(string="Bao gồm ăn tối?" , related="hanh_trinh_id.dinner")
    day = fields.Char(string="Ngày", default=1)
    hanh_trinh_line_id = fields.Many2one('product.template')


class product_template_ihr(models.Model):
    _inherit = 'product.template'

    hanh_trinh_line = fields.One2many('chuong.trinh.tour.line','hanh_trinh_line_id',string="Hành trình")






