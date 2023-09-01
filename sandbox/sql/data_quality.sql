-- List schema and tables and comments on the database server
SELECT table_catalog,
    table_schema,
    table_name,
    table_type,
    obj_description(pgc.oid, 'pg_class'),
    pgc.relowner,
    u.usename
FROM information_schema.tables t
    INNER JOIN pg_catalog.pg_class pgc ON t.table_name = pgc.relname
    INNER JOIN pg_catalog.pg_user u ON (pgc.relowner = u.usesysid)
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_catalog,
    table_schema,
    table_name;
---
--- @ Retrieving the schema for tables
SELECT '"' || table_catalog || '"."' || table_schema || '"."' || table_name || '"' AS full_name,
    column_name,
    data_type,
    column_default,
    is_nullable,
    character_maximum_length,
    numeric_precision,
    datetime_precision,
    pgd.description
FROM information_schema.columns C
    LEFT JOIN pg_catalog.pg_class pgc ON C .table_name = pgc.relname
    LEFT JOIN pg_catalog.pg_description pgd ON C .ordinal_position = pgd.objsubid
    AND pgc.oid = pgd.objoid
WHERE table_schema NOT IN ('pg_catalog', 'information_schema');
--- 
--- Query generating results correlating to the freshness of the table 
--- Cannot get freshness modified date of a table is not track unless 
SELECT table_schema,
    table_name,
    pg_size_pretty(
        pg_total_relation_size(
            '"' || table_schema || '"."' || table_name || '"'
        )
    ) AS table_size,
    pg_size_pretty(
        pg_indexes_size(
            '"' || table_schema || '"."' || table_name || '"'
        )
    ) AS index_size,
    n_live_tup AS estimated_row_count
FROM information_schema.tables t
    INNER JOIN pg_catalog.pg_stat_user_tables psut ON psut.schemaname = t.table_schema
    AND psut.relname = t.table_name
WHERE table_schema NOT IN ('pg_catalog', 'information_schema');