# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class ovitas_etat(models.TransientModel):
    _name = "ovitas.etat"
    _description = "Etats"

    debut = fields.Date(string="Date de debut", required=True)
    fin = fields.Date(string="Date de fin", required=True)
    idmagasin = fields.Many2one('ovitas.magasin', 'Magasin')
    
    def mouvement_report(self):
        data = {'debut': self.debut, 'fin': self.fin , 'idmagasin': self.idmagasin.id}
        return self.env.ref('ovitas.stock_id').report_action(self, data=data)

    def bilan_vente_details(self):
        data = {'debut': self.debut, 'fin': self.fin , 'idmagasin': self.idmagasin.id}
        return self.env.ref('ovitas.bilanventedetails_id').report_action(self, data=data)
    
    def bilan_vente_grossiste(self):
        data = {'debut': self.debut, 'fin': self.fin , 'idmagasin': self.idmagasin.id}
        return self.env.ref('ovitas.bilanventegrossiste_id').report_action(self, data=data)
    
    def bilan_vente_annexe(self):
        data = {'debut': self.debut, 'fin': self.fin , 'idmagasin': self.idmagasin.id}
        return self.env.ref('ovitas.bilanventeannexe_id').report_action(self, data=data)

    def bilan_appro(self):
        data = {'debut': self.debut, 'fin': self.fin , 'idmagasin': self.idmagasin.id}
        return self.env.ref('ovitas.bilanappro_id').report_action(self, data=data)


class ostation_abstractetatstock(models.AbstractModel):
    _name = 'report.ovitas.stock'
    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('idmagasin'):
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'), ('idmagasin', '=', data.get('idmagasin'))]
        else :
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'),]  
    
        resultats = []
        quantiterecue = 0
        quantitesortie = 0
        
        for rec in self.env['ovitas.article'].search([]):
            quantiterecue = sum(m.quantiterecue  for m in self.env['ovitas.detailsentree'].search([('idarticle', '=', rec.id)]))
            # quantitesortie = sum(m.quantitesortie  for m in self.env['ovitas.detailsortie'].search([('idarticle', '=', rec.id)]))
            qte_manuel_jour = sum(m.quantitesortie  for m in self.env['ovitas.volumejour.details'].search([('idarticle', '=', rec.id)]))
            qte_casser = sum(m.quantitesortie  for m in self.env['ovitas.volumecasserjour'].search([('idarticle', '=', rec.id)]))
            qte_grossiste = sum(m.quantitesortie  for m in self.env['ovitas.detailsortie.grossiste'].search([('idarticle', '=', rec.id)]))
            qte_grossiste_details = sum(m.quantitesortie  for m in self.env['ovitas.detailsortie.grossiste2'].search([('idarticle', '=', rec.id)]))
            qte_annexe = sum(m.quantitesortie  for m in self.env['ovitas.detailsortie.annexe'].search([('idarticle', '=', rec.id)]))
            
            val = {
                'name':rec.name,
                'quantiterecue':quantiterecue,
                # 'quantitesortie':quantitesortie,
                'qte_manuel_jour':qte_manuel_jour,
                'qte_casser':qte_casser,
                'qte_grossiste':qte_grossiste,
                'qte_grossiste_details':qte_grossiste_details,
                'qte_annexe':qte_annexe,
                'variation':quantiterecue - qte_manuel_jour - qte_casser - qte_grossiste - qte_grossiste_details - qte_annexe       
            }
            resultats.append(val)
        return {
            'data':data,
            'resultats':resultats
        }


class ovitas_abstractbilanventedetails(models.AbstractModel):
    _name = 'report.ovitas.bilanventedetails'
    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('idmagasin'):
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'), ('idmagasin', '=', data.get('idmagasin'))]
        else :
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'),]  
    
        resultats = []
        montant_total = 0
        
        for rec in self.env['ovitas.sortie.details'].search(domain):
            montant_total += rec.montant
            val = {
                'name': rec.name,
                'date': rec.date,
                'client':rec.client.name,
                'montant':rec.montant      
            }
            resultats.append(val)
        for rec in self.env['ovitas.sortie.grossiste'].search(domain):
            montant_total += rec.montant
            val = {
                'name': rec.name,
                'date': rec.date,
                'client':rec.client.name,
                'montant':rec.montant      
            }
            resultats.append(val)
        for rec in self.env['ovitas.sortie.grossiste2'].search(domain):
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

class ovitas_abstractbilanventegrossiste(models.AbstractModel):
    _name = 'report.ovitas.bilanventegrossiste'
    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('idmagasin'):
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'), ('idmagasin', '=', data.get('idmagasin'))]
        else :
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'),]  
    
        resultats = []
        montant_total = 0
        
        for rec in self.env['ovitas.sortie.grossiste'].search(domain):
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

class ovitas_abstractbilanventeannexe(models.AbstractModel):
    _name = 'report.ovitas.bilanventeannexe'
    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('idmagasin'):
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'), ('idmagasin', '=', data.get('idmagasin'))]
        else :
            domain = [('date', '>=', data.get('debut')), ('date', '<=', data.get('fin')), ('state', '=', 'valide'),]  
    
        resultats = []
        montant_total = 0
        
        for rec in self.env['ovitas.sortie.annexe'].search(domain):
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
            
class ovitas_abstractbilanappro(models.AbstractModel):
    _name = 'report.ovitas.bilanappro'
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


