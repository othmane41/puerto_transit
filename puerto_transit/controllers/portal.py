# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


def _fix_datetime(value):
    """Convert HTML datetime-local format (2026-03-19T01:09) to Odoo format (2026-03-19 01:09:00)."""
    if value and 'T' in value:
        return value.replace('T', ' ') + ':00' if len(value) == 16 else value.replace('T', ' ')
    return value or False


class TransitPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'dossier_count' in counters:
            values['dossier_count'] = request.env['puerto.dossier'].search_count(
                self._get_dossier_domain()
            )
        return values

    def _get_dossier_domain(self):
        return [('partner_id', '=', request.env.user.partner_id.id)]

    def _get_form_context(self, error=None, values=None):
        env = request.env
        return {
            'page_name': 'dossiers',
            'error': error or {},
            'values': values or {},
            'regimes': env['puerto.regime'].sudo().search([]),
            'bureaux': env['puerto.bureau'].sudo().search([]),
            'arrondissements': env['puerto.arrondissement'].sudo().search([]),
            'lieux_stockage': env['puerto.lieu.stockage'].sudo().search([]),
            'modes_transport': env['puerto.mode.transport'].sudo().search([]),
            'contenants': env['puerto.contenant'].sudo().search([]),
            'priorites': env['puerto.priorite'].sudo().search([]),
            'pays': env['res.country'].sudo().search([], order='name asc'),
            'incoterms': env['account.incoterms'].sudo().search([]),
        }

    # ── Liste ─────────────────────────────────────────────────────────────────
    @http.route(['/my/dossiers', '/my/dossiers/page/<int:page>'],
                type='http', auth='user', website=True)
    def portal_my_dossiers(self, page=1, sortby=None, **kw):
        Dossier = request.env['puerto.dossier']
        domain = self._get_dossier_domain()

        sort_order = {
            'date': 'date_creation desc',
            'name': 'name asc',
            'state': 'state asc',
        }
        order = sort_order.get(sortby, 'date_creation desc')

        dossier_count = Dossier.search_count(domain)
        pager = portal_pager(
            url='/my/dossiers',
            url_args={'sortby': sortby},
            total=dossier_count,
            page=page,
            step=10,
        )
        dossiers = Dossier.search(
            domain, order=order, limit=10, offset=pager['offset'])

        all_dossiers = Dossier.search(domain)
        all_factures = all_dossiers.mapped('facture_ids')
        total_lignes = sum(len(f.line_ids) for f in all_factures)
        total_poids_net = sum(f.poids_net_total for f in all_factures)
        total_poids_brut = sum(f.poids_brut_total for f in all_factures)

        active_tab = kw.get('tab', 'ouverture')

        return request.render('puerto_transit.portal_my_dossiers', {
            'dossiers': dossiers,
            'page_name': 'dossiers',
            'pager': pager,
            'default_url': '/my/dossiers',
            'sortby': sortby,
            'all_factures': all_factures,
            'total_lignes': total_lignes,
            'total_poids_net': total_poids_net,
            'total_poids_brut': total_poids_brut,
            'active_tab': active_tab,
        })

    # ── Détail ────────────────────────────────────────────────────────────────
    @http.route(['/my/dossiers/<int:dossier_id>'],
                type='http', auth='user', website=True)
    def portal_dossier_detail(self, dossier_id, **kw):
        dossier = request.env['puerto.dossier'].sudo().browse(dossier_id)
        if not dossier.exists():
            return request.not_found()
        if dossier.partner_id.id != request.env.user.partner_id.id:
            return request.not_found()

        return request.render('puerto_transit.portal_my_dossier_detail', {
            'dossier': dossier,
            'page_name': 'dossiers',
        })

    # ── Nouveau dossier — GET ─────────────────────────────────────────────────
    @http.route(['/my/dossiers/new'],
                type='http', auth='user', website=True, methods=['GET'])
    def portal_dossier_new(self, **kw):
        return request.render('puerto_transit.portal_dossier_new',
                              self._get_form_context())

    # ── Nouveau dossier — POST ────────────────────────────────────────────────
    @http.route(['/my/dossiers/new'],
                type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def portal_dossier_new_post(self, **post):
        env = request.env
        error = {}

        required = {
            'type_dossier': 'Type de dossier',
            'date_etd_eta': 'ETD/ETA',
            'type_contenant_colis': 'Type de colis',
            'nb_contenant_colis': 'Nombre de colis',
        }
        for field, label in required.items():
            if not post.get(field, '').strip():
                error[field] = f'Le champ « {label} » est obligatoire.'

        if error:
            ctx = self._get_form_context(error=error, values=post)
            return request.render('puerto_transit.portal_dossier_new', ctx)

        vals = {
            'partner_id': request.env.user.partner_id.id,
            'type_dossier': post.get('type_dossier'),
            'date_etd_eta': _fix_datetime(post.get('date_etd_eta')),
            'date_reception_demande': _fix_datetime(post.get('date_reception_demande')),
            'date_reception_dernier_element': _fix_datetime(post.get('date_reception_dernier_element')),
            'type_contenant_colis': post.get('type_contenant_colis'),
            'nb_contenant_colis': int(post.get('nb_contenant_colis') or 0),
            'type_contenant_palette': post.get('type_contenant_palette') or False,
            'nb_contenant_palette': int(post.get('nb_contenant_palette') or 0),
            'nature_marchandise': post.get('nature_marchandise') or False,
            'reference_client': post.get('reference_client') or False,
            'poids_brut_total': float(post.get('poids_brut_total') or 0),
            'groupage': post.get('groupage') in ('1', 'true', 'on'),
            'num_dum_initiale': post.get('num_dum_initiale') or False,
            'num_dum_definitive': post.get('num_dum_definitive') or False,
            'date_debut_dum': post.get('date_debut_dum') or False,
            'date_fin_dum': post.get('date_fin_dum') or False,
            'annexe_demande': post.get('annexe_demande') or False,
            'matricule': post.get('matricule') or False,
            'categorie': post.get('categorie') or False,
            'selectivite': post.get('selectivite') or False,
            # Transport
            'date_voyage': _fix_datetime(post.get('date_voyage')),
            'date_presentation': _fix_datetime(post.get('date_presentation')),
            'nb_transport': int(post.get('nb_transport') or 0),
            'marque_ref_transport': post.get('marque_ref_transport') or False,
            'sous_type_unite': post.get('sous_type_unite') or False,
            # Scellés
            'proprietaire_scelles': post.get('proprietaire_scelles') or False,
            'pt_transporteur_autres': post.get('pt_transporteur_autres') or False,
            'centre_rc': post.get('centre_rc') or False,
            'num_serie_scelles': post.get('num_serie_scelles') or False,
            'nb_scelles': int(post.get('nb_scelles') or 0),
            # DS
            'type_ds': post.get('type_ds') or False,
            'ref_ds': post.get('ref_ds') or False,
            'lieu_chargement': post.get('lieu_chargement') or False,
            'num_lot': post.get('num_lot') or False,
            # Expéditeur
            'expediteur_adresse': post.get('expediteur_adresse') or False,
            'expediteur_ville': post.get('expediteur_ville') or False,
            'expediteur_pays_text': post.get('expediteur_pays_text') or False,
            'port_depart': post.get('port_depart') or False,
            # Destinataire
            'destinataire_adresse': post.get('destinataire_adresse') or False,
            'destinataire_ville': post.get('destinataire_ville') or False,
            'destinataire_pays_text': post.get('destinataire_pays_text') or False,
            'port_arrivee': post.get('port_arrivee') or False,
            # Marchandise
            'nb_contenant': int(post.get('nb_contenant') or 0),
            'cas_hors_standard': post.get('cas_hors_standard') or False,
        }

        m2o = {
            'regime_id': 'puerto.regime',
            'bureau_dedouanement_id': 'puerto.bureau',
            'bureau_destination_id': 'puerto.bureau',
            'arrondissement_id': 'puerto.arrondissement',
            'lieu_stockage_id': 'puerto.lieu.stockage',
            'lieu_stockage_dest_id': 'puerto.lieu.stockage',
            'priorite_id': 'puerto.priorite',
            'incoterm_id': 'account.incoterms',
            'mode_transport_id': 'puerto.mode.transport',
            'contenant_id': 'puerto.contenant',
            'pays_origine_id': 'res.country',
            'pays_provenance_id': 'res.country',
        }
        for field in m2o:
            val = post.get(field)
            if val and val.isdigit():
                vals[field] = int(val)

        dossier = env['puerto.dossier'].sudo().create(vals)
        return request.redirect(f'/my/dossiers/{dossier.id}')
