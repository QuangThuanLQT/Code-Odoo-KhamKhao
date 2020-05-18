# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_schedule(models.Model):
    _name = 'sale.schedule'
    _rec_name = 'schedule'

    schedule = fields.Char(string="Lịch trình")
    description = fields.Text(string="Miêu tả")
