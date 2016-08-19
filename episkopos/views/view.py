# -*- coding: utf-8 -*-

"""
Created on 2016-08-19
:author: Izhar Firdaus (kagesenshi.87@gmail.com)
"""

from pyramid.view import view_config
from pyramid.view import view_defaults

from episkopos import _
from episkopos.resources import CustomContent
from episkopos.fanstatic import css_and_js
from episkopos.views import BaseView


@view_defaults(context=CustomContent, permission='view')
class CustomContentViews(BaseView):
    """ Views for :class:`episkopos.resources.CustomContent` """

    @view_config(name='view', permission='view',
                 renderer='episkopos:templates/custom-content-default.pt')
    def default_view(self):
        """ Default view for :class:`episkopos.resources.CustomContent`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        return {
            'foo': _(u'bar'),
        }

    @view_config(name='alternative-view', permission='view',
                 renderer='episkopos:templates/custom-content-alternative.pt')
    def alternative_view(self):
        """ Alternative view for :class:`episkopos.resources.CustomContent`.
        This view requires the JS / CSS resources defined in
        :mod:`episkopos.fanstatic`.

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        css_and_js.need()

        return {
            'foo': _(u'bar'),
        }
