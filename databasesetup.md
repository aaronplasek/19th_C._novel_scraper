*Building a database on a Mac*  
====================

*Step 1: install Mysql*

Mac: The easiest way to install all necessary packages is to use Homebrew (http://brew.sh/) . You can follow the instructions at the Homebrew site. After that, you need to install the Mysql package. Just open and terminal and type: 
`brew install mysql`

To code in python you'll need a program called Pip. Homebrew provides Pip via
`brew install python` (Preferred option since OS X's built-in version of python is usually less-than-current.) 

However you will then have two Pythons installed on your Mac, so alternatively you use 
`sudo easy_install pip`. (Not the preferred option.)  


After that, install the Mysqldb-python lib:
`pip install MySQL-python`

NOTE: If homebrew and pip are having problems installing packages, it could be that your permissions on OS X need to be fixed. You can easily check and fix your permissions using Apple's "Disk Utility" program.

*Step 2: Start & stop mySQL server*

There are a number of ways to start your mysql server:

(1) `mysqld` (starts server regardless of OS being used; not preferred)

(2) `mysqld_safe` (tries to predict best sql settings and then starts server; still not preferred)

(3) Use the mysql.server script to start and stop server. This is the preferred method. Simply type at terminal:

     `mysql.server start`  

     `mysql.server stop`
     
*Step 3: Creating Users*

When you first start your sql server, you won't have any users. We'll need to add some since you can't do anything in the database except as logged on as a user.

To log on as the root user into MySQL monitor, type

`mysql -uroot -p` (in the terminal command line; the default password is blank)

This will automatically log you in to MySQL monitor (i.e., you will be at the "mysql>" prompt). Now we can create a user account for normal usage by typing:

`CREATE USER 'collector'@'localhost' IDENTIFIED BY '123456';`  (This identifies a user "collector" with a password "123456")

Note that the user and the password must match what is specified by epigrapscraper.py script. Now we need our "collector" account to do stuff to the database so we should 

`GRANT ALL PRIVILEGES ON *.* TO 'collector'@'localhost' WITH GRANT OPTION;`


*Step 4: Create a database*

At "mysql>" prompt and logged on as "root" user, create a database named "EPIDB" by typing

`CREATE DATABASE EPIDB;`

You can see all the existing databases on the MySQL server via

`SHOW DATABASES;`
