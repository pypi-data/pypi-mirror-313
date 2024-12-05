"""ClickHouse database operations module."""

import os

from clickhouse_driver import Client


class ClickHouseClient:
    def __init__(self, host=None, database=None, port=None):
        host = host or os.getenv("CLICKHOUSE_HOST", "localhost")
        if ":" in host:
            host, port = host.split(":")

        self.client = Client(
            host=host,
            port=port or os.getenv("CLICKHOUSE_PORT", 9000),
            database=database or os.getenv("CLICKHOUSE_DB", "development"),
            user=os.getenv("CLICKHOUSE_USER", "default"),
            password=os.getenv("CLICKHOUSE_PASSWORD", ""),
        )

    def init_migrations_table(self):
        """Initialize the schema migrations table."""
        self.client.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version LowCardinality(String),
                active UInt8 NOT NULL DEFAULT 1,
                created_at DateTime64(6, 'UTC') NOT NULL DEFAULT now64()
            )
            ENGINE = ReplacingMergeTree(created_at)
            PRIMARY KEY(version)
            ORDER BY (version)
        """)

    def get_database_schema(self):
        """Get the database schema organized by object type and sorted by migration date."""
        # Get all applied migrations in order
        applied_migrations = self.get_applied_migrations()
        latest_version = applied_migrations[-1][0] if applied_migrations else "0"

        # Initialize schema structure
        schema = {
            "version": latest_version,
            "tables": [],
            "materialized_views": [],
            "dictionaries": [],
        }

        # Get all database objects
        tables = self.get_database_tables()
        materialized_views = self.get_database_materialized_views()
        dictionaries = self.get_database_dictionaries()

        for table in tables:
            table_name = table[0]
            create_stmt = self.client.execute(f"SHOW CREATE TABLE {table_name}")[0][0]
            schema["tables"].append(create_stmt)

        for materialized_view in materialized_views:
            materialized_view_name = materialized_view[0]
            create_stmt = self.client.execute(
                f"SHOW CREATE MATERIALIZED VIEW {materialized_view_name}"
            )[0][0]
            schema["materialized_views"].append(create_stmt)

        for dictionary in dictionaries:
            dictionary_name = dictionary[0]
            create_stmt = self.client.execute(
                f"SHOW CREATE DICTIONARY {dictionary_name}"
            )[0][0]
            schema["dictionaries"].append(create_stmt)

        # Sort each category by migration date
        for category in ["tables", "materialized_views", "dictionaries"]:
            schema[category].sort()

        return schema

    def get_latest_migration(self):
        """Get the latest migration version."""
        # First check if the table exists
        table_exists = self.client.execute("""
            SELECT name
            FROM system.tables
            WHERE database = currentDatabase()
            AND name = 'schema_migrations'
        """)

        if not table_exists:
            return None

        result = self.client.execute("""
            SELECT MAX(version) FROM schema_migrations WHERE active = 1
        """)
        return result[0][0] if result else None

    def get_database_tables(self):
        """Get the database tables with their engines, indexes and partitioning."""
        return self.client.execute("""
            SELECT
                name
            FROM system.tables
            WHERE database = currentDatabase()
                AND position('MergeTree' IN engine) > 0
                AND engine NOT IN ('MaterializedView', 'Dictionary')
                AND name != 'schema_migrations'
            ORDER BY name
        """)

    def get_database_materialized_views(self):
        """Get the database materialized views."""
        return self.client.execute("""
            SELECT
                name
            FROM system.tables
            WHERE database = currentDatabase()
                AND engine = 'MaterializedView'
                AND name != 'schema_migrations'
            ORDER BY name
        """)

    def get_database_dictionaries(self):
        """Get the database dictionaries."""
        return self.client.execute("""
            SELECT
                name
            FROM system.tables
            WHERE database = currentDatabase()
                AND engine = 'Dictionary'
                AND name != 'schema_migrations'
            ORDER BY name
        """)

    def get_applied_migrations(self):
        """Get list of applied migrations."""
        return self.client.execute("""
            SELECT version
            FROM schema_migrations FINAL
            WHERE active = 1
            ORDER BY version
        """)

    def execute_migration(self, sql: str):
        """Execute a migration SQL statement."""
        # Split multiple statements and execute them separately
        statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()]
        for statement in statements:
            self.client.execute(statement)

    def mark_migration_applied(self, version: str):
        """Mark a migration as applied."""
        self.client.execute(
            """
            INSERT INTO schema_migrations (version, active)
            VALUES (%(version)s, 1)
            """,
            {"version": version},
        )

        self.client.execute(
            """
            OPTIMIZE TABLE schema_migrations FINAL
            """
        )

    def mark_migration_rolled_back(self, version: str):
        """Mark a migration as rolled back."""
        self.client.execute(
            """
            INSERT INTO schema_migrations (version, active, created_at)
            VALUES (
                %(version)s,
                0,
                now64()
            )
            """,
            {"version": version},
        )

        self.client.execute(
            """
            OPTIMIZE TABLE schema_migrations FINAL
            """
        )
