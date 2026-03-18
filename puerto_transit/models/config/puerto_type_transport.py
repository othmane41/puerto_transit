# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoTypeTransport(models.Model):
    _name = 'puerto.type.transport'
    _description = 'Type de Transport'
    _rec_name = 'name'
    _order = 'code'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Désignation', required=True)
    mode_transport_id = fields.Many2one('puerto.mode.transport', string='Mode de Transport', required=True)
