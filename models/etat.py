# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class OvitasEtat(models.TransientModel):
    _name = "ovitas.etat"
    _description = "Etats"

    debut = fields.Datetime(string="Date de début", required=True)
    fin = fields.Datetime(string="Date de fin", default=fields.Date.today, required=True)
    idmagasin = fields.Many2one('ovitas.magasin', string="Magasin")
    
    def reportbilan(self):
        data = {'debut': self.debut, 'fin': self.fin, 'magasin': self.idmagasin.id }
        return self.env.ref('ovitas.stock_id').report_action(self, data=data)
    
    def bilan_vente(self):
        data = {'debut': self.debut, 'fin': self.fin, 'magasin': self.idmagasin.id }
        return self.env.ref('ovitas.bilanvente_id').report_action(self, data=data)

    def bilan_appro(self):
        data = {'debut': self.debut, 'fin': self.fin, 'magasin': self.idmagasin.id }
        return self.env.ref('ovitas.bilanappro_id').report_action(self, data=data)


class OvitasAbtractBilan(models.AbstractModel):
    _name = 'report.ovitas.reportbilan_template'
    _description = 'rapport'
    
    def _get_report_values(self, docids, data=None):
        domain = [('state', '=', 'valide'), ('date', '>=', data.get('debut')), ('date', '<=', data.get('fin'))]
        docs = []
        for rec in self.env['ovitas.magasin'].search([]):
            articles = []
            for article in self.env['ovitas.article'].search(domain):
                totalentree  = 0 # som 
        
        return {
            'docs': docs,
            'data': data,
        }


class OvitasAbtractBilanVente(models.AbstractModel):
    _name = 'report.ovitas.bilanvente_template'
    _description = 'bilan des ventes'
    
    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('idmagasin'):
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'), ('idmagasin', '=', data.get('idmagasin'))]
        else :
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'),]  
    
        resultats = []
        montant_total = 0
        
        for rec in self.env['ovitas.sortie'].search(domain):
            montant_total += rec.montant
            val = {
                'name': rec.name,
                'date': rec.date,
                'client':rec.client.name,
                'montant':rec.montant      
            }
            resultats.append(val)
        return {
            'data':data,
            'resultats':resultats,
            'montant_total': montant_total
        }


class OvitasAbtractBilanappro(models.AbstractModel):
    _name = 'report.ovitas.bilanappro_template'
    _description = 'bilan des appro'
    
    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('idmagasin'):
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'), ('idmagasin', '=', data.get('idmagasin'))]
        else :
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'),]  
    
        resultats = []
        
        
        for rec in self.env['ovitas.entree'].search(domain):
            
            val = {
                'name': rec.name,
                'date': rec.date,
                'fournisseur':rec.idfournisseur.name,
                'magasin':rec.idmagasin.name      
            }
            resultats.append(val)
        return {
            'data':data,
            'resultats':resultats,
            
        }