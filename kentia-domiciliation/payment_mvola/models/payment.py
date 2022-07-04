# coding: utf-8

import logging

from odoo import api, fields, models
from werkzeug import urls

_logger = logging.getLogger(__name__)


class MvolaAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('mvola', 'MVOLA')])
    mvola_api_username = fields.Char('Username', groups='base.group_user', required_if_provider='mvola')
    mvola_api_password = fields.Char('Password', groups='base.group_user', required_if_provider='mvola')
    mvola_hashcode = fields.Char('HashCode', groups='base.group_user', required_if_provider='mvola')

    @api.model
    def _get_mvola_urls(self, state):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if state == 'enabled':
            return {
                'mvola_base_url': "https://www.telma.net/mpgw/v2",
                'mvola_ws_url': "https://www.telma.net/mpgw/v2/ws/MPGwApi",
                'mvola_transaction_url': "https://www.telma.net/mpgw/v2/transaction/",
                'api_version': '2.0.0',
                'mvola_form_url': urls.url_join(base_url, '/payment/mv')
            }
        else:
            return {
                'mvola_base_url': "https://www.telma.net/mpgw/v2",
                'mvola_ws_url': "https://www.telma.net/mpgw/v2/ws/MPGwApi",
                'mvola_transaction_url': "https://www.telma.net/mpgw/v2/transaction/",
                'api_version': '2.0.0',
                'mvola_form_url': urls.url_join(base_url, '/payment/mv')
            }

    def mvola_compute_fees(self, amount, currency_id, country_id):
        # compute fees for Mvola Transaction
        return 0.0

    def mvola_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        mvola_tx_values = dict(values)
        mvola_tx_values.update({
            'cmd': '_xclick',
            'item_name': '%s: %s' % (self.company_id.name, values['reference']),
            'item_number': values['reference'],
            'amount': values['amount'],
            'currency_code': values['currency'] and values['currency'].name or '',
            'address1': values.get('partner_address'),
            'city': values.get('partner_city'),
            'country': values.get('partner_country') and values.get('partner_country').code or '',
            'state': values.get('partner_state') and (values.get('partner_state').code or values.get('partner_state').name) or '',
            'email': values.get('partner_email'),
            'zip_code': values.get('partner_zip'),
            'first_name': values.get('partner_first_name'),
            'last_name': values.get('partner_last_name')
        })
        return mvola_tx_values

    def mvola_get_form_action_url(self):
        return self._get_mvola_urls(self.state)['mvola_form_url']


class TxMvola(models.Model):
    _inherit = 'payment.transaction'

    mvola_token_id = fields.Char(string='Mvola Token ID')

    @api.model
    def _mvola_form_get_tx_from_data(self, data):
        reference = data.get('item_number')
        txs = self.env['payment.transaction'].search([('reference', '=', reference)])
        return txs[0]

    def _mvola_form_validate(self, data):
        status = data.get('payment_status')
        res = {
            'acquirer_reference': data.get('txn_id'),
            'paypal_txn_type': data.get('payment_type'),
        }
        return res
