SELECT
    db.database_id,
    database_name = db.name
FROM sys.databases AS db
WHERE db.name = DB_NAME()
