from mysqlmigratorpostgree.connect_mysql import connect_mysql
from mysqlmigratorpostgree.connect_postgresql import connect_postgresql

class MysqlMigratorPostgree:
    def __init__(self):
        """Inicializa las conexiones y cursores para MySQL y PostgreSQL."""
        self.mysql_conn = None
        self.mysql_cursor = None
        self.postgres_conn = None
        self.postgres_cursor = None

    def connect_mysql(self, host, port, user, password, database):
        """
        Conecta a MySQL utilizando el módulo `connect_mysql`.
        """
        self.mysql_conn, self.mysql_cursor = connect_mysql(host, port, user, password, database)

    def connect_postgresql(self, host, port, user, password, database):
        """
        Conecta a PostgreSQL utilizando el módulo `connect_postgresql`.
        """
        self.postgres_conn, self.postgres_cursor = connect_postgresql(host, port, user, password, database)

    def migrate_table(self, table_name):
        """
        Migra una tabla desde MySQL a PostgreSQL.

        Args:
            table_name (str): Nombre de la tabla a migrar.
        """
        try:
            
            self.mysql_cursor.execute(f"DESCRIBE {table_name}")
            columns = self.mysql_cursor.fetchall()

            column_definitions = []
            for column in columns:
                column_name = column["Field"]
                column_type = column["Type"]

                if "int" in column_type:
                    postgres_type = "INTEGER"
                elif "varchar" in column_type or "text" in column_type:
                    postgres_type = "TEXT"
                elif "float" in column_type or "double" in column_type:
                    postgres_type = "REAL"
                elif "date" in column_type:
                    postgres_type = "DATE"
                else:
                    postgres_type = "TEXT"

                column_definitions.append(f"{column_name} {postgres_type}")

            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)});"
            self.postgres_cursor.execute(create_table_sql)

            self.mysql_cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.mysql_cursor.fetchall()

            if rows:
                column_names = [desc[0] for desc in self.mysql_cursor.description]
                column_placeholders = ", ".join(["%s"] * len(column_names))
                insert_sql = f"""
                    INSERT INTO {table_name} ({', '.join(column_names)})
                    VALUES ({column_placeholders})
                    ON CONFLICT DO NOTHING;
                """
                for row in rows:
                    self.postgres_cursor.execute(insert_sql, tuple(row.values()))

            self.postgres_conn.commit()
            print(f"Tabla {table_name} migrada con éxito.")
        except Exception as e:
            self.postgres_conn.rollback()
            print(f"Error al migrar la tabla {table_name}: {e}")
            raise

    def migrate_all(self):
        """
        Detecta y migra todas las tablas desde MySQL a PostgreSQL.
        """
        try:
            self.mysql_cursor.execute("SHOW TABLES")
            tables = [table[f"Tables_in_{self.mysql_conn.database}"] for table in self.mysql_cursor.fetchall()]
            print(f"Tablas encontradas en MySQL: {tables}")

            for table in tables:
                print(f"Migrando tabla: {table}")
                self.migrate_table(table)

            print("Migración completada con éxito.")
        except Exception as e:
            print(f"Error durante la migración: {e}")
            raise

    def close_connections(self):
        """Cierra las conexiones a MySQL y PostgreSQL."""
        if self.mysql_conn:
            self.mysql_conn.close()
        if self.postgres_conn:
            self.postgres_conn.close()
