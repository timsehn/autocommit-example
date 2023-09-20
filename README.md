# autocommit-example

An example of using the Python database connector that has autocommit off by default.

# Setup

This eaxmple uses [Dolt](https://www.doltdb.com) as the SQL database.
```bash
$ cd dolt
$ mkdir autocommit_example
$ cd autocommit_example 
$ dolt init --fun
Successfully initialized dolt data repository.
$ dolt sql -q "create table t (id int primary key, words varchar(255)"
$ dolt sql-server
```
