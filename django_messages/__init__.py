# coding: utf-8
from __future__ import (absolute_import, division, print_function, unicode_literals)
import pkg_resources
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import importlib

__version__ = pkg_resources.resource_string('django_messages', 'version.txt').strip().decode('utf-8')


def _version_tuple(version):
    versions = version.split('-')
    numversions = map(int, versions[0].split('.'))
    return tuple(numversions) + tuple(versions[1:])
VERSION = _version_tuple(__version__)

BACKEND = getattr(settings, 'MESSAGES_BACKEND',
                  'django_messages.backends.username.UsernameBackend')


def _get_backend(full_backend_path):
    from django_messages.backends import BaseMessageBackend
    module, attr = full_backend_path.rsplit('.', 1)
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))
    try:
        Backend = getattr(mod, attr)
    except AttributeError as e:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                   'class.' % (module, attr))

    if not issubclass(Backend, BaseMessageBackend):
        raise ImproperlyConfigured('Backend "%s" is not a subclass of "%s"' %
                                   (Backend, BaseMessageBackend))

    return Backend()

backend = _get_backend(BACKEND)
