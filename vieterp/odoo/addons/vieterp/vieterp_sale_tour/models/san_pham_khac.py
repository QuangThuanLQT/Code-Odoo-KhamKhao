# -*- coding: utf-8 -*-

from odoo import models, fields, api

class san_pham_khac(models.Model):
    _name = 'san.pham.khac'

    name = fields.Char(string="Tên")