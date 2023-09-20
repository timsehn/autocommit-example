# autocommit-example

An example of using the Python database connector that has autocommit off by default.

# Setup

This example uses [Dolt](https://www.doltdb.com) as the SQL database. To setup:

```bash
$ mkdir autocommit_example
$ cd autocommit_example 
$ dolt init --fun
Successfully initialized dolt data repository.
$ dolt sql -q "create table t (id int primary key, words varchar(255)"
$ dolt sql-server
```

# Running scripts

Once you've setup, you run a script like so:
```bash
$ python pool.py
Reading an uncommitted transaction. Will show empty.
[]
Potentially Reading off transaction begun when pool was made. Will likely show empty.
[]
Will show new row.
[(0, 'A committed transaction.')]
Will show two rows.
[(0, 'A committed transaction.'), (1, 'Every connection can read this')]
```
