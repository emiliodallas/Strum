import psycopg2

def create_tables():
    conn = psycopg2.connect(
        host="postgresql",
        port="5432",
        database="postgres",
        user="postgres",
        password="mysecretpassword"
    )
    cursor = conn.cursor()

    create_client_table_query = """
    CREATE TABLE IF NOT EXISTS client (
        idclient SERIAL PRIMARY KEY,
        firstname VARCHAR(255),
        lastname VARCHAR(255),
        idtelegram VARCHAR(255)
    )
    """

    create_wishlist_table_query = """
    CREATE TABLE IF NOT EXISTS wishlist (
        idwishlist SERIAL PRIMARY KEY,
        idclient INT REFERENCES client (idclient),
        idgame INT REFERENCES game (idgame)
    )
    """

    create_game_table_query = """
    CREATE TABLE IF NOT EXISTS game (
        idgame SERIAL PRIMARY KEY,
        name VARCHAR(255),
        price VARCHAR(255),
        discount INT,
        promo BOOLEAN
        idwishlist INT REFERENCES wishlist (idwishlist)
    )
    """

    cursor.execute(create_client_table_query)
    cursor.execute(create_wishlist_table_query)
    cursor.execute(create_game_table_query)

    conn.commit()
    cursor.close()
    conn.close()

create_tables()