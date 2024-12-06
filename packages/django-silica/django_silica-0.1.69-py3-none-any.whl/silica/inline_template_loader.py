from django.template import TemplateDoesNotExist
from django.template import Template
from django.template.loaders.base import Loader


class Loader(Loader):
    def get_template_sources(self, template_name):
        return [template_name]

    def get_contents(self, origin):
        return origin

    def get_template(self, template_name, skip=None, dirs=None):
        """We identify if this is an silica inline template with the '::silica-inline::' prefix"""
        if "::silica-inline::" not in template_name:
            raise TemplateDoesNotExist("Template %s not found" % template_name)

        inline_template = template_name.replace("::silica-inline::", "")

        return Template(inline_template)

        # TO DEPRECATE
        # is_admin = False
        # for template_source in self.get_template_sources(template_name):
        #     if "admin" in template_source:
        #         is_admin = True
        #
        # if is_admin:
        #     raise TemplateDoesNotExist("Template %s not found" % template_name)
        # else:
        #     return Template(template_name, engine=self.engine)
