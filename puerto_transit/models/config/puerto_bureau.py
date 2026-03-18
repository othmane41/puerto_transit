# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoBureau(models.Model):
    _name = 'puerto.bureau'
    _description = 'Bureau Douanier'
    _rec_name = 'name'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Désignation', required=True)
    type = fields.Selection([
        ('port', 'Port'),
        ('zai', 'ZAI'),
        ('zone_logistique', 'Zone Logistique'),
        ('aeroport', 'Aéroport'),
        ('bureau_frontal', 'Bureau Frontalier'),
    ], string='Type')
