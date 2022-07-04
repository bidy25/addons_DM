from odoo import api, fields, models
from odoo.addons.http_routing.models.ir_http import slug


class BlogPostInherit(models.Model):
    _inherit = 'blog.post'

    def _compute_website_url(self):
        super(BlogPostInherit, self)._compute_website_url()
        for blog_post in self:
            blog_post.website_url = "/actualites/%s/%s" % (slug(blog_post.blog_id), slug(blog_post))
