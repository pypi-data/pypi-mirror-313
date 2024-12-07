import typing
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_babel import BabelConfigs, BabelMiddleware
from injector import Binder, singleton, Injector
from loguru import logger
from pydantic_i18n import BabelLoader, PydanticI18n
from starlette.middleware.cors import CORSMiddleware

from griff.infra.fastapi.exception_handlers.griff_exception_handler import (
    griff_exception_handler,
)
from griff.infra.fastapi.exception_handlers.pydantic_exception_handler import (
    PydanticValidationExceptionHandler,
)
from griff.runtime.components.abstract_runtime_component import (
    RuntimeComponent,
    InjectBindable,
    Runnable,
)
from griff.settings.griff_settings import GriffSettings
from griff.utils.exceptions import GriffException
from griff.infra.fastapi.middlewares.fake_lagtime_middleware import (
    FakeLagTimeMiddleware,
)


class FastApiRuntimeComponent(Runnable, InjectBindable, RuntimeComponent):
    def __init__(self, settings: GriffSettings):
        self._settings = settings

    def configure(self, binder: Binder) -> None:
        binder.bind(FastAPI, to=FastAPI, scope=singleton)

    # noinspection PyTypeChecker
    @typing.no_type_check
    def initialize(self, injector: Injector):
        app = injector.get(FastAPI)
        app.add_middleware(CORSMiddleware, **self._settings.cors.model_dump())
        app.add_exception_handler(GriffException, griff_exception_handler)
        self.init_fastapi_locale(app)
        self.init_pydantic_locale_and_exception_handler(app)
        if self._settings.env == "dev":
            app.add_middleware(FakeLagTimeMiddleware)

    def clean(self, injector: Injector):
        pass

    def start(self, injector: Injector):
        pass

    def stop(self, injector: Injector):
        pass

    def init_fastapi_locale(self, app: FastAPI):
        if self._settings.locale is None:
            logger.warning("No locale settings found. Skipping locale initialization.")
            return None

        # # check translation messages are compiled
        translation_filename = Path(self._settings.project_dir).joinpath(
            f"{self._settings.fastapi_local_path}/fr/LC_MESSAGES/messages.mo"
        )
        if translation_filename.exists() is False:
            raise RuntimeError(
                "Translation files are missing, run "
                "'python manage.py locale compilemessages'"
            )

        configs = BabelConfigs(
            ROOT_DIR=f"{self._settings.project_dir}/app",  # bug ? config do a .parent
            BABEL_DEFAULT_LOCALE=self._settings.locale.default,
            BABEL_TRANSLATION_DIRECTORY=self._settings.locale.relative_path,
        )
        app.add_middleware(BabelMiddleware, babel_configs=configs)

    def init_pydantic_locale_and_exception_handler(self, app):
        if self._settings.locale is None:
            return None
        loader = BabelLoader(f"{self._settings.pydantic_locale_path}")
        pydantic_i18n = PydanticI18n(
            loader, default_locale=self._settings.locale.default
        )
        pydantic_exc_handler = PydanticValidationExceptionHandler(pydantic_i18n)
        app.add_exception_handler(RequestValidationError, pydantic_exc_handler.dispatch)
