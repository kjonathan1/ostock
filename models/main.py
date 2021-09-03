# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError

class OstockEntree(models.Model):
    _name = "ostock.entree"
    _description = "Entree de stock"
        
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    name = fields.Char(string="Nom")


