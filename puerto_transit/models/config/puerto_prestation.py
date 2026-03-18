# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoPrestation(models.Model):
    _name = 'puerto.prestation'
    _description = 'Prestation'
    _rec_name = 'name'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Désignation', required=True)
    price = fields.Float(string='Prix unitaire', default=0.0)
