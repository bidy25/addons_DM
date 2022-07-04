# -*- coding: utf-8 -*-
import json
import io
from datetime import datetime, date
from odoo.tools import date_utils
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from calendar import monthrange
from odoo import models, fields, api, _

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class AccountDeclaration(models.Model):
    _name = 'account.declaration'
    _description = 'Account declaration'
    _rec_name = 'name'

    name = fields.Char(compute='_compute_name', store='True')
    month_declaration = fields.Selection(
        [('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
         ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
         ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], string='Month', default='1', required=True)
    year = fields.Char(string='Year', default=lambda a: datetime.now().year, required=True, size=4)
    start_date = fields.Date('Start date', required=True)
    end_date = fields.Date('End date', required=True)
    invoice_lines_ids = fields.Many2many('account.move', string='Invoice lines')

    @api.constrains('year')
    def _check_value(self):
        if self.year:
            if len(self.year) != 4 or int(self.year) < 0:
                raise ValidationError(_('Number of digits must on exceed 4'))

    @api.depends('month_declaration', 'year')
    def _compute_name(self):
        for declaration in self:
            declaration.name = '%s - %s' % (declaration.month_declaration, declaration.year)

    @api.onchange('month_declaration', 'year')
    def _value_day(self):
        if self.year and self.month_declaration:
            self._check_value()
            months = int(self.month_declaration)
            year = int(self.year)
            lasts = int(monthrange(year, months)[1])
            return {'value': {
                'start_date': date(year, months, 1),
                'end_date': date(year, months, lasts),
            }}

    def invoicing_list(self):
        domain = [('state', '=', 'posted')]
        domain += [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date)]
        invoice_ids = self.env['account.move'].search(domain)
        self.invoice_lines_ids = [(6, 0, invoice_ids.mapped('id'))]

    def export_data_xls(self):
        self = self.with_context(lang=self.env.user.lang)
        if self.invoice_lines_ids:
            invoice_list_ids = self.invoice_lines_ids
            data = {
                'start_date': self.start_date,
                'end_date': self.end_date,
                'number': invoice_list_ids.mapped('name'),
                'docs': invoice_list_ids.mapped('invoice_origin'),
                'date_due': invoice_list_ids.mapped('invoice_date_due'),
                'reference': invoice_list_ids.mapped('ref'),
                'untaxe_signed': invoice_list_ids.mapped('amount_untaxed_signed'),
                'tax_signed': invoice_list_ids.mapped('amount_tax_signed'),
                'amount_total_signed': invoice_list_ids.mapped('amount_total_signed'),
                'amount_residual_signed': invoice_list_ids.mapped('amount_residual_signed'),
                'invoice_payment_state': invoice_list_ids.mapped('invoice_payment_state'),
                'currency_id': invoice_list_ids.mapped('currency_id').name,
            }
            return {
                'type': 'ir_actions_xlsx_download',
                'data': {'model': 'account.declaration',
                         'options': json.dumps(data, default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': '%s' % self.name,
                         }
            }

    def get_xlsx_report(self, data, response):
        self = self.with_context(lang=self.env.user.lang)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        label = workbook.add_format({'bold': True, 'font_size': '12'})
        val = workbook.add_format()
        val.set_border()
        head = workbook.add_format({'bold': True, 'font_size': '12'})
        head.set_pattern(1)
        head.set_bg_color('gray')
        head.set_border()
        title = workbook.add_format({'align': 'center', 'bold': True, 'italic': True, 'font_size': '16'})
        number_format = workbook.add_format({'font_size': '12', 'num_format': '# ### ### ##0.00'})
        number_format.set_border()
        sum_format = workbook.add_format({'bold': True, 'font_size': '12', 'num_format': '# ### ### ##0.00'})
        sum_format.set_border()
        date_format = workbook.add_format({'num_format': 'dd mmm yyyy', 'align': 'left'})
        date_form = workbook.add_format({'num_format': 'dd-mm-yyyy', 'align': 'left'})
        date_form.set_border()
        sheet.merge_range('A1:I1', _("Account declaration"), title)
        sheet.write('A3', _("Start date:"), label)
        date_start = datetime.strptime(data['start_date'], '%Y-%m-%d')
        sheet.write_datetime('B3', date_start, date_format)
        sheet.write('D3', _("End date:"), label)
        date_end = datetime.strptime(data['end_date'], '%Y-%m-%d')
        sheet.write_datetime('E3', date_end, date_format)
        sheet.write('G3', _('Currency:'), label)
        sheet.write('H3', data['currency_id'])
        sheet.set_column(0, 0, 17)
        sheet.set_column(1, 1, 12)
        sheet.set_column(2, 8, 17)
        row = 5
        col = 0
        for value in data['number']:
            sheet.write(4, col, _("Number"), head)
            sheet.write(row, col, value, val)
            row += 1
        row = 5
        col = 1
        for value in data['date_due']:
            sheet.write(4, col, _("Date due"), head)
            if value:
                values = datetime.strptime(value, '%Y-%m-%d')
                sheet.write(row, col, values, date_form)
                row += 1
            else:
                value = _("")
                sheet.write(row, col, value, val)
                row += 1
        row = 5
        col = 2
        for value in data['docs']:
            sheet.write(4, col, _("Original document"), head)
            if value:
                sheet.write(row, col, value, val)
                row += 1
            else:
                value = _("")
                sheet.write(row, col, value, val)
                row += 1
        row = 5
        col = 3
        for value in data['reference']:
            sheet.write(4, col, _("Reference"), head)
            if value:
                sheet.write(row, col, value, val)
                row += 1
            else:
                value = _("")
                sheet.write(row, col, value, val)
                row += 1
        row = 5
        col = 4
        for value in data['untaxe_signed']:
            sheet.write(4, col, _("Untaxe signed"), head)
            sheet.write(row, col, value, number_format)
            row += 1
            sum_untaxe_signed = sum(data['untaxe_signed'])
            sheet.write(row, col, sum_untaxe_signed, sum_format)
        row = 5
        col = 5
        for value in data['tax_signed']:
            sheet.write(4, col, _("Taxe signed"), head)
            sheet.write(row, col, value, number_format)
            row += 1
            sum_taxe_signed = sum(data['tax_signed'])
            sheet.write(row, col, sum_taxe_signed, sum_format)
        row = 5
        col = 6
        for value in data['amount_total_signed']:
            sheet.write(4, col, _("Total"), head)
            sheet.write(row, col, value, number_format)
            row += 1
            sum_amount_total_signed = sum(data['amount_total_signed'])
            sheet.write(row, col, sum_amount_total_signed, sum_format)
        row = 5
        col = 7
        for value in data['amount_residual_signed']:
            sheet.write(4, col, _("Amount due"), head)
            sheet.write(row, col, value, number_format)
            row += 1
            sum_amount_residual_signed = sum(data['amount_residual_signed'])
            sheet.write(row, col, sum_amount_residual_signed, sum_format)
        row = 5
        col = 8
        for value in data['invoice_payment_state']:
            sheet.write(4, col, _("Payment"), head)
            if value:
                if value == 'paid':
                    value = 'Paid'
                else:
                    value = 'Not paid'
                sheet.write(row, col, value, val)
                row += 1
            if value is False:
                value = _("")
                sheet.write(row, col, value, val)
                row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()