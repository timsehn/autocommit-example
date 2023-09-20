import mysql.connector

def main():
    conn_args = {
        "user": "root",
        "host": "127.0.0.1",
        "port": 3306,
        "database": "autocommit_example",
    }
    
    # Clean up so I can run again
    conn       = mysql.connector.connect(**conn_args)

    cursor = conn.cursor()
    cursor.execute("delete from t")
    cursor.execute("commit")

    # Only establish the connection once I'm sure I've cleaned up
    other_conn = mysql.connector.connect(**conn_args)
    
    # Insert a value
    cursor.execute("insert into t values (0, 'Only this connection can read this')")
    # Read the value on same connection
    cursor.execute("select * from t")
    results = cursor.fetchall()
    print(results)

    other_cursor = other_conn.cursor()
    # Read the value on the other connection
    other_cursor.execute("select * from t")
    results = other_cursor.fetchall()
    print("Will be empty")
    print(results)

    cursor = conn.cursor()
    cursor.execute("commit")
    
    other_cursor.execute("select * from t")
    results = other_cursor.fetchall()
    print("Still empty")
    print(results)

    other_cursor.execute("start transaction")
    other_cursor.execute("select * from t")
    results = other_cursor.fetchall()
    print("Finally I can see the row")
    print(results)

    conn.close()
    other_conn.close()

main()
