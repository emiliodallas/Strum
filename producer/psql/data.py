import psycopg2

def insert_client(idtelegram, first_name, last_name):
    conn = psycopg2.connect(
        host="postgresql",
        port="5432",
        database="postgres",
        user="postgres",
        password="mysecretpassword"
    )

    try:
        cursor = conn.cursor()

        # Check if the user already exists
        check_user_query = """
        SELECT idtelegram FROM client
        WHERE idtelegram = %s
        """
        cursor.execute(check_user_query, (idtelegram,))
        existing_user = cursor.fetchone()

        if existing_user:
            # User already exists, retrieve the user's ID
            user_id = existing_user[0]
            print(f"User already exists. ID: {user_id}")

        else:
            # Insert the new user into the client table
            insert_user_query = """
            INSERT INTO client (idtelegram, firstname, lastname)
            VALUES (%s, %s, %s)
            RETURNING idtelegram
            """
            cursor.execute(insert_user_query, (idtelegram, first_name, last_name))
            user_id = cursor.fetchone()[0]

            # Commit the changes for the new user
            conn.commit()

        return user_id

    except psycopg2.Error as e:
        print(f"Error: {e}")
        # Rollback the transaction in case of an error
        conn.rollback()
        return None

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

        

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
    print(" 1 ")
    try:
        # Get the wishlist ID for the given client ID
        get_wishlist_query = """
        SELECT idwishlist FROM wishlist
        WHERE idclient = %s
        """
        cursor.execute(get_wishlist_query, (client_id,))
        wishlist_id = cursor.fetchone()[0]
        print(" 2 ")

    except TypeError:
        # Wishlist doesn't exist, create a new one
        create_wishlist_query = """
        INSERT INTO wishlist (idclient, idgame)
        VALUES (%s, %s)
        RETURNING idwishlist
        """
        cursor.execute(create_wishlist_query, (client_id, game_id))
        wishlist_id = cursor.fetchone()[0]
        print(" 3 ")

    # Connect the game and wishlist in the client table
    update_client_query = """
    UPDATE client
    SET idgame = %s, idwishlist = %s
    WHERE idclient = %s
    """
    cursor.execute(update_client_query, (game_id, wishlist_id, client_id))
    print(" 4 ")

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


def wishlist_query(idtelegram):

    connection = psycopg2.connect(
        host="postgresql",
        port="5432",
        database="postgres",
        user="postgres",
        password="mysecretpassword"
    )

    # Query the client table to get idwishlist
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT idwishlist FROM client WHERE idtelegram = {idtelegram}")
        result = cursor.fetchone()
        if result:
            idwishlist = result[0]
            # Query the game table to get games associated with idwishlist
            cursor.execute(f"SELECT * FROM game WHERE idwishlist = {idwishlist}")
            wishlist = cursor.fetchall()
            return wishlist
        else:
            return None


#Create tables first thing
#sql.create_tables()
'''
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
'''
