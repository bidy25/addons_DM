from odoo import models


class PaymentTransactionInherit(models.Model):
    _inherit = 'payment.transaction'

    def done_transaction(self):
        self._set_transaction_done()
        self._post_process_after_done()
        sale_orders = self.sale_order_ids;
        for sale_order in sale_orders:
            invoices=sale_order._create_invoices(True,True)
            for invoice in invoices:
                invoice.action_post();
