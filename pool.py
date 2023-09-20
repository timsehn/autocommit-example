import mysql.connector

def main():
    # Clean up so I can run again
    # Can't use a pool here because a transaction begins
    # when the pool is created. If IU get unlucky, I'll get duplicate
    # primary key errors.
    no_pool_conn = mysql.connector.connect(user = "root",
                                           host = "127.0.0.1",
                                           port = 3306,
                                           database = "autocommit_example")

    cursor = no_pool_conn.cursor()
    cursor.execute("delete from t")
    cursor.execute("commit")
    cursor.close()
    no_pool_conn.close()
    
    # No transactions
    conn1 = mysql.connector.connect(user = "root",
                                    host = "127.0.0.1",
                                    port = 3306,
                                    database = "autocommit_example",
                                    pool_name = "mypool",
                                    pool_size=3)
    cursor = conn1.cursor()
    cursor.execute("insert into t values (0,'An uncommitted transaction')")
    cursor.close()

    conn2 = mysql.connector.connect(pool_name = "mypool")
    cursor = conn2.cursor()
    cursor.execute("select * from t")
    results = cursor.fetchall()
    print("Reading an uncommitted transaction. Will show empty.")
    print(results)
    cursor.close()
    conn2.close()

    # Rollback on conn1
    conn1.cursor().execute("rollback")

    # Transactions
    conn = mysql.connector.connect(pool_name = "mypool")
    cursor = conn.cursor()
    cursor.execute("insert into t values (0,'A committed transaction.')")
    cursor.execute("commit")
    cursor.close()
    conn.close()

    # Leaving this here to show you it's reading off an
    # old commit (potentially)
    conn = mysql.connector.connect(pool_name = "mypool")
    cursor = conn.cursor()
    cursor.execute("select * from t")
    results = cursor.fetchall()
    print("Potentially Reading off transaction begun when pool was made. Will likely show empty.")
    print(results)
    cursor.close()
    conn.close()

    # Start a new transaction to read committed transaction 
    conn = mysql.connector.connect(pool_name = "mypool")
    cursor = conn.cursor()
    cursor.execute("start transaction")
    cursor.execute("select * from t")
    results = cursor.fetchall()
    print("Will show new row.")
    print(results)
    cursor.close()
    conn.close()

    # autocommit works as you'd expect
    auto_conn = mysql.connector.connect(user = "root",
                                        host = "127.0.0.1",
                                        port = 3306,
                                        database = "autocommit_example",
                                        pool_name = "autopool",
                                        pool_size=3,
                                        autocommit=True)

    auto_conn.cursor().execute("insert into t values (1,'Every connection can read this')")
    cursor = auto_conn.cursor()
    cursor.execute("select * from t")
    results = cursor.fetchall()
    print("Will show two rows.")
    print(results)
    
main()
