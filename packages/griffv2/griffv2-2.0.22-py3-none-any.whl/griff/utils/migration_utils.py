from yoyo import get_backend, read_migrations


class MigrationUtils:
    @staticmethod
    def migrate(dsn: str, migrations_path: str) -> None:  # pragma: no cover
        backend = get_backend(dsn)
        migrations = read_migrations(str(migrations_path))

        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
            backend.connection.commit()
