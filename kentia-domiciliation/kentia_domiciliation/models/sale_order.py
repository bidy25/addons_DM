from google_currency import convert
import json
from odoo import api, fields, models


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    contract_sequence = fields.Char(string='Contract N°')
    amount_convert = fields.Char(string=' In € ', store=True)

    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        if len(self.order_line.filtered(lambda line: line.product_id.is_creation is True)) > 0:
            self.write({
                'contract_sequence': self.env['ir.sequence'].next_by_code('seq.contract'),
            })
        return res

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