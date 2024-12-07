from jinja2.ext import Extension

from griff.infra.cli.controllers.griff.jinja2.filters.j2_str_filters import (
    j2_snake_case_filter,
    j2_kebab_case_filter,
    j2_camel_case_filter,
    j2_pascal_case_filter,
)


class GriffExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["snake_case"] = j2_snake_case_filter
        environment.filters["kebab_case"] = j2_kebab_case_filter
        environment.filters["camel_case"] = j2_camel_case_filter
        environment.filters["pascal_case"] = j2_pascal_case_filter
