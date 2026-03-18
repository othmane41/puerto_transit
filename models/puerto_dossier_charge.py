# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PuertoDossierCharge(models.Model):
    _name = 'puerto.dossier.charge'
    _description = 'Charge / Débours Dossier Transit'

    dossier_id = fields.Many2one(
        'puerto.dossier', string='Dossier', required=True, ondelete='cascade')
    mode_facturation = fields.Selection([
        ('forfait', 'Forfait'),
        ('unitaire', 'Unitaire'),
    ], string='Mode Facturation', default='forfait')
    prestataire_id = fields.Many2one('res.partner', string='Prestataire')
    prestation_id = fields.Many2one('puerto.prestation', string='Prestation')
    date = fields.Date(string='Date', default=fields.Date.today)
    ref_document = fields.Char(string='Réf. Document')
    prix_unitaire = fields.Float(string='Prix Unitaire')
    quantite = fields.Float(string='Quantité', default=1.0)
    montant_total = fields.Float(
        string='Montant Total', compute='_compute_montant_total', store=True)
    currency_id = fields.Many2one(
        'res.currency', string='Devise',
        default=lambda self: self.env.company.currency_id)
    commentaire = fields.Text(string='Commentaire')

    @api.depends('prix_unitaire', 'quantite')
    def _compute_montant_total(self):
        for rec in self:
            rec.montant_total = rec.prix_unitaire * rec.quantite
