class BaseVersionControl(object):

    @classmethod
    def get_current_branch_name(cls):
        raise NotImplementedError()
