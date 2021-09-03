# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Ostock',
    'version': '1.0',
    'summary': 'GESTION DES STOCK',
    'description': """
        GESTION DES HOPITAUX
        ====================
        Ce logiciel permet la gestion des stock
    """,
    'category': 'Commerce',
    
   
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/paperformat.xml',
        'report/reports.xml',
        'report/reportcaisse.xml',
        'views/params.xml',
        'views/main.xml',
        'views/etat.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
