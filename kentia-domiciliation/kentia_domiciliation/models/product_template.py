# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    is_creation = fields.Boolean(string='Is creation type')
