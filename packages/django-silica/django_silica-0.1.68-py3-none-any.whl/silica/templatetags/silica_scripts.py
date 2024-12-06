from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def silica_scripts():
    silica_js = static("silica.js")
    morphdom_js = static("morphdom.js")
    alpine_morph_js = static("alpine3.morph.min.js")
    alpine_js = static("alpine3.min.js")
    return mark_safe(f"""
        <script src="{morphdom_js}"></script>
        <script src="{silica_js}"></script>
        <script src="{alpine_morph_js}"></script>
        <script src="{alpine_js}" defer></script>
        <style>
            [silica\:loading], 
            [silica\:loading\.init], 
            [silica\:loading\.proceeding] {{ display: none }}</style>
    """)
