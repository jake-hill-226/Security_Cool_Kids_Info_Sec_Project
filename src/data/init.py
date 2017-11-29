# Author: Dikai Xiong
# Class: CSE 4471, AU17, 11:10 WF

import sqlite3

def main ():
	# default database path is "data/carrot"
	conn = sqlite3.connect('data/carrot')
	conn.execute('PRAGMA foreign_keys = ON')
	c = conn.cursor()
	# users table
	c.execute('''
	CREATE TABLE IF NOT EXISTS users(
		row_id INTEGER PRIMARY KEY,
		username TEXT NOT NULL,
		password TEXT NOT NULL,
		auth_options INTEGER NOT NULL DEFAULT 0,
		email TEXT,
		phone TEXT
	)
		''')
	conn.commit()
	# vaults table
	c.execute('''
	CREATE TABLE IF NOT EXISTS vaults(
		entry_id INTEGER PRIMARY KEY,
		user_id INTEGER NOT NULL,
		url TEXT NOT NULL,
		username TEXT NOT NULL,
		password TEXT NOT NULL,
		details TEXT,
		FOREIGN KEY (user_id) REFERENCES users (row_id)
	)
		''')
	conn.commit()
	# create indexes
	c.executescript('''
	CREATE UNIQUE INDEX unique_username ON users (username);
	CREATE UNIQUE INDEX unique_email ON users (email);
	CREATE UNIQUE INDEX unique_phone ON users (phone);
	CREATE INDEX vault_index1 ON vaults (user_id, url)
		''')
	conn.commit()
	conn.close()

# main()