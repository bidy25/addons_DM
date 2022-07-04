# -*- coding: utf-8 -*-

import logging
import json
import werkzeug
import requests
from odoo import http
from odoo.http import request
import random

_logger = logging.getLogger(__name__)

class OrangeMoneyController(http.Controller):
    _notify_url = '/payment/om/notif'
    _return_url = '/payment/om/return'
    _cancel_url = '/payment/om/cancel'
    _error_url = '/payment/om/error'


    @http.route('/payment/om/', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def payment_om_process(self, **post):
        return self.executePayment(post);

    def executePayment(self, post):
        reference = post.get('item_number')
        tx = None
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if reference:
            tx = request.env['payment.transaction'].search([('reference', '=', reference)]).sudo()
            om_urls = request.env['payment.acquirer']._get_orange_money_urls(tx and tx.acquirer_id.state or 'prod')
            webpayment_url = om_urls.get('om_webpayment_url')
            headers = {
                'Authorization': '%s %s' % (tx.acquirer_id.om_token_type, tx.acquirer_id.om_access_token),
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            om_data = {
                'merchant_key': tx.acquirer_id.om_merchant_key,
                'currency': tx.acquirer_id.om_currency,
                'order_id': str(post.get('item_number')),
                "amount": post.get('amount'),
                'return_url': werkzeug.urls.url_join(base_url, self._return_url),
                'cancel_url': werkzeug.urls.url_join(base_url, self._cancel_url),
                'notif_url': werkzeug.urls.url_join(base_url, self._notify_url),
                'lang': 'fr',
                'reference': '100935',
            }
            data = requests.post(url=webpayment_url, headers=headers, data=json.dumps(om_data))
            response = data.json();

            return self.executeRedirection(tx, response, post)
        return werkzeug.utils.redirect(werkzeug.urls.url_join(base_url, self._error_url))

    def executeRedirection(self, tx, response, posted):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if response.get('message') == 'OK':
            payment_url = response.get('payment_url')
            notif_token = response.get('notif_token')
            pay_token = response.get('pay_token')
            tx.sudo().write({
                'om_notif_token': notif_token,
                'om_pay_token': pay_token,
            })
            return werkzeug.utils.redirect(payment_url)
        if response.get('message') == 'Invalid credentials':
            tx.acquirer_id.get_orange_money_token()
            return self.executePayment(posted);
        return werkzeug.utils.redirect(werkzeug.urls.url_join(base_url, self._error_url))

    @http.route('/payment/om/return', type='http', auth='public', methods=['GET'], csrf=False)
    def payment_om_return(self, **post):
        # to do : redirect according to payment type : e-commerce - customer portal
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return werkzeug.utils.redirect(werkzeug.urls.url_join(base_url, '/shop/confirmation'))

    @http.route('/payment/om/notif', type='json', auth='public', csrf=False)
    def payment_om_notif(self, **args):
        post=json.loads(request.httprequest.data)
        _logger.info('Orange Money notification --------------------------------')
        status = post.get('status')
        if status == 'SUCCESS':
            notif_token = post.get('notif_token')
            tx = request.env['payment.transaction'].sudo().search([('om_notif_token', '=', notif_token)],                                                                order='reference desc', limit=1)
            if tx:
                headers = {
                    'Authorization': '%s %s' % (tx.acquirer_id.om_token_type, tx.acquirer_id.om_access_token),
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                # check data
                check_data = {
                    'order_id': tx.reference,
                    'amount': tx.amount,
                    'pay_token': tx.om_pay_token,
                }
                om_urls = request.env['payment.acquirer']._get_orange_money_urls(tx and tx.acquirer_id.state or 'prod')
                response = requests.post(url=om_urls.get('om_transaction_url'), headers=headers,
                                         data=json.dumps(check_data))

                if response.json().get('status') == 'SUCCESS':
                    tx.write({
                        'acquirer_reference': response.json().get('txnid')
                    })
                    tx._set_transaction_done()
                    tx._post_process_after_done()
                    sale_orders = tx.sale_order_ids;
                    for sale_order in sale_orders:
                        invoices = sale_order._create_invoices(True, True)
                        for invoice in invoices:
                            invoice.action_post();
                return 'sucess'
            else:
                _logger.error('Orange Money : transaction error')
                return 'transaction error'
        elif status == 'FAILED':
            _logger.error('Orange Money : transaction error')
            return "failed"
        return 'Transaction error'