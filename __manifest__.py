# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Ovitas',
    'version': '1.0',
    'summary': 'GESTION DES STOCKS',
    'description': """
        GESTION DES STOCKS
        ====================
        Ce logiciel permet la gestion des stock
    """,
    'category': 'Commerce',
    
   
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/paperformat.xml',
        'report/reportbilanvente.xml',
        'report/reportbilanventedetails.xml',
        'report/reportbilanventegrossiste.xml',
        'report/reportbilanventeannexe.xml',
        'report/reportbilanappro.xml',
        'report/stock.xml',
        'report/report.xml',
        'report/reportentree.xml',
        'report/reportsortie.xml',
        'report/reportsortie_details.xml',
        'report/reportsortie_details_facture.xml',
        'report/reportsortie_details_bl.xml',
        'report/reportsortie_grossiste.xml',
        'report/reportsortie_grossiste_bl.xml',
        'report/reportsortie_grossiste_facture.xml',
        'report/reportsortie_grossiste2_bl.xml',
        'report/reportsortie_grossiste2_facture.xml',
        'report/reportsortie_annexe.xml',
        'report/reportfacture.xml',
        'report/reportarticle.xml',
        'report/reportetatstock.xml',
        'views/params.xml',
        'views/main.xml',
        # 'views/etat.xml',
        'wizard/etat.xml',
        'views/menu.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
