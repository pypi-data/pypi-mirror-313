-- name: insert!
insert into {{ cookiecutter.context | snake_case }}__{{ cookiecutter.aggregate | snake_case }} (
                            entity_id,
                            serialized,
                            created_at,
                            updated_at
                        )
values (
        :entity_id,
        :serialized,
        :created_at,
        :updated_at
       );

-- name: update!
UPDATE {{ cookiecutter.context | snake_case }}__{{ cookiecutter.aggregate | snake_case }}
SET serialized  = :serialized,
    updated_at  = :updated_at
WHERE entity_id = :entity_id;

-- name: delete!
DELETE
FROM {{ cookiecutter.context | snake_case }}__{{ cookiecutter.aggregate | snake_case }}
WHERE entity_id = :entity_id;

-- name: get_by_id^
SELECT entity_id,
       serialized,
       created_at,
       updated_at
from {{ cookiecutter.context | snake_case }}__{{ cookiecutter.aggregate | snake_case }}
where entity_id = :entity_id;

-- name: list_all
SELECT entity_id,
       serialized,
       created_at,
       updated_at
FROM {{ cookiecutter.context | snake_case }}__{{ cookiecutter.aggregate | snake_case }};

