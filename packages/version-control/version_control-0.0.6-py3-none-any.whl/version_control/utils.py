from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .backends.gitpython import HAS_GITPYTHON, GitPythonBackend
from .backends.mercurial import HAS_HGLIB, HgLibBackend

try:
    from django.utils.module_loading import import_string
except ImportError:
    from django.utils.module_loading import import_by_path as import_string


def get_backend():
    backend_path = getattr(
        settings,
        "VERSION_CONTROL_BACKEND",
        "version_control.backends.dummy.DummyVersionControlBackend",
    )
    try:
        klass = import_string(backend_path)
    except (ImproperlyConfigured, ImportError):
        if HAS_GITPYTHON:
            klass = GitPythonBackend
        elif HAS_HGLIB:
            klass = HgLibBackend
        else:
            raise ImportError("Install GitPython or hglib package.")
    return klass
