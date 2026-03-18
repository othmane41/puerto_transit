# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoTerminal(models.Model):
    _name = 'puerto.terminal'
    _description = 'Terminal'
    _rec_name = 'name'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Désignation', required=True)
