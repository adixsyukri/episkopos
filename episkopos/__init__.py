# -*- coding: utf-8 -*-

"""
Created on 2016-08-19
:author: Izhar Firdaus (kagesenshi.87@gmail.com)
"""

from kotti.resources import File
from pyramid.i18n import TranslationStringFactory
from sqlalchemy.orm import configure_mappers
from sqlalchemy_continuum import make_versioned
from kotti.security import Principal

_ = TranslationStringFactory('episkopos')


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                episkopos.kotti_configure

        to enable the ``episkopos`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    make_versioned(user_cls='Principal')
    settings['pyramid.includes'] += ' episkopos'
    settings['kotti.alembic_dirs'] += ' episkopos:alembic'
    settings['kotti.available_types'] += ' episkopos.resources.Company'
    settings['kotti.fanstatic.view_needed'] += ' episkopos.fanstatic.css_and_js'
    File.type_info.addable_to.append('Company')


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('episkopos:locale')
    config.add_static_view('static-episkopos', 'episkopos:static')
    config.scan(__name__)
    configure_mappers()
