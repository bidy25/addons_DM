# -*- coding: utf-8 -*-
from datetime import date

from odoo import _, models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.api import constrains

class EventEventInherit(models.Model):
    _inherit = 'event.event'

    post_type = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')])
    publication_date = fields.Date('Publication date')
    banner = fields.Binary('Banner', attachment=True)
    website_meta_description = fields.Text(size=300);

    def button_publish(self):
        self.website_published = True

    def button_unpublish(self):
        self.website_published = False

    def event_cron(self):
        event_publication = self.env['event.event'].sudo().search(
            [('post_type', '=', 'automatic'), ('publication_date', '<=', date.today())])
        event_publication.write({'is_published': True})
        return True

    @api.model
    def create(self, values):
        current_id = 1
        if len(self.env['event.event'].sudo().search([])) > 0:
            current_id = 1 + self.env['event.event'].sudo().search([])[-1].id
        img_path = '/web/image/event.event/' + str(current_id) + '/banner'
        if values.get('banner'):
            values['cover_properties'] = "{\"background-image\":\"url(" + img_path + ")\",\"background-color\":\"oe_black\",\"opacity\":\"0.2\",\"resize_class\":\"o_record_has_cover cover_mid\"}"
            values['website_meta_og_img'] = img_path
        return super(EventEventInherit, self).create(values)

    def write(self, values):
        img_path = '/web/image/event.event/' + str(self.id) + '/banner'
        if self.banner:
            values['cover_properties'] = "{\"background-image\":\"url(" + img_path + ")\",\"background-color\":\"oe_black\",\"opacity\":\"0.2\",\"resize_class\":\"o_record_has_cover cover_mid\"}"
            values['website_meta_og_img'] = img_path
        return super(EventEventInherit, self).write(values)

    @api.constrains('website_meta_description')
    def _verify_website_meta_description(self):
        for event in self:
            if self.website_meta_description and len(self.website_meta_description) < 50:
                raise ValidationError(_('Your description is too short.'))
            if self.website_meta_description and len(self.website_meta_description) > 300:
                raise ValidationError(_('Your description is too long.'))