import psycopg2
from psql import sql

def insert_client(first_name, last_name, idtelegram):
    conn = psycopg2.connect(
        host="postgresql",
        port="5432",
        database="postgres",
        user="postgres",
        password="mysecretpassword"
    )
    cursor = conn.cursor()

    # Check if the user already exists
    check_user_query = """
    SELECT idclient FROM client
    WHERE firstname = %s AND lastname = %s
    """
    cursor.execute(check_user_query, (first_name, last_name))
    existing_user = cursor.fetchone()

    if existing_user:
        # User already exists, retrieve the user's ID
        user_id = existing_user[0]
        print(f"User already exists. ID: {user_id}")
        return user_id

    else:
        # Insert the new user into the client table
        insert_user_query = """
        INSERT INTO client (firstname, lastname, idtelegram)
        VALUES (%s, %s, %s)
        RETURNING idclient
        """
        cursor.execute(insert_user_query, (first_name, last_name, idtelegram))
        user_id = cursor.fetchone()[0]
        return user_id


    # Commit the changes
    conn.commit()

    # Close the cursor
    cursor.close()

def add_game_to_wishlist(client_id, game_name, game_price, game_discount, game_promotion):
    conn = psycopg2.connect(
        host="postgresql",
        port="5432",
        database="postgres",
        user="postgres",
        password="mysecretpassword"
    )
    cursor = conn.cursor()

    # Insert the game into the game table
    insert_game_query = """
    INSERT INTO game (name, price, discount, promo, idwishlist)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING idgame
    """
    cursor.execute(insert_game_query, (game_name, game_price, game_discount, game_promotion, None))
    game_id = cursor.fetchone()[0]

    try:
        # Get the wishlist ID for the given client ID
        get_wishlist_query = """
        SELECT idwishlist FROM wishlist
        WHERE idclient = %s
        """
        cursor.execute(get_wishlist_query, (client_id,))
        wishlist_id = cursor.fetchone()[0]

    except TypeError:
        # Wishlist doesn't exist, create a new one
        create_wishlist_query = """
        INSERT INTO wishlist (idclient, idgame)
        VALUES (%s, %s)
        RETURNING idwishlist
        """
        cursor.execute(create_wishlist_query, (client_id, game_id))
        wishlist_id = cursor.fetchone()[0]

    # Connect the game and wishlist in the client table
    update_client_query = """
    UPDATE client
    SET idgame = %s, idwishlist = %s
    WHERE idclient = %s
    """
    cursor.execute(update_client_query, (game_id, wishlist_id, client_id))

    update_game_query = """
    UPDATE game
    SET idwishlist = %s
    WHERE idgame = %s
    """
    cursor.execute(update_game_query, (wishlist_id, game_id))

    # Commit the changes
    conn.commit()

    # Close the cursor
    cursor.close()

#Create tables first thing
sql.create_tables()

# Establish a connection to the PostgreSQL container
conn = psycopg2.connect(
    host="postgresql",
    port="5432",
    database="postgres",
    user="postgres",
    password="mysecretpassword"
)

# Create a cursor object to interact with the database
cursor = conn.cursor()

create_user_query = """
INSERT INTO client (firstname, lastname, idtelegram)
VALUES ('Emilio', 'Gabriel', '1224465429')
RETURNING idclient
"""

cursor = conn.cursor()

# Execute the SELECT query
select_query = """
SELECT * FROM client
"""

cursor.execute(select_query)
rows = cursor.fetchall()

# Display the retrieved entries
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()

