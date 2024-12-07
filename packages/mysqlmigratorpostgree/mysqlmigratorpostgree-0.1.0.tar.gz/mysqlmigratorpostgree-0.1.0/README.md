# MysqlMigratorPostgree

## Introducción

**MysqlMigratorPostgree** es una librería en Python diseñada para facilitar la migración de bases de datos completas desde **MySQL** hacia **PostgreSQL**. Esta herramienta es ideal para ingenieros de software que buscan una solución automatizada para transferir datos y estructuras de tablas entre estos dos sistemas de gestión de bases de datos relacionales.

La librería ofrece:
- Conexión sencilla a servidores de MySQL y PostgreSQL.
- Migración automatizada de tablas, incluyendo columnas y tipos de datos.
- Manejo eficiente de conexiones y errores.
- Un diseño modular y extensible.

---

## Diccionario de Palabras Reservadas

Durante la migración, ciertos tipos de datos en **MySQL** no tienen un equivalente exacto en **PostgreSQL**. Este es un resumen de las conversiones realizadas por la librería:

| **Tipo en MySQL**     | **Tipo en PostgreSQL** | **Descripción**                                                                 |
|------------------------|------------------------|---------------------------------------------------------------------------------|
| `INT`                 | `INTEGER`             | Enteros de tamaño fijo.                                                        |
| `VARCHAR(n)`          | `TEXT`                | PostgreSQL no requiere límites estrictos para textos.                          |
| `TEXT`                | `TEXT`                | Se mantiene el mismo tipo para textos largos.                                  |
| `FLOAT`               | `REAL`                | Valores de punto flotante.                                                     |
| `DOUBLE`              | `DOUBLE PRECISION`    | Valores de mayor precisión en PostgreSQL.                                      |
| `DATE`                | `DATE`                | Fecha estándar en formato `YYYY-MM-DD`.                                        |
| `DATETIME`            | `TIMESTAMP`           | Fecha y hora con zona horaria.                                                 |
| `TINYINT(1)`          | `BOOLEAN`             | Interpretado como un valor lógico (`TRUE` o `FALSE`).                          |
| `ENUM`                | `TEXT`                | Convertido a texto, ya que PostgreSQL no soporta directamente el tipo `ENUM`.  |

---

## Detalles del Código

### **Estructura General**

La librería sigue un enfoque modular. Cada funcionalidad está definida en un archivo específico:
- **`connect_mysql.py`**: Maneja la conexión a un servidor MySQL.
- **`connect_postgresql.py`**: Maneja la conexión a un servidor PostgreSQL.
- **`migrator.py`**: Orquesta la migración de tablas y datos.

---

### **Cambios en los Tipos de Datos**

La lógica para convertir tipos de datos de MySQL a PostgreSQL se encuentra en el archivo `migrator.py`. Aquí está el fragmento clave del código con explicación:

```python
# Mapeo de tipos de datos
if "int" in column_type:
    postgres_type = "INTEGER"
elif "varchar" in column_type or "text" in column_type:
    postgres_type = "TEXT"
elif "float" in column_type or "double" in column_type:
    postgres_type = "REAL"
elif "date" in column_type:
    postgres_type = "DATE"
elif "tinyint(1)" in column_type:
    postgres_type = "BOOLEAN"
else:
    postgres_type = "TEXT"  # Tipo predeterminado si no hay un mapeo específico

## Código de Ejemplo

Aquí tienes un ejemplo funcional que muestra cómo usar la librería para migrar todas las tablas de una base de datos MySQL a PostgreSQL:

```python
from mysqlmigratorpostgree import MysqlMigratorPostgree

# Instanciar el migrador
migrator = MysqlMigratorPostgree()

# Conectar a MySQL
migrator.connect_mysql(
    host="localhost",
    port=3306,  # Puerto predeterminado de MySQL
    user="root",
    password="password",  # Cambiar por tu contraseña
    database="databases_name"
)

# Conectar a PostgreSQL
migrator.connect_postgresql(
    host="localhost",
    port=5432,  # Puerto predeterminado de PostgreSQL
    user="postgres",
    password="password",  # Cambiar por tu contraseña
    database="databases_name"
)

# Migrar todas las tablas
migrator.migrate_all()

# Cerrar conexiones
migrator.close_connections()
```