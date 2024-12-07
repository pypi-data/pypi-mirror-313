from typing import TypeVar

from injector import singleton, Binder

from griff.runtime.components.abstract_runtime_component import (
    InjectBindable,
    RuntimeComponent,
)
from griff.services.date.date_service import DateService
from griff.services.date.fake_date_service import FakeDateService
from griff.services.db.db_settings import DbSettings
from griff.services.hasher.providers.argon2_provider import Argon2Provider
from griff.services.hasher.providers.fake_hasher_provider import FakeHasherProvider
from griff.services.hasher.providers.hasher_provider import HasherProvider
from griff.services.jwt.jwt_settings import JwtSettings
from griff.services.query_runner.query_runner_settings import QueryRunnerSettings
from griff.services.uniqid.generator.fake_uniqid_generator import FakeUniqIdGenerator
from griff.services.uniqid.generator.ulid_uniqid_generator import UlidUniqIdGenerator
from griff.services.uniqid.generator.uniqid_generator import (
    UniqIdGenerator,
)
from griff.settings.griff_settings import GriffSettings

S = TypeVar("S", bound=GriffSettings)


class DefaultServicesRuntimeComponent(InjectBindable, RuntimeComponent):
    def __init__(self, settings: S):
        self._settings = settings

    def configure(self, binder: Binder) -> None:
        binder.bind(UniqIdGenerator, to=UlidUniqIdGenerator, scope=singleton)  # type: ignore # noqa: E501
        binder.bind(HasherProvider, to=Argon2Provider, scope=singleton)  # type: ignore
        binder.bind(JwtSettings, to=self._settings.jwt, scope=singleton)  # type: ignore
        binder.bind(QueryRunnerSettings, to=self._settings.query_runner)
        binder.bind(DbSettings, to=self._settings.db)


class DefaultServicesTestRuntimeComponent(InjectBindable, RuntimeComponent):
    def __init__(self, settings: S):
        self._settings = settings

    def configure(self, binder: Binder) -> None:
        binder.bind(DateService, to=FakeDateService)
        binder.bind(UniqIdGenerator, to=FakeUniqIdGenerator)  # type: ignore # noqa: E501
        binder.bind(HasherProvider, to=FakeHasherProvider)  # type: ignore
        binder.bind(JwtSettings, to=self._settings.jwt)
        binder.bind(QueryRunnerSettings, to=self._settings.query_runner)
        binder.bind(DbSettings, to=self._settings.db)
