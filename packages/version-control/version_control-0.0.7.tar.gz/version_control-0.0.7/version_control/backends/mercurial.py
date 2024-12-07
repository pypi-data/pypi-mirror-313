from django.conf import settings

from .base import BaseVersionControl

try:
    import hglib

    HAS_HGLIB = True
except ImportError:
    HAS_HGLIB = False


class HgLibBackend(BaseVersionControl):

    @classmethod
    def get_current_branch_name(cls):
        branch = ""
        if HAS_HGLIB:
            repo = hglib.open(settings.BASE_DIR)
            branch = repo.branch().decode()

        return branch
