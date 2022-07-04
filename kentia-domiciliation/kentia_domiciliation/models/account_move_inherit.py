from google_currency import convert
import json
from odoo import api, fields, models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    amount_convert = fields.Char(string=' In €', store=True)

    @api.depends('amount_total')
    def _compute_euro(self):
        for rec in self:
            if rec.amount_total != 0:
                if rec.amount_total > 0:
                    val = rec.amount_total
                    conv = convert('MGA', 'EUR', val)
                    data = json.loads(conv)
                    rec.amount_convert = data['amount']
                else:
                    val = rec.amount_total * -1
                    conv = convert('MGA', 'EUR', val)
                    data = json.loads(conv)
                    amount = data['amount'] * -1
                    rec.amount_convert = amount
            else:
                rec.amount_convert = 0
