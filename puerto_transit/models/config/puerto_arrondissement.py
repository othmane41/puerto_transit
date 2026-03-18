# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoArrondissement(models.Model):
    _name = 'puerto.arrondissement'
    _description = 'Arrondissement Douanier'
    _rec_name = 'name'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Désignation', required=True)
