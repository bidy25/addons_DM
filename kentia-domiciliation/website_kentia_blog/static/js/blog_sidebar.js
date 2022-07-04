odoo.define('website_kentia_blog.blog_sidebar_popular_posts', function (require) {
    'use strict';

    var core = require('web.core');
    var wUtils = require('website.utils');
    var publicWidget = require('web.public.widget');

    var _t = core._t;

    publicWidget.registry.js_get_popular_posts = publicWidget.Widget.extend({
        selector: '.popular-posts',
        disabledInEditableMode: false,

        start: function () {
            var self = this;

            var template = 'website_kentia_blog.popular_posts_list_template';
            var domain = [
                ['website_published', '=', true]
            ];
            var limit = 3;

            var prom = new Promise(function (resolve) {
                self._rpc({
                    route: '/blog/render_popular_posts',
                    params: {
                        template: template,
                        domain: domain,
                        limit: limit,
                    },
                }).then(function (posts) {
                    var count = $(posts).children().length;
                    if (count > 0) {
                        self.$target.html(posts);
                        return;
                    } else {
                        self.$target.html('').append($('<div/>', {
                            class: 'alert alert-warning alert-dismissible text-center',
                            text: _t("No blog post was found. Make sure your posts are published."),
                        }));
                    }

                    resolve();
                });
            });
            return Promise.all([this._super.apply(this, arguments), prom]);
        },
    });

    publicWidget.registry.social_share = publicWidget.Widget.extend({
        selector: '.o_wblog_social_links',
        disabledInEditableMode: false,
        events: {
            'click .o_facebook': '_onFacebook',
            'click .o_twitter': '_onTwitter',
            'click .o_linkedin': '_onLinkedin',
        },
        _onFacebook: function (ev) {
            ev.preventDefault();
            var url = '';
            var articleURL = encodeURIComponent(window.location.href);
            url = 'https://www.facebook.com/sharer/sharer.php?u=' + articleURL;
            window.open(url, '', 'menubar=no, width=500, height=400');
        },
        _onTwitter: function (ev) {
            var url = '';
            var articleURL;
            var blogPostTitle;
            var blogPostTitle = encodeURIComponent($('#o_wblog_post_name').html() || '');
            var articleURL = encodeURIComponent(window.location.href);
            url = 'https://twitter.com/intent/tweet?tw_p=tweetbutton&text=Amazing blog article : ' + blogPostTitle + "! " + articleURL;
            window.open(url, '', 'menubar=no, width=500, height=400');
        },
        _onLinkedin: function (ev) {
            var url = '';
            var articleURL;
            var blogPostTitle;
            var blogPostTitle = encodeURIComponent($('#o_wblog_post_name').html() || '');
            var articleURL = encodeURIComponent(window.location.href);
            url = 'https://www.linkedin.com/shareArticle?mini=true&url=' + articleURL + '&title=' + blogPostTitle;
            window.open(url, '', 'menubar=no, width=500, height=400');
        }
    });


});