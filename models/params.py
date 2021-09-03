# -*- coding: utf-8 -*-
from typing import Sequence
from odoo import api, fields, models, _, tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
from datetime import datetime
from odoo.tools.enlettres import convlettres


class OstockArticle(models.Model):
    _name = "ostock.article"
    _description = "Article"
        
    name = fields.Char(string="Nom")