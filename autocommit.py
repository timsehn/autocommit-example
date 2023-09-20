import mysql.connector

def main():
    conn_args = {
        "user": "root",
        "host": "127.0.0.1",
        "port": 3306,
        "database": "autocommit_example",
        "autocommit": True
    }
    
    # Clean up so I can run again
    conn = mysql.connector.connect(**conn_args)
    other_conn = mysql.connector.connect(**conn_args)

    cursor = conn.cursor()
    cursor.execute("delete from t")

    # Insert a value
    cursor.execute("insert into t values (0, 'Every other connection can read this')")
    # Read the value on same connection
    cursor.execute("select * from t")
    results = cursor.fetchall()
    print(results)

    cursor = other_conn.cursor()
    # Read the value on the other connection
    cursor.execute("select * from t")
    results = cursor.fetchall()
    print(results)

    conn.close()
    other_conn.close()

main()
