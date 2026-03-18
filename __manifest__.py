# -*- coding: utf-8 -*-
{
    'name': 'Puerto Transit',
    'version': '19.0.1.0',
    'summary': 'Gestion de transit douanier avec portail client',
    'description': 'Module complet de gestion de transit douanier (import/export) avec portail client.',
    'author': 'Dynamic Horizon',
    'website': 'https://www.dynamichorizon.ma',
    'category': 'Logistics',
    'depends': ['base', 'mail', 'website', 'portal', 'account', 'uom', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/puerto_config_views.xml',
        'views/puerto_dossier_views.xml',
        'views/puerto_dossier_facture_views.xml',
        'views/puerto_dossier_charge_views.xml',
        'views/portal_templates.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'puerto_transit/static/src/css/portal.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
