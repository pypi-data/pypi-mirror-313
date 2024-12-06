-- Fetch database information
WITH ids AS (
    SELECT DISTINCT
        table_catalog,
        table_schema
    FROM information_schema.tables
    WHERE table_catalog = DB_NAME()
)

SELECT
    d.database_id,
    database_name = i.table_catalog,
    schema_name = s.name,
    s.schema_id,
    schema_owner = u.name,
    schema_owner_id = u.uid
FROM sys.schemas AS s
INNER JOIN ids AS i
    ON s.name = i.table_schema
LEFT JOIN sys.sysusers AS u
    ON s.principal_id = u.uid
LEFT JOIN sys.databases AS d
    ON i.table_catalog = d.name
