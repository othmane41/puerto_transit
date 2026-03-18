# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoDossierDocument(models.Model):
    _name = 'puerto.dossier.document'
    _description = 'Document / Annexe Dossier Transit'

    dossier_id = fields.Many2one(
        'puerto.dossier', string='Dossier', required=True, ondelete='cascade')
    type_annexe = fields.Char(string="Type d'Annexe")
    nom_document = fields.Char(string='Nom Document', required=True)
    createur_id = fields.Many2one(
        'res.users', string='Créateur', default=lambda self: self.env.user)
    date_reception = fields.Date(string='Date Réception')
    date_annexation = fields.Date(
        string="Date d'Annexation", default=fields.Date.today)
    attachment_id = fields.Many2one('ir.attachment', string='Fichier')
    commentaire = fields.Text(string='Commentaire')
