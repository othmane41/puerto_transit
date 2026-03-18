# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoPriorite(models.Model):
    _name = 'puerto.priorite'
    _description = 'Priorité'
    _rec_name = 'name'
    _order = 'sequence'

    name = fields.Char(string='Nom', required=True)
    sequence = fields.Integer(string='Séquence', default=10)
