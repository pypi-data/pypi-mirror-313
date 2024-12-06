from griff.infra.persistence.db_persistence import SerializedDbPersistence, DbPersistence
from griff.infra.persistence.dict_persistence import SerializedDictPersistence, DictPersistence
from injector import singleton

class {{ cookiecutter.aggregate | pascal_case }}Persistence(SerializedDbPersistence):
    def _get_relative_sql_queries_path(self) -> str:
        return "{{ cookiecutter.context| snake_case }}/_common/repositories/sql/{{ cookiecutter.aggregate | snake_case }}.sql"

@singleton
class {{ cookiecutter.aggregate | pascal_case }}FakePersistence(SerializedDictPersistence):
    ...

######
# OU (supprimer l'implémentation inutile)
######
class {{ cookiecutter.aggregate | pascal_case }}Persistence(DbPersistence):
    def _get_relative_sql_queries_path(self) -> str:
        return "{{ cookiecutter.context| snake_case }}/_common/repositories/sql/{{ cookiecutter.aggregate | snake_case }}.sql"

@singleton
class {{ cookiecutter.aggregate | pascal_case }}FakePersistence(DictPersistence):
    ...
