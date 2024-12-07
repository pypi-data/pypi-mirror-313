import mysql.connector

def connect_mysql(host, port, user, password, database):
    """
    Conecta a una base de datos MySQL.

    Guia:
        host (str): Direccion del host de MySQL.
        port (int): Puerto del servidor MySQL.
        user (str): Usuario de MySQL.
        password (str): Contraseña de MySQL.
        database (str): Nombre de la base de datos.
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor(dictionary=True)
        print("Conexión a MySQL exitosa.")
        return conn, cursor
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise
