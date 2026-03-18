# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoLieuStockage(models.Model):
    _name = 'puerto.lieu.stockage'
    _description = 'Lieu de Stockage'
    _rec_name = 'name'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Désignation', required=True)
