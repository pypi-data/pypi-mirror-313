from griff.appli.event.event import Event

from {{ cookiecutter.context | snake_case }}._common.domain.{{ cookiecutter.aggregate | snake_case }} import {{cookiecutter.aggregate | pascal_case}}

# todo: renommer correctement l'evt
class {{ cookiecutter.CommandEvent }}(Event):
    payload: {{cookiecutter.aggregate | pascal_case}}
