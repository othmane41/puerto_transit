# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PuertoDossierFacture(models.Model):
    _name = 'puerto.dossier.facture'
    _description = 'Facture Dossier Transit'
    _rec_name = 'num_facture'

    dossier_id = fields.Many2one(
        'puerto.dossier', string='Dossier', required=True, ondelete='cascade')
    num_facture = fields.Char(string='N° Facture', required=True)
    date_facture = fields.Date(string='Date Facture')
    partner_id = fields.Many2one('res.partner', string='Fournisseur')
    poids_brut_total = fields.Float(string='Poids Brut Total (kg)')
    poids_net_total = fields.Float(string='Poids Net Total (kg)')
    valeur_total = fields.Float(string='Valeur Totale', compute='_compute_valeur_total', store=True)
    currency_id = fields.Many2one(
        'res.currency', string='Devise',
        default=lambda self: self.env.company.currency_id)
    paiement = fields.Selection([
        ('avec', 'Avec'),
        ('sans', 'Sans'),
    ], string='Paiement', default='avec')
    type_marchandise = fields.Selection([
        ('neuf', 'Neuf'),
        ('occasion', 'Occasion'),
    ], string='Type Marchandise', default='neuf')
    incoterm_id = fields.Many2one('account.incoterms', string='Incoterm')
    notion_origine = fields.Char(string="Notion d'Origine")
    num_eacce = fields.Char(string='N° EACCE')

    line_ids = fields.One2many(
        'puerto.dossier.facture.line', 'facture_id', string='Lignes Facture')

    @api.depends('line_ids.prix_net')
    def _compute_valeur_total(self):
        for rec in self:
            rec.valeur_total = sum(rec.line_ids.mapped('prix_net'))


class PuertoDossierFactureLine(models.Model):
    _name = 'puerto.dossier.facture.line'
    _description = 'Ligne Facture Dossier Transit'

    facture_id = fields.Many2one(
        'puerto.dossier.facture', string='Facture', required=True, ondelete='cascade')
    code_article = fields.Char(string='Code Article')
    description = fields.Char(string='Description')
    code_nomenclature = fields.Char(string='Code Nomenclature')
    designation_commerciale = fields.Char(string='Désignation Commerciale')
    uom_id = fields.Many2one('uom.uom', string='Unité de Mesure')
    quantite = fields.Float(string='Quantité', default=1.0)
    poids_net_unitaire = fields.Float(string='Poids Net Unitaire (kg)')
    prix_unitaire = fields.Float(string='Prix Unitaire')
    prix_net = fields.Float(
        string='Prix Net', compute='_compute_prix_net', store=True)
    montant_devise = fields.Float(string='Montant Devise')

    @api.depends('quantite', 'prix_unitaire')
    def _compute_prix_net(self):
        for line in self:
            line.prix_net = line.quantite * line.prix_unitaire
