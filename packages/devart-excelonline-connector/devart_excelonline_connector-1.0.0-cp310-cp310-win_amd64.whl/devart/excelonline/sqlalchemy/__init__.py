from sqlalchemy.dialects import registry
from sqlalchemy.dialects.sqlite.base import SQLiteDialect

registry.register('devart.excelonline', 'devart.excelonline.sqlalchemy', 'DevartExcelOnlineDialect')

class DevartExcelOnlineDialect(SQLiteDialect):
    driver = "devart"
    name = "excelonline"

    supports_statement_cache = False
    default_paramstyle = "named"

    @classmethod
    def import_dbapi(cls):
        import devart.excelonline
        excelonline_package = devart.excelonline
        setattr(excelonline_package, "sqlite_version_info", (3, 39, 2))
        return excelonline_package

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
