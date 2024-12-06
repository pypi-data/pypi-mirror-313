from griff.appli.policies.policy import Policy, PolicyException
from griff.utils.errors import ConflictError

class {{cookiecutter.aggregate | pascal_case}}VerifieUnTrucError(ConflictError):
    ...

# à renommer
class {{cookiecutter.aggregate | pascal_case}}VerifieUnTrucPolicy(Policy):
    async def check(self, **kwargs) -> None:
        # some code
        if True:
            return None
        message = _("echec")
        raise PolicyException({{cookiecutter.aggregate | pascal_case}}VerifieUnTrucError(message=message))
