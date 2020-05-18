# -*- coding: utf-8 -*-
# import os
from odoo import models, fields, api

# dir_path = os.path.dirname(os.path.realpath(__file__))
class vieterp_base(models.Model):
    _name = 'vieterp.base'

    @api.model
    def execute_query(self, query, get_result=False):
        self.env.cr.execute(query)
        if get_result:
            results = self.env.cr.fetchall()
            return results
        return True