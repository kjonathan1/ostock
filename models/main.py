# -*- coding: utf-8 -*-
# from typing_extensions import required
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from odoo.tools.enlettres import convlettres

class OvitasCompany(models.Model):
    _name = "res.company"
    _description = 'Companies'
    _inherit = "res.company"

    def compute_amount_text(self,montant):
        return convlettres(montant)

    def mtlettre(self,montant):
        return convlettres(montant)
    
    user_ids = fields.Many2many('res.users', 'res_company_users_ovitas', 'cid', 'user_id', string='Accepted Users')

class OvitasEntree(models.Model):
    _name = "ovitas.entree"
    _description = "Entree de stock"
        
    def valider(self):
        for rec in self: 
            for record in self.lignedetailsentree:
                if  record.quantiterecue < 0 :
                    raise UserError(_("Veuillez saisir une quantite superieur à 0!")) 
            self.write({'state':'valide'})
                # rec.MouvementEntreeMagasin()
     
    def MouvementEntreeMagasin(self):
        for rec in self:
            mouvmag=[]
            for record in self.lignedetailsentree:
                    val = {
                        'date':rec.date,
                        'idmagasin':rec.idmagasin.id,
                        'motif':rec.motif,
                        'idarticle':record.idarticle.id,
                        'quantiteentree':record.quantiterecue
                    } 
                    mouvmag.append(val)
            self.env['ovitas.lignedemagasin'].create(mouvmag)   
                          
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('ovitas.entree') or _('New')
        vals['name'] = sequence
        result = super(OvitasEntree, self).create(vals)
        return result

    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    name = fields.Char(string="Reference" , readonly=True)
    motif = fields.Char(string="Motif")
    idfournisseur=fields.Many2one('ovitas.fournisseur','Fournisseur')
    idmagasin=fields.Many2one('ovitas.magasin','Magasin' , required=True)
    lignedetailsentree=fields.One2many('ovitas.detailsentree','idstockentree')
    state = fields.Selection([('brouillon','Commande'), ('valide','Reçu'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')
       

class DetailsEntree(models.Model):
    _name = "ovitas.detailsentree"
    _description="Details des entrées"
    
    
    idstockentree=fields.Many2one('ovitas.entree','Stock entree')
    quantitecommande=fields.Float(string="Quantité Commandée")
    quantiterecue=fields.Float(string="Quantité Reçue")
    idarticle=fields.Many2one('ovitas.article','Article', required=True)
    

class OvitasSortie(models.Model):
    _name = "ovitas.sortie"
    _description = "Sortie de stock"
        
    def valider(self):
        for rec in self: 
            for record in self.lignedetailsortie:
                if  record.quantitesortie < 0 :
                    raise UserError(_("Veuillez saisir une quantite superieur à 0!")) 
                self.write({'state':'valide'}) 
                rec.MouvementSortieMagasin()  
                # Generate and assign the sequence number
                sequence = self.env['ir.sequence'].next_by_code('ovitas.sortie') or _('New')
                self.write({'name': sequence})       
                
    def MouvementSortieMagasin(self):
        for rec in self:
            mouvmag=[]
            for record in self.lignedetailsortie:
                    val = {
                        'date':rec.date,
                        'idmagasin':rec.idmagasin.id,
                        'motif':rec.motif,
                        'idarticle':record.idarticle.id,
                        'quantitesortie':record.quantitesortie
                    } 
                    mouvmag.append(val)
            self.env['ovitas.lignedemagasin'].create(mouvmag)   
    
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})

    # @api.model
    # def create(self, vals):
    #     sequence = self.env['ir.sequence'].next_by_code('ovitas.sortie') or _('New')
    #     vals['name'] = sequence
    #     result = super(OvitasSortie, self).create(vals)
    #     return result

    @api.model
    def create(self, vals):
        # Do not assign the sequence number here
        result = super(OvitasSortie, self).create(vals)
        return result

    def generate_invoice_number(self):
        # Generate and assign the sequence number
        sequence = self.env['ir.sequence'].next_by_code('ovitas.sortie') or _('New')
        self.write({'name': sequence})


    @api.depends('lignedetailsortie.idarticle', 'lignedetailsortie.pu', 'lignedetailsortie.quantitesortie', 'lignedetailsortie.longueur', 'lignedetailsortie.hauteur', 'lignedetailsortie.remise', 'remise', 'lignedetailspaiement.montant', 'montant_paye')            
    def get_montant(self):
        pass
        # for rec in self:
        #     montant = 0
        #     montant_paye = 0
        #     for record in rec.lignedetailsortie:
        #         record.pu = record.idarticle.prix

        #         if record.idarticle.idcategoriearticle.name.lower() in "verre":
        #             record.quantitesortie = record.longueur * record.hauteur * record.piece / 10000
        #             record.montant = (record.pu - record.remise) * record.quantitesortie
        #             montant += record.montant
        #         else:
        #             record.montant = (record.pu - record.remise) * record.quantitesortie
        #             montant += record.montant
               
        #     rec.montantnet = montant
        #     rec.montant = montant - rec.remise
        #     for record in rec.lignedetailspaiement:
        #         montant_paye += record.montant
        #     rec.montant_paye = montant_paye
        #     rec.reste = rec.montant - rec.montant_paye


    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    name = fields.Char(string="Reference", readonly=True)
    client = fields.Many2one('ovitas.client', string='Client')
    telephone = fields.Char(string='Téléphones', related='client.telephone', readonly=False)
    motif = fields.Char(string="Objet")
    idtechnicien=fields.Many2one('ovitas.technicien','Vendeur')
    idchantier=fields.Many2one('ovitas.chantier','Chantier')
    montantnet = fields.Float(string='Montant Net', digits=(16,0), compute=get_montant, store=True)
    montant = fields.Float(string='Total Général', digits=(16,0), compute=get_montant, store=True)
    remise = fields.Float('Remise', default=0)
    montant_paye = fields.Float('Montant payé', default=0, digits=(16,0), compute=get_montant, store=True)
    reste = fields.Float('Reste à payer', default=0, digits=(16,0), compute=get_montant, store=True)
    idmagasin = fields.Many2one('ovitas.magasin','Magasin', required=True)
    lignedetailsortie = fields.One2many('ovitas.detailsortie','idstocksortie')
    lignedetailspaiement = fields.One2many('ovitas.detailspaiement','idstocksortie')
    state = fields.Selection([('brouillon','Devis'), ('valide','Payé'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')

    
class DetailsSortie(models.Model):
    _name = "ovitas.detailsortie"
    _description="Details des sorties"
    
    idstocksortie=fields.Many2one('ovitas.sortie','Stock sortie')
    quantitesortie=fields.Float(string="Quantité sortie", default=1)
    idarticle=fields.Many2one('ovitas.article','Désignation', required=True)
    remise = fields.Float('Remise', default=0, digits=(16,0))
    pu = fields.Float('Prix unitaire', required=True, digits=(16,0))
    montant = fields.Float('Montant', digits=(16,0), store=True)
    longueur = fields.Float('L')
    hauteur = fields.Float('H')
    piece = fields.Float('Nbre', digits=(16,0), store=True)


class DetailsPaiement(models.Model):
    _name = "ovitas.detailspaiement"
    _description="Details des paiement de sortie (vente)"
    
    idstocksortie=fields.Many2one('ovitas.sortie','Stock sortie')
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    montant = fields.Float('Montant', digits=(16,0), store=True)



class OvitasSortieDetails(models.Model):
    _name = "ovitas.sortie.details"
    _description = "Sortie de stock"
    # _inherit = "ovitas.sortie"

    def valider(self):
          for rec in self: 
            for record in self.lignedetailsortie:
                if  record.quantitesortie < 0 :
                    raise UserError(_("Veuillez saisir une quantite superieur à 0!")) 
                self.write({'state':'valide'})  
                # Generate and assign the sequence number
                sequence = self.env['ir.sequence'].next_by_code('ovitas.sortie') or _('New')
                self.write({'name': sequence})    
    
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})

    @api.model
    def create(self, vals):
        # sequence = self.env['ir.sequence'].next_by_code('ovitas.sortie') or _('New')
        # vals['name'] = sequence
        # result = super(OvitasSortieDetails, self).create(vals)
        # return result
        result = super(OvitasSortieDetails, self).create(vals)
        return result

    @api.depends('lignedetailsortie.idarticle', 'lignedetailsortie.pu', 'lignedetailsortie.quantitesortie', 'lignedetailsortie.longueur', 'lignedetailsortie.hauteur', 'lignedetailsortie.remise', 'remise', 'montant_paye')            
    def get_montant(self):
        for rec in self:
            montant = 0
            montant_paye = 0
            for record in rec.lignedetailsortie:
                record.pu = record.idarticle.prix

                record.quantitesortie = record.longueur * record.hauteur * record.piece / 10000
                record.montant = (record.pu - record.remise) * record.quantitesortie
                montant += record.montant
               
            rec.montantnet = montant
            rec.montant = montant - rec.remise
            for record in rec.lignedetailspaiement:
                montant_paye += record.montant
            rec.montant_paye = montant_paye
            rec.reste = rec.montant - rec.montant_paye
    
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    name = fields.Char(string="Reference", readonly=True)
    client = fields.Many2one('ovitas.client', string='Client')
    telephone = fields.Char(string='Téléphones', related='client.telephone', readonly=False)
    motif = fields.Char(string="Objet")
    idtechnicien=fields.Many2one('ovitas.technicien','Vendeur')
    idchantier=fields.Many2one('ovitas.chantier','Chantier')
    montantnet = fields.Float(string='Montant Net', digits=(16,0), compute=get_montant, store=True)
    montant = fields.Float(string='Total Général', digits=(16,0), compute=get_montant, store=True)
    remise = fields.Float('Remise', default=0)
    montant_paye = fields.Float('Montant payé', default=0, digits=(16,0), compute=get_montant, store=True)
    reste = fields.Float('Reste à payer', default=0, digits=(16,0), compute=get_montant, store=True)
    idmagasin = fields.Many2one('ovitas.magasin','Magasin', required=True)
    lignedetailspaiement = fields.One2many('ovitas.detailspaiement','idstocksortie')
    state = fields.Selection([('brouillon','Devis'), ('valide','Payé'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')
    lignedetailsortie = fields.One2many('ovitas.detailsortie.details','idstocksortie')


class OvitasSortieGrossiste(models.Model):
    _name = "ovitas.sortie.grossiste"
    _description = "Sortie de stock"
    # _inherit = "ovitas.sortie"

    def valider(self):
          for rec in self: 
            for record in self.lignedetailsortie:
                if  record.quantitesortie < 0 :
                    raise UserError(_("Veuillez saisir une quantite superieur à 0!")) 
                self.write({'state':'valide'})    
    
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('ovitas.sortie') or _('New')
        vals['name'] = sequence
        result = super(OvitasSortieGrossiste, self).create(vals)
        return result

    @api.depends('lignedetailsortie.idarticle', 'lignedetailsortie.pu', 'lignedetailsortie.quantitesortie', 'lignedetailsortie.remise', 'remise', 'montant_paye')            
    def get_montant(self):
        for rec in self:
            montant = 0
            montant_paye = 0
            for record in rec.lignedetailsortie:
                record.pu = record.idarticle.prix_grossiste

                record.montant = (record.pu - record.remise) * record.quantitesortie
                montant += record.montant
               
            rec.montantnet = montant
            rec.montant = montant - rec.remise
            for record in rec.lignedetailspaiement:
                montant_paye += record.montant
            rec.montant_paye = montant_paye
            rec.reste = rec.montant - rec.montant_paye

    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    name = fields.Char(string="Reference", readonly=True)
    client = fields.Many2one('ovitas.client', string='Client')
    telephone = fields.Char(string='Téléphones', related='client.telephone', readonly=False)
    motif = fields.Char(string="Objet")
    idtechnicien=fields.Many2one('ovitas.technicien','Vendeur')
    idchantier=fields.Many2one('ovitas.chantier','Chantier')
    montantnet = fields.Float(string='Montant Net', digits=(16,0), compute=get_montant, store=True)
    montant = fields.Float(string='Total Général', digits=(16,0), compute=get_montant, store=True)
    remise = fields.Float('Remise', default=0)
    montant_paye = fields.Float('Montant payé', default=0, digits=(16,0), compute=get_montant, store=True)
    reste = fields.Float('Reste à payer', default=0, digits=(16,0), compute=get_montant, store=True)
    idmagasin = fields.Many2one('ovitas.magasin','Magasin', required=True)
    lignedetailspaiement = fields.One2many('ovitas.detailspaiement','idstocksortie')
    state = fields.Selection([('brouillon','Devis'), ('valide','Payé'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')
    lignedetailsortie = fields.One2many('ovitas.detailsortie.grossiste','idstocksortie')
   


class OvitasSortieAnnexe(models.Model):
    _name = "ovitas.sortie.annexe"
    _description = "Sortie de stock"
    # _inherit = "ovitas.sortie"

    def valider(self):
          for rec in self: 
            for record in self.lignedetailsortie:
                if  record.quantitesortie < 0 :
                    raise UserError(_("Veuillez saisir une quantite superieur à 0!")) 
                self.write({'state':'valide'})    
    
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('ovitas.sortie.annexe') or _('New')
        vals['name'] = sequence
        result = super(OvitasSortieAnnexe, self).create(vals)
        return result

    @api.depends('lignedetailsortie.idarticle', 'lignedetailsortie.pu', 'lignedetailsortie.quantitesortie', 'lignedetailsortie.remise', 'remise', 'montant_paye')            
    def get_montant(self):
        for rec in self:
            montant = 0
            montant_paye = 0
            for record in rec.lignedetailsortie:
                record.pu = record.idarticle.prix_grossiste

                record.montant = (record.pu - record.remise) * record.quantitesortie
                montant += record.montant
               
            rec.montantnet = montant
            rec.montant = montant - rec.remise
            for record in rec.lignedetailspaiement:
                montant_paye += record.montant
            rec.montant_paye = montant_paye
            rec.reste = rec.montant - rec.montant_paye

    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    name = fields.Char(string="Reference", readonly=True)
    client = fields.Many2one('ovitas.client', string='Client')
    telephone = fields.Char(string='Téléphones', related='client.telephone', readonly=False)
    motif = fields.Char(string="Objet")
    idtechnicien=fields.Many2one('ovitas.technicien','Vendeur')
    idchantier=fields.Many2one('ovitas.chantier','Chantier')
    montantnet = fields.Float(string='Montant Net', digits=(16,0), compute=get_montant, store=True)
    montant = fields.Float(string='Total Général', digits=(16,0), compute=get_montant, store=True)
    remise = fields.Float('Remise', default=0)
    montant_paye = fields.Float('Montant payé', default=0, digits=(16,0), compute=get_montant, store=True)
    reste = fields.Float('Reste à payer', default=0, digits=(16,0), compute=get_montant, store=True)
    idmagasin = fields.Many2one('ovitas.magasin','Magasin', required=True)
    lignedetailsortie = fields.One2many('ovitas.detailsortie.annexe','idstocksortie')
    lignedetailspaiement = fields.One2many('ovitas.detailspaiement','idstocksortie')
    state = fields.Selection([('brouillon','Devis'), ('valide','Payé'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')

class DetailsSortieDetails(models.Model):
    _name = "ovitas.detailsortie.details"
    _description="Details des sorties"
    _inherit = "ovitas.detailsortie"

    idstocksortie=fields.Many2one('ovitas.sortie.details','Stock sortie')
    quantitesortie=fields.Float(string="Quantité sortie", default=1)
    idarticle=fields.Many2one('ovitas.article','Désignation', required=True)
    remise = fields.Float('Remise', default=0, digits=(16,0))
    pu = fields.Float('Prix unitaire', required=True, digits=(16,0))
    montant = fields.Float('Montant', digits=(16,0), store=True)
    longueur = fields.Float('L')
    hauteur = fields.Float('H')
    piece = fields.Float('Nbre', digits=(16,0), store=True)


class DetailsSortieGrossiste(models.Model):
    _name = "ovitas.detailsortie.grossiste"
    _description="Details des sorties"
    _inherit = "ovitas.detailsortie"

    idstocksortie=fields.Many2one('ovitas.sortie.grossiste','Stock sortie')
    quantitesortie=fields.Float(string="Quantité sortie", default=1)
    idarticle=fields.Many2one('ovitas.article','Désignation', required=True)
    remise = fields.Float('Remise', default=0, digits=(16,0))
    pu = fields.Float('Prix unitaire', required=True, digits=(16,0))
    montant = fields.Float('Montant', digits=(16,0), store=True)

class DetailsSortieAnnexe(models.Model):
    _name = "ovitas.detailsortie.annexe"
    _description="Details des sorties"
    # _inherit = "ovitas.detailsortie"

    idstocksortie=fields.Many2one('ovitas.sortie.annexe','Stock sortie')
    quantitesortie=fields.Float(string="Quantité sortie", default=1)
    idarticle=fields.Many2one('ovitas.article','Désignation', required=True)
    remise = fields.Float('Remise', default=0, digits=(16,0))
    pu = fields.Float('Prix unitaire', required=True, digits=(16,0))
    montant = fields.Float('Montant', digits=(16,0), store=True)


class OvitasVolumeUtiliserJour(models.Model):
    _name = "ovitas.volumejour"
    _description = "Utilisation des volumres par jours"

    def valider(self):
        self.write({'state':'valide'})    
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})

    name = fields.Date(string="Date", required=True, default=fields.Date.today)
    idmagasin=fields.Many2one('ovitas.magasin','Magasin' , required=True)
    lignedetails=fields.One2many('ovitas.volumejour.details','idvolumejour')
    lignedetailscasser=fields.One2many('ovitas.volumecasserjour','idvolumecasserjour')
    state = fields.Selection([('brouillon','Brouillon'), ('valide','Valide'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')
    
class OvitasVolumeUtiliserJourDetails(models.Model):
    _name = "ovitas.volumejour.details"
    _description = "Utilisation des volumres par jours details"

    idvolumejour=fields.Many2one('ovitas.volumejour','Volume utiliser jour')
    idarticle = fields.Many2one('ovitas.article','Désignation', required=True)
    quantitesortie=fields.Float(string="Quantité sortie", default=0)

class OvitasVolumeCasserJourDetails(models.Model):
    _name = "ovitas.volumecasserjour"
    _description = "repertorier les volume casser par jour"

    idvolumecasserjour=fields.Many2one('ovitas.volumejour','Volume jour')
    idarticle = fields.Many2one('ovitas.article','Désignation', required=True)
    quantitesortie=fields.Float(string="Quantité cassée", default=0)

class OvitasSortieGrossiste2(models.Model):
    _name = "ovitas.sortie.grossiste2"
    _description = "Sortie de stock vente grossite details"
    # _inherit = "ovitas.sortie"

    def valider(self):
          for rec in self: 
            for record in self.lignedetailsortie:
                if  record.quantitesortie < 0 :
                    raise UserError(_("Veuillez saisir une quantite superieur à 0!")) 
                self.write({'state':'valide'})    
    
    def brouillon(self):
        self.write({'state':'brouillon'})
    def annuler(self):
        self.write({'state':'annule'})

    @api.model
    def create(self, vals):
        sequence = self.env['ir.sequence'].next_by_code('ovitas.sortie') or _('New')
        vals['name'] = sequence
        result = super(OvitasSortieGrossiste2, self).create(vals)
        return result

    @api.depends('lignedetailsortie.idarticle', 'lignedetailsortie.pu', 'lignedetailsortie.quantitesortie', 'lignedetailsortie.remise', 'remise', 'montant_paye')            
    def get_montant(self):
        for rec in self:
            montant = 0
            montant_paye = 0
            for record in rec.lignedetailsortie:
                record.pu = record.idarticle.prix_grossiste_details

                record.montant = (record.pu - record.remise) * record.quantitesortie
                montant += record.montant
               
            rec.montantnet = montant
            rec.montant = montant - rec.remise
            for record in rec.lignedetailspaiement:
                montant_paye += record.montant
            rec.montant_paye = montant_paye
            rec.reste = rec.montant - rec.montant_paye

    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    name = fields.Char(string="Reference", readonly=True)
    client = fields.Many2one('ovitas.client', string='Client')
    telephone = fields.Char(string='Téléphones', related='client.telephone', readonly=False)
    motif = fields.Char(string="Objet")
    idtechnicien=fields.Many2one('ovitas.technicien','Vendeur')
    idchantier=fields.Many2one('ovitas.chantier','Chantier')
    montantnet = fields.Float(string='Montant Net', digits=(16,0), compute=get_montant, store=True)
    montant = fields.Float(string='Total Général', digits=(16,0), compute=get_montant, store=True)
    remise = fields.Float('Remise', default=0)
    montant_paye = fields.Float('Montant payé', default=0, digits=(16,0), compute=get_montant, store=True)
    reste = fields.Float('Reste à payer', default=0, digits=(16,0), compute=get_montant, store=True)
    idmagasin = fields.Many2one('ovitas.magasin','Magasin', required=True)
    lignedetailspaiement = fields.One2many('ovitas.detailspaiement','idstocksortie')
    state = fields.Selection([('brouillon','Devis'), ('valide','Payé'),('annule','Annulé')], string='Etat', readonly=True, default='brouillon')
    lignedetailsortie = fields.One2many('ovitas.detailsortie.grossiste2','idstocksortie')

class DetailsSortieGrossiste2(models.Model):
    _name = "ovitas.detailsortie.grossiste2"
    _description="Details des sorties"
    _inherit = "ovitas.detailsortie"

    idstocksortie=fields.Many2one('ovitas.sortie.grossiste2','Stock sortie')
    quantitesortie=fields.Float(string="Quantité sortie", default=1)
    idarticle=fields.Many2one('ovitas.article','Désignation', required=True)
    remise = fields.Float('Remise', default=0, digits=(16,0))
    pu = fields.Float('Prix unitaire', required=True, digits=(16,0))
    montant = fields.Float('Montant', digits=(16,0), store=True)
