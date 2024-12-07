class EndpointDecoratorProcessor:
    """
    Class meant to interpret endpoint decorator.
    Such a decorator should contain :

    @register_endpoint(route="/me", method="GET",
    permission="LEAGUE_ADMIN",
    success_code=status.HTTP_201_CREATED)

    route: a str that shall start by '/'
    method: a string in [GET, POST, PATCH, PUT, OPTIONS]
    http_code: a starlette HTTP code
    permission: a string in PUBLIC / SIMPLE_USER / LEAGUE_ADMIN /SITE_ADMIN
    """

    def __init__(self):
        self._route = None
        self._method = None
        self._http_code = None

    @staticmethod
    def _sanitize(to_be_sanitized: str):
        return to_be_sanitized.strip("'").strip('"').strip(" ")

    def _check_route_is_correct(self, a_route_definition: str) -> bool:
        splited = a_route_definition.split("=")
        if self._sanitize(splited[1])[0] != "/":
            raise ValueError("route définition shall start by /")
        return True

    def _check_method_is_correct(self, a_method_definition: str):
        splited = a_method_definition.split("=")
        method = self._sanitize(splited[1])
        if method not in ["GET", "POST", "OPTIONS", "PATCH", "PUT", "DELETE"]:
            raise ValueError(f"Http method {method} unknown")
        return True

    def _check_http_code_is_correct(self, a_http_code_def: str) -> int:
        splited = a_http_code_def.split("=")
        http_code = self._sanitize(splited[1])
        # do not remove line below !!
        from starlette import status  # noqa: F401

        return eval(http_code)

    def _check_decoration_string(self, a_decoration_str: str):
        if "route" not in a_decoration_str:
            raise ValueError("route définition not found in decoration")

    def _process_route_param(self, a_str_to_process: str):
        if "route" in a_str_to_process and self._check_route_is_correct(
            a_route_definition=a_str_to_process
        ):
            splited = a_str_to_process.split("=")
            self._route = self._sanitize(splited[1])

    def _process_http_method_param(self, a_str_to_process: str):
        if "method" in a_str_to_process and self._check_method_is_correct(
            a_method_definition=a_str_to_process
        ):
            splited = a_str_to_process.split("=")
            self._method = self._sanitize(splited[1])

    def _process_http_code_param(self, a_str_to_process: str):
        if "success_code" in a_str_to_process:
            self._http_code = self._check_http_code_is_correct(
                a_http_code_def=a_str_to_process
            )

    def load_decorators(self, a_decoration_string_list: list[str]):
        for decorator in a_decoration_string_list:
            if decorator[:18] == "@register_endpoint":
                self._check_decoration_string(decorator)
                keyval_list = decorator[
                    decorator.index("(") + 1 : decorator.index(")")  # noqa: E203
                ].split(",")
                for decoration_param in keyval_list:
                    if len(decoration_param) <= 1:
                        continue
                    if "=" not in decoration_param:
                        raise ValueError("decoration badly formatted, '=' not found")
                    self._process_route_param(a_str_to_process=decoration_param)
                    self._process_http_code_param(a_str_to_process=decoration_param)
                    self._process_http_method_param(a_str_to_process=decoration_param)

    def get_decorator_params(self):
        return {
            "route": self._route,
            "method": self._method,
            "http_code": self._http_code,
        }

    @property
    def route(self):
        return self._route

    @property
    def method(self):
        return self._method

    @property
    def code(self):
        return self._http_code
