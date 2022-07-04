# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class MailSubscription(models.Model):
    _name = 'mail.subscription'

    def process_send_mail(self):
        company = self.env.ref('base.main_company').mapped('email')
        str_mail_company = ''.join(company)
        customer_ids = self.env['subscription.subscription'].search([])
        _logger.info('Send email template : --------------------')
        for item in customer_ids:
            customer_id = item.customer_name
            account_ids = self.env['account.move'].search([('partner_id', '=', customer_id.id)])
            for h in account_ids:
                if h.state != 'posted':
                    email_customer = h.partner_id.email

                    ctx = {
                        'email_to': 'toky@kasia.mg',
                        'email_from': str_mail_company,
                    }

                    _logger.info('Send email template : --------------------')
                    if email_customer:
                        self.env.ref("kentia_domiciliation.email_invoicing").send_mail(h.id, email_values=ctx, force_send=True)
