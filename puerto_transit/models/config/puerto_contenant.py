# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoContenant(models.Model):
    _name = 'puerto.contenant'
    _description = 'Type de Contenant'
    _rec_name = 'name'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Désignation', required=True)
