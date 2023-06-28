import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="strum",
    user="postgres",
    password="1234"
)


cursor = conn.cursor()

create_client_table_query = """
CREATE TABLE IF NOT EXISTS client(
    idclient SERIAL PRIMARY KEY,
    idwishlist INT,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    idtelegram VARCHAR(255)
)
"""

create_wishlist_table_query = """
CREATE TABLE IF NOT EXISTS wishlist (
    idwishlist SERIAL PRIMARY KEY,
    idclient INT,
    idgame INT
)
"""

create_game_table_query = """
CREATE TABLE IF NOT EXISTS game (
    idgame SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price VARCHAR(255),
    discount INT,
    promo BOOLEAN,
    idwishlist INT
)
"""

# Execute table creation queries
cursor = conn.cursor()
cursor.execute(create_client_table_query)
#cursor.execute(create_wishlist_table_query)
#cursor.execute(create_game_table_query)
conn.commit()