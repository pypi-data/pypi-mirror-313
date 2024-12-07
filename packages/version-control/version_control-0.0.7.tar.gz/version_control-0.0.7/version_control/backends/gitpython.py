from .base import BaseVersionControl

try:
    import git

    HAS_GITPYTHON = True
except ImportError:
    HAS_GITPYTHON = False


class GitPythonBackend(BaseVersionControl):

    @classmethod
    def get_current_branch_name(cls):
        branch = ""
        if HAS_GITPYTHON:
            repo = git.Repo(search_parent_directories=True)
            branch = repo.active_branch.name

        return branch
