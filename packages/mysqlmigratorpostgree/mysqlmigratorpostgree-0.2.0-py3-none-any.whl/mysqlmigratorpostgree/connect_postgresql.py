import psycopg2

def connect_postgresql(host, port, user, password, database):
    """
    Conecta a una base de datos PostgreSQL.

    Guia:
        host (str): Direccion del host de PostgreSQL.
        port (int): Puerto del servidor PostgreSQL.
        user (str): Usuario de PostgreSQL.
        password (str): Contraseña de PostgreSQL.
        database (str): Nombre de la base de datos.
    """
    try:
        # Establecer la conexión a PostgreSQL
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        # Crear un cursor para ejecutar consultas SQL
        cursor = conn.cursor()
        print("Conexión a PostgreSQL exitosa.")
        return conn, cursor
    except psycopg2.Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        raise