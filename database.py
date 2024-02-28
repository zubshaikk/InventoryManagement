import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

def create_item(conn, item):
    """
    Create a new item into the inventory table
    """
    sql = ''' INSERT INTO inventory(item_name,quantity,price)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, item)
    conn.commit()
    return cur.lastrowid

def select_all_items(conn):
    """
    Query all rows in the inventory table
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")

    rows = cur.fetchall()

    return rows

def create_inventory_table(conn):
    """
    Create the inventory table if it doesn't exist
    """
    sql = '''CREATE TABLE IF NOT EXISTS inventory (
                id integer PRIMARY KEY,
                item_name text NOT NULL,
                quantity integer,
                price real
             );'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def update_item(conn, item):
    """
    Update quantity and price of an item
    """
    sql = ''' UPDATE inventory
              SET quantity = ? ,
                  price = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, item)
    conn.commit()

def delete_item_by_id(conn, id):
    """
    Delete an item by item id
    """
    sql = 'DELETE FROM inventory WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

