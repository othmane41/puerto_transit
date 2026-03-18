# -*- coding: utf-8 -*-
from odoo import models, fields


class PuertoDossierCircuit(models.Model):
    _name = 'puerto.dossier.circuit'
    _description = 'Circuit de Validation Dossier Transit'

    dossier_id = fields.Many2one(
        'puerto.dossier', string='Dossier', required=True, ondelete='cascade')
    service_demandeur = fields.Char(string='Service Demandeur')
    user_demandeur_id = fields.Many2one('res.users', string='Utilisateur Demandeur')
    intitule_tache = fields.Char(string='Intitulé Tâche', required=True)
    priorite_id = fields.Many2one('puerto.priorite', string='Priorité')
    service_destinataire = fields.Char(string='Service Destinataire')
    user_destinataire_id = fields.Many2one(
        'res.users', string='Utilisateur Destinataire')
    statut = fields.Selection([
        ('en_attente', 'En Attente'),
        ('en_cours', 'En Cours'),
        ('cloturee', 'Clôturée'),
        ('rejetee', 'Rejetée'),
    ], string='Statut', default='en_attente')
    date_creation = fields.Datetime(
        string='Date Création', default=fields.Datetime.now)
    date_reception = fields.Datetime(string='Date Réception')
    date_cloture = fields.Datetime(string='Date Clôture')
    reference = fields.Char(string='Référence')
    commentaire = fields.Text(string='Commentaire')
