from sqlalchemy.dialects import registry
from sqlalchemy.dialects.sqlite.base import SQLiteDialect

registry.register('devart.dynamicsbc', 'devart.dynamicsbc.sqlalchemy', 'DevartDynamicsBCDialect')

class DevartDynamicsBCDialect(SQLiteDialect):
    driver = "devart"
    name = "dynamicsbc"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.dynamicsbc
        dynamicsbc_package = devart.dynamicsbc
        setattr(dynamicsbc_package, "sqlite_version_info", (3, 39, 2))
        return dynamicsbc_package

    def get_isolation_level(self, dbapi_connection):
        return "SERIALIZABLE"
    
    def has_table(self, connection, table_name, schema=None, **kw):
        self._ensure_has_table_connection(connection)

        if schema is not None and schema not in self.get_schema_names(
            connection, **kw
        ):
            return False

        cursor = connection.connection.cursor()
        try:
            try:
                cursor.execute("select * from {} where 1 = 0".format(table_name))
                exists = True
            except:
                exists = False
        finally:
            cursor.close()
        return exists
        
    def has_table(self, connection, table_name, schema=None, **kw):
        self._ensure_has_table_connection(connection)
        query = "select TABLE_NAME as name from SYS_TABLES where TABLE_NAME = '{}'".format(table_name)
        names = connection.exec_driver_sql(query).scalars().all()
        return len(names) > 0
    
    def get_table_names(
        self, connection, schema=None, sqlite_include_internal=False, **kw
    ):
        query = "select TABLE_NAME as name from SYS_TABLES order by TABLE_NAME"
        names = connection.exec_driver_sql(query).scalars().all()
        return names
