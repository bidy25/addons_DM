# coding: utf-8

import logging
import requests
import json
from odoo import api, fields, models
from werkzeug import urls

_logger = logging.getLogger(__name__)


class OrangeMoneyAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('orange_money', 'Orange Money')])
    om_authorization = fields.Char('Authorization', groups='base.group_user', required_if_provider='orange_money')
    om_merchant_key = fields.Char('Merchant Key', groups='base.group_user', required_if_provider='orange_money')
    om_token_type = fields.Char('Token Type', groups='base.group_user', required_if_provider='orange_money')
    om_access_token = fields.Char('Access Token', groups='base.group_user', required_if_provider='orange_money')
    om_expires_in = fields.Char('Expires In', groups='base.group_user', required_if_provider='orange_money')
    om_currency = fields.Char('Currency', groups='base.group_user', required_if_provider='orange_money', compute='_toggle_currency'
                              , store=True)

    @api.model
    def _get_orange_money_urls(self, state):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if state == 'test':
            return {
                'om_token_url': "https://api.orange.com/oauth/v2/token",
                'om_webpayment_url': "https://api.orange.com/orange-money-webpay/dev/v1/webpayment",
                'om_transaction_url': "https://api.orange.com/orange-money-webpay/dev/v1/transactionstatus",
                'om_form_url': urls.url_join(base_url, '/payment/om')
            }
        else:
            return {
                'om_token_url': "https://api.orange.com/oauth/v2/token",
                'om_webpayment_url': "https://api.orange.com/orange-money-webpay/mg/v1/webpayment",
                'om_transaction_url': "https://api.orange.com/orange-money-webpay/mg/v1/transactionstatus",
                'om_form_url': urls.url_join(base_url, '/payment/om/')
            }

    #@api.multi
    def orange_money_compute_fees(self, amount, currency_id, country_id):
        # compute fees for Orange Money Transaction
        return 0.0

    #@api.multi
    def orange_money_form_generate_values(self, values):
        orange_money_tx_values = dict(values)
        # test
        orange_money_tx_values.update({
            'cmd': '_xclick',
            #    'business': self.paypal_email_account,
            'item_name': '%s: %s' % (self.company_id.name, values['reference']),
            'item_number': values['reference'],
            'amount': values['amount'],
            'currency_code': values['currency'] and values['currency'].name or '',
            'address1': values.get('partner_address'),
            'city': values.get('partner_city'),
            'country': values.get('partner_country') and values.get('partner_country').code or '',
            'state': values.get('partner_state') and (
                    values.get('partner_state').code or values.get('partner_state').name) or '',
            'email': values.get('partner_email'),
            'zip_code': values.get('partner_zip'),
            'first_name': values.get('partner_first_name'),
            'last_name': values.get('partner_last_name'),
        })
        return orange_money_tx_values

    # @api.multi
    def orange_money_get_form_action_url(self):
        return self._get_orange_money_urls(self.state)['om_form_url']

    def get_orange_money_token(self):
        token_url = self._get_orange_money_urls(self.state)['om_token_url']
        headers = {
            'Authorization': self.om_authorization,
        }
        data = {
            'grant_type': 'client_credentials'
        }
        response = requests.post(url=token_url, headers=headers, data=data)
        if response:
            self.write({
                "om_token_type": response.json().get('token_type'),
                "om_access_token": response.json().get('access_token'),
                "om_expires_in": response.json().get('expires_in')
            })

    @api.depends('state')
    def _toggle_currency(self):
        for payment in self:
            if payment.provider == 'orange_money':
                if payment.state == 'test':
                    payment.om_currency = 'OUV'
                else:
                    payment.om_currency = 'MGA'


class TxOrangeMoney(models.Model):
    _inherit = 'payment.transaction'

    om_notif_token = fields.Char(string='Notif Token')
    om_pay_token = fields.Char(string='Pay Token')

    @api.model
    def _orange_money_form_get_tx_from_data(self, data):
        reference = data.get('item_number')
        txs = self.env['payment.transaction'].search([('reference', '=', reference)])
        return txs[0]

    # @api.multi
    def _orange_money_form_get_invalid_parameters(self, data):
        print("get invalid param")
        pass

    # @api.multi
    def _orange_money_form_validate(self, data):
        status = data.get('payment_status')
        res = {
            'acquirer_reference': data.get('txn_id'),
            'paypal_txn_type': data.get('payment_type'),
        }
