from .base import BaseVersionControl


class DummyVersionControlBackend(BaseVersionControl):

    @classmethod
    def get_current_branch_name(self):
        return "dummy_backend"
