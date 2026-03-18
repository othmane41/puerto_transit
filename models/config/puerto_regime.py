# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoRegime(models.Model):
    _name = 'puerto.regime'
    _description = 'Régime Douanier'
    _rec_name = 'name'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Description', required=True)
    type = fields.Selection([
        ('import', 'Import'),
        ('export', 'Export'),
    ], string='Type', required=True, default='import')
