# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoModeTransport(models.Model):
    _name = 'puerto.mode.transport'
    _description = 'Mode de Transport'
    _rec_name = 'name'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Désignation', required=True)
    type = fields.Selection([
        ('maritime', 'Maritime'),
        ('aerien', 'Aérien'),
        ('routier', 'Routier'),
        ('ferroviaire', 'Ferroviaire'),
    ], string='Type', required=True)
