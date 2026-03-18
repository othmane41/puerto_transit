# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PuertoDossier(models.Model):
    _name = 'puerto.dossier'
    _description = 'Dossier Transit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'date_creation desc'

    # ── En-tête ──────────────────────────────────────────────────────────────
    name = fields.Char(
        string='N° Dossier', readonly=True, copy=False, default='/')
    type_dossier = fields.Selection([
        ('import', 'Import'),
        ('export', 'Export'),
        ('cession', 'Cession'),
        ('intervention', 'Intervention'),
    ], string='Type Dossier', required=True, default='import', tracking=True)
    date_creation = fields.Datetime(
        string='Date Création', default=fields.Datetime.now, readonly=True)
    date_reception_demande = fields.Datetime(
        string='Date Réception Demande', default=fields.Datetime.now)
    date_reception_dernier_element = fields.Datetime(
        string='Date Réception Dernier Élément')
    date_etd_eta = fields.Datetime(
        string='ETD/ETA', required=True, tracking=True)
    priorite_id = fields.Many2one(
        'puerto.priorite', string='Priorité', tracking=True)
    selectivite = fields.Selection([
        ('vert', 'Vert'),
        ('orange', 'Orange'),
        ('rouge', 'Rouge'),
    ], string='Sélectivité', tracking=True)
    categorie = fields.Selection([
        ('perissable', 'Périssable'),
        ('industrie', 'Industrie'),
        ('consignation', 'Consignation'),
        ('transport', 'Transport'),
    ], string='Catégorie')
    groupage = fields.Boolean(string='Groupage', default=False)

    # Partenaires
    partner_id = fields.Many2one(
        'res.partner', string='Soumissionnaire', required=True, tracking=True)
    client_facturation_id = fields.Many2one(
        'res.partner', string='Client Facturation', tracking=True)
    expediteur_id = fields.Many2one(
        'res.partner', string='Expéditeur')
    destinataire_id = fields.Many2one(
        'res.partner', string='Destinataire')
    reference_client = fields.Char(string='Référence Client')

    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('ouvert', 'Ouvert'),
        ('en_cours', 'En Cours'),
        ('cloture', 'Clôturé'),
    ], string='Statut', default='brouillon', tracking=True, group_expand='_expand_states')

    # ── Détail déclaration ────────────────────────────────────────────────────
    num_dum_initiale = fields.Char(string='N° DUM Initiale')
    num_dum_definitive = fields.Char(string='N° DUM Définitive')
    date_debut_dum = fields.Datetime(string='Date Début DUM')
    date_fin_dum = fields.Datetime(string='Date Fin DUM')
    regime_id = fields.Many2one('puerto.regime', string='Régime Douanier')
    bureau_dedouanement_id = fields.Many2one(
        'puerto.bureau', string='Bureau Dédouanement')
    arrondissement_id = fields.Many2one(
        'puerto.arrondissement', string='Arrondissement')
    lieu_stockage_id = fields.Many2one(
        'puerto.lieu.stockage', string='Lieu Stockage')
    lieu_stockage_dest_id = fields.Many2one(
        'puerto.lieu.stockage', string='Lieu Stockage Destination')
    bureau_destination_id = fields.Many2one(
        'puerto.bureau', string='Bureau Destination')
    currency_id = fields.Many2one(
        'res.currency', string='Devise',
        default=lambda self: self.env.company.currency_id)

    # ── Marchandise ───────────────────────────────────────────────────────────
    type_contenant_palette = fields.Char(string='Type Contenant Palette')
    nb_contenant_palette = fields.Integer(string='Nb Palette')
    type_contenant_colis = fields.Char(
        string='Type Contenant Colis', required=True)
    nb_contenant_colis = fields.Integer(string='Nb Colis', required=True)
    nature_marchandise = fields.Char(string='Nature Marchandise')
    poids_brut_total = fields.Float(string='Poids Brut Total (kg)')
    incoterm_id = fields.Many2one('account.incoterms', string='Incoterm')
    pays_origine_id = fields.Many2one('res.country', string="Pays d'Origine")
    pays_provenance_id = fields.Many2one(
        'res.country', string='Pays de Provenance')
    contenant_id = fields.Many2one('puerto.contenant', string='Type Contenant')
    nb_contenant = fields.Integer(string='Nb Contenants')

    # ── Transport ─────────────────────────────────────────────────────────────
    mode_transport_id = fields.Many2one(
        'puerto.mode.transport', string='Mode Transport', tracking=True)
    type_transport_id = fields.Many2one(
        'puerto.type.transport', string='Type Transport',
        domain="[('mode_transport_id', '=', mode_transport_id)]")
    date_voyage = fields.Datetime(string='Date Voyage')
    date_presentation = fields.Datetime(string='Date Présentation')
    contact_chauffeur = fields.Char(string='Contact Chauffeur')
    transporteur_id = fields.Many2one('res.partner', string='Transporteur')
    terminal_id = fields.Many2one(
        'puerto.terminal', string='Terminal',
        help='Visible pour transport maritime')
    num_connaissement = fields.Char(string='N° Connaissement')
    num_lot = fields.Char(string='N° Lot')
    nb_transport = fields.Integer(string='Nombre de transport')
    marque_ref_transport = fields.Char(string='Marque/Réf. Transport')
    sous_type_unite = fields.Char(string="Sous type d'unité")

    # ── Scellés ───────────────────────────────────────────────────────────────
    proprietaire_scelles = fields.Char(string='Propriétaire des scellés')
    pt_transporteur_autres = fields.Char(string='PT/Transporteur/Autres')
    centre_rc = fields.Char(string='Centre RC / N°RC')
    num_serie_scelles = fields.Char(string='N° Série des scellés')
    nb_scelles = fields.Integer(string='Nombre des scellés')

    # ── Document de sortie (DS) ───────────────────────────────────────────────
    type_ds = fields.Char(string='Type DS')
    ref_ds = fields.Char(string='Référence DS')
    lieu_chargement = fields.Char(string='Lieu de chargement')

    # ── Marchandise compléments ───────────────────────────────────────────────
    cas_hors_standard = fields.Char(string='Cas hors standard (palette/Colis)')
    annexe_demande = fields.Char(string='Annexe (Demande de service)')
    matricule = fields.Char(string='Matricule')

    # ── Expéditeur détail ─────────────────────────────────────────────────────
    expediteur_adresse = fields.Char(string="Adresse Expéditeur")
    expediteur_ville = fields.Char(string="Ville Expéditeur")
    expediteur_pays_text = fields.Char(string="Pays Expéditeur")
    port_depart = fields.Char(string="De (Port départ)")

    # ── Destinataire détail ───────────────────────────────────────────────────
    destinataire_adresse = fields.Char(string="Adresse Destinataire")
    destinataire_ville = fields.Char(string="Ville Destinataire")
    destinataire_pays_text = fields.Char(string="Pays Destinataire")
    port_arrivee = fields.Char(string="À (Port arrivée)")

    # ── Relations ─────────────────────────────────────────────────────────────
    facture_ids = fields.One2many(
        'puerto.dossier.facture', 'dossier_id', string='Factures')
    charge_ids = fields.One2many(
        'puerto.dossier.charge', 'dossier_id', string='Charges')
    document_ids = fields.One2many(
        'puerto.dossier.document', 'dossier_id', string='Documents')
    circuit_ids = fields.One2many(
        'puerto.dossier.circuit', 'dossier_id', string='Circuit')

    # ── Computed counts ───────────────────────────────────────────────────────
    facture_count = fields.Integer(
        string='Nb Factures', compute='_compute_counts')
    charge_count = fields.Integer(
        string='Nb Charges', compute='_compute_counts')
    document_count = fields.Integer(
        string='Nb Documents', compute='_compute_counts')

    @api.depends('facture_ids', 'charge_ids', 'document_ids')
    def _compute_counts(self):
        for rec in self:
            rec.facture_count = len(rec.facture_ids)
            rec.charge_count = len(rec.charge_ids)
            rec.document_count = len(rec.document_ids)

    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, _val in self._fields['state'].selection]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                type_d = vals.get('type_dossier', 'import')
                seq_code = (
                    'puerto.dossier.export'
                    if type_d == 'export'
                    else 'puerto.dossier.import'
                )
                vals['name'] = self.env['ir.sequence'].next_by_code(seq_code) or '/'
        return super().create(vals_list)

    def action_open(self):
        self.write({'state': 'ouvert'})

    def action_en_cours(self):
        self.write({'state': 'en_cours'})

    def action_cloture(self):
        self.write({'state': 'cloture'})

    def action_reset(self):
        self.write({'state': 'brouillon'})

    def action_view_factures(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Factures',
            'res_model': 'puerto.dossier.facture',
            'view_mode': 'list,form',
            'domain': [('dossier_id', '=', self.id)],
            'context': {'default_dossier_id': self.id},
        }

    def action_view_charges(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Charges',
            'res_model': 'puerto.dossier.charge',
            'view_mode': 'list,form',
            'domain': [('dossier_id', '=', self.id)],
            'context': {'default_dossier_id': self.id},
        }

    def action_view_documents(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Documents',
            'res_model': 'puerto.dossier.document',
            'view_mode': 'list,form',
            'domain': [('dossier_id', '=', self.id)],
            'context': {'default_dossier_id': self.id},
        }
