# -*- coding: utf-8 -*-
from datetime import date

from odoo import _, models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError

class BlogPostInherit(models.Model):
    _inherit = 'blog.post'
    post_type = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')])
    publication_date = fields.Date('Publication date')
    banner = fields.Binary('Banner', attachment=True)

    def publish_blog(self):
        self.is_published = True

    def unpublish_blog(self):
        self.is_published = False

    def blog_cron(self):
        blog_to_publish = self.env['blog.post'].sudo().search(
            [('post_type', '=', 'automatic'), ('publication_date', '<=', date.today())])
        blog_to_publish.write({'is_published': True})
        return True

    @api.model
    def create(self, values):
        current_id = 1
        if len(self.env['blog.post'].sudo().search([])) > 0:
            current_id = 1 + self.env['blog.post'].sudo().search([])[-1].id
        img_path = '/web/image/blog.post/' + str(current_id) + '/banner'
        if values.get('banner'):
            values['cover_properties']="{\"background-image\":\"url(" + img_path + ")\",\"background-color\":\"oe_black\",\"opacity\":\"0.2\",\"resize_class\":\"o_record_has_cover cover_mid\"}"
            values['website_meta_og_img'] = img_path
        return super(BlogPostInherit, self).create(values)

    def write(self, values):
        img_path = '/web/image/blog.post/' + str(self.id) + '/banner'
        if self.banner :
            values['cover_properties'] = "{\"background-image\":\"url(" + img_path + ")\",\"background-color\":\"oe_black\",\"opacity\":\"0.2\",\"resize_class\":\"o_record_has_cover cover_mid\"}"
            values['website_meta_og_img'] = img_path
        return super(BlogPostInherit, self).write(values)

    @api.constrains('website_meta_description')
    def _verify_website_meta_description(self):
        for event in self:
            if self.website_meta_description and len(self.website_meta_description) < 50:
                raise ValidationError(_('Your description is too short.'))
            if self.website_meta_description and len(self.website_meta_description) > 300:
                raise ValidationError(_('Your description is too long.'))