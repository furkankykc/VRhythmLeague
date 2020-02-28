# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# AJAX mixin
class AjaxTemplateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            # split template_name
            split = self.template_name.split('.html')
            # add _inner to the end of split list
            split[-1] = '_inner'
            # add .html to the split list
            split.append('.html')
            # join split list without spaces
            self.ajax_template_name = ''.join(split)
        # ajax_template_name defaults to template_name_inner.html
        # if the request is AJAX, then the view renders this template
        # otherwise, the view renders the template_name.html template
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)
