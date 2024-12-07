import re

from django.template.loader import render_to_string

try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_str as force_text

from .utils import get_backend

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


def get_version_control_panel():
    backend = get_backend()
    branch = backend.get_current_branch_name()

    return render_to_string("version_control_panel.html", {"branch": branch})


class VersionControlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        encoding = response.charset if hasattr(response, "charset") else "utf-8"
        content = force_text(response.content, encoding=encoding)
        insert_before = "</body>"
        pattern = re.escape(insert_before)
        bits = re.split(pattern, content, flags=re.IGNORECASE)
        if len(bits) > 1:
            bits[-2] += get_version_control_panel()
            response.content = insert_before.join(bits)
            if response.get("Content-Length", None):
                response["Content-Length"] = len(response.content)

        return response
