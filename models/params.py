# -*- coding: utf-8 -*-
from typing import Sequence
# from typing_extensions import Required
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
from datetime import datetime
from odoo.tools.enlettres import convlettres


class OvitasArticle(models.Model):
    _name = "ovitas.article"
    _description = "Article"
    
    def getquantite(self):
        for rec in self:
            entre  = sum(m.quantiterecue  for m in self.env['ovitas.detailsentree'].search([('idarticle', '=', rec.id)]))
            sortie_details  = sum(m.quantitesortie  for m in self.env['ovitas.volumejour.details'].search([('idarticle', '=', rec.id)]))
            sortie_casser  = sum(m.quantitesortie  for m in self.env['ovitas.volumecasserjour'].search([('idarticle', '=', rec.id)]))
            sortie_grossiste  = sum(m.quantitesortie  for m in self.env['ovitas.detailsortie.grossiste'].search([('idarticle', '=', rec.id)]))
            sortie_grossiste_details  = sum(m.quantitesortie  for m in self.env['ovitas.detailsortie.grossiste2'].search([('idarticle', '=', rec.id)]))
            sortie_annexe  = sum(m.quantitesortie  for m in self.env['ovitas.detailsortie.annexe'].search([('idarticle', '=', rec.id)]))
            rec.quantite=entre-sortie_casser-sortie_details-sortie_grossiste-sortie_grossiste_details-sortie_annexe
    
        
    name = fields.Char(string="Article")
    idcategoriearticle = fields.Many2one('ovitas.categoriearticle','Categorie article ')
    idunite = fields.Many2one('ovitas.unite','Unite')
    quantite = fields.Float(string="Quantite", compute=getquantite, readonly=True)
    description = fields.Char(string="Description")
    prix = fields.Float(string="Prix")
    prix_grossiste = fields.Float(string="Prix grossiste")
    prix_grossiste_details = fields.Float(string="Prix grossiste details")
    

class OvitasCategoriearticle(models.Model):
    _name = "ovitas.categoriearticle"
    _description = "Categorie Article"
        
    name = fields.Char(string="Categorie article")
    
class OvitasMagasin(models.Model):
    _name = "ovitas.magasin"
    _description = "Magasin"
        
    name = fields.Char(string="Magasin")
    adresse = fields.Char(string="Adresse")
    lignedemagasin=fields.One2many('ovitas.lignedemagasin','idmagasin')
    
    
class OvitasLigneMagasin(models.Model):
    _name = "ovitas.lignedemagasin"
    _description = "details des articles par magasin"
        
    idmagasin=fields.Many2one('ovitas.magasin','Magasin')
    date = fields.Date(string="Date")
    idarticle = fields.Many2one('ovitas.article','article ')
    idcategoriearticle = fields.Many2one('ovitas.categoriearticle','Categorie article ', related='idarticle.idcategoriearticle')
    motif = fields.Char(string="Motif")
    quantiteentree=fields.Integer(string="Quantité entree")
    quantitesortie=fields.Integer(string="Quantité sortie")
    

class OvitasMouvements(models.Model):
    _name = "ovitas.mouvements"
    _description = "Mouvements de stock"
        
    date = fields.Date(string="Date")
    motif = fields.Char(string="Nom")
    quantiteentree=fields.Integer(string="Quantité entree")
    quantitesortie=fields.Integer(string="Quantité sortie")

    
class OvitasTechnicien(models.Model):
    _name = "ovitas.technicien"
    _description = "Technicien"
        
    name = fields.Char(string="Vendeur")
    cnib = fields.Char(string="N° CNIB")
    telephone = fields.Char(string="Telephone")
  
   
class OvitasFournisseur(models.Model):
    _name = "ovitas.fournisseur"
    _description = "Fournisseur"
        
    name = fields.Char(string="Fournisseur")
    cnib = fields.Char(string="N° CNIB")
    telephone = fields.Char(string="Telephone")

class OvitasUnite(models.Model):
    _name = "ovitas.unite"
    _description = "unite des articles"
        
    name = fields.Char(string="Unite")

class OvitasChantier(models.Model):
    _name = "ovitas.chantier"
    _description = "chantier"
        
    name = fields.Char(string="Chantier")

class OvitasClient(models.Model):
    _name = "ovitas.client"
    _description = "client"
        
    name = fields.Char(string='Nom et Prénom(s)')
    telephone = fields.Char(string='Téléphones')


