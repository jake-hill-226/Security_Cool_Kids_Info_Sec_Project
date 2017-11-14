import sqlite3

# Description:
# Connect to database
# Note:
# Run this first!
def connect(path='data/carrot'):
	try:
		CarrotDB.conn = sqlite3.connect(path)
		CarrotDB.c = CarrotDB.conn.cursor()
	except Exception as e:
		print(e)

# Description:
# Disconnect from database
# Note:
# Run this last and always run!
def disconnect():
	try:
		CarrotDB.c.close()
		CarrotDB.conn.close()
	except Exception as e:
		print(e)

class CarrotDB:
	conn = None
	c = None

# Description:
# Use User class to create, modify, or delete user from database
class User():
	
	def __init__(self):
		self.reset()

	# DO NOT USE THIS! This is a private function
	def reset(self):
		self.row_id = None
		self.username = None
		self.password = None
		self.auth_options = 0
		self.email = None
		self.phone = None

		# old values - DO NOT MODIFY THEM!
		self.row_id_old = None
		self.username_old = None
		self.password_old = None
		self.auth_options_old = 0
		self.email_old = None
		self.phone_old = None

	# DO NOT USE THIS! This is a private function!
	def copy_to_old(self):
		self.row_id_old = self.row_id
		self.username_old = self.username
		self.password_old = self.password
		self.auth_options_old = self.auth_options
		self.email_old = self.email
		self.phone_old = self.phone

	# Description:
	# Use username to fetch user info
	# Req:
	# self.username		
	def fetch(self):

		if (self.username == None):
			print "username required for fetch()"
			return None

		CarrotDB.c.execute('SELECT * FROM users WHERE username=?', (self.username,))
		row = CarrotDB.c.fetchone()
		if (row == None):
			print "user \"%s\" is not found" % self.username
			return None
		else:
			self.row_id = row[0]
			self.password = row[2]
			self.auth_options = row[3]
			self.email = row[4]
			self.phone = row[5]
			# update old values too
			self.copy_to_old()
			print row
		return True
	# Description:
	# Insert new user into database. After success, row_id is assigned
	# Req:
	# self.username, self.password
	def insert(self):
		
		if (self.username == None or self.password == None):
			print "username and password required for insert()"
			return None

		CarrotDB.c.execute('SELECT COUNT(*) FROM users WHERE username=?', (self.username,))
		(num_rows,) = CarrotDB.c.fetchone()
		if (num_rows > 0):
			print "user \"%s\" already exists" % self.username
		else:
			CarrotDB.c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, self.password))
			CarrotDB.conn.commit()
			self.row_id = CarrotDB.c.lastrowid
			self.copy_to_old()
			print "user \"%s\" added, id %d assigned" % (self.username, self.row_id)

	# Description:
	# Update user info in database, using:
	# self.username -> cannot be empty; must be unique
	# self.password -> cannot be empty
	# self.auth_options -> only accept 0, 1, 2; otherwise, ignore
	# self.email -> must be unique
	# self.phone -> must be unique
	# Req:
	# self.row_id
	def update(self):
		
		if (self.row_id == None):
			print "row_id required for update()"
			return None
		elif (self.username == "" or self.username == None or self.password == "" or self.password == None):
			print "username and password must not be empty for update()"
			return None

		# check username uniqueness if changed
		if (self.username != self.username_old):
			CarrotDB.c.execute('SELECT COUNT(*) FROM users WHERE username=?', (self.username,))
			(num_rows,) = CarrotDB.c.fetchone()
			if (num_rows > 0):
				print "user \"%s\" already exists" % self.username
				return None

		# check email uniqueness if changed
		if (self.username != self.username_old):
			CarrotDB.c.execute('SELECT COUNT(*) FROM users WHERE email=?', (self.email,))
			(num_rows,) = CarrotDB.c.fetchone()
			if (num_rows > 0):
				print "email address \"%s\" already exists" % self.email
				return None

		# check phone uniqueness if changed
		if (self.username != self.username_old):
			CarrotDB.c.execute('SELECT COUNT(*) FROM users WHERE phone=?', (self.phone,))
			(num_rows,) = CarrotDB.c.fetchone()
			if (num_rows > 0):
				print "phone number \"%s\" already exists" % self.phone
				return None

		# check auth_options
		if (self.auth_options != 0 and self.auth_options != 1 and self.auth_options != 2):
			self.auth_options = self.auth_options_old

		CarrotDB.c.execute('UPDATE users SET username=?, password=?, auth_options=?, email=?, phone=? WHERE row_id=?',
			(self.username, self.password, self.auth_options, self.email, self.phone, self.row_id))
		CarrotDB.conn.commit()
		if (CarrotDB.c.rowcount == 0):
			print "Failed to update user with row_id %d: no rows affected" % self.row_id
		else:
			self.copy_to_old()

	# Description:
	# Delete user from database
	# Req:
	# self.row_id
	def delete(self):
		
		if (self.row_id == None):
			print "row_id required for delete()"
			return None

		CarrotDB.c.execute('DELETE FROM users WHERE row_id=?', (self.row_id,))
		CarrotDB.conn.commit()
		if (CarrotDB.c.rowcount == 0):
			print "Failed to delete user with row_id %d: no rows affected" % self.row_id
		else:
			self.reset()

	def display(self): # display user info
		print "Current Value\nrow_id: %s\nusername: %s\npassword: %s\nauth_options: %s\nemail: %s\nphone: %s\n" % (self.row_id, self.username, self.password, self.auth_options, self.email, self.phone)
		print "Old Value\nrow_id: %s\nusername: %s\npassword: %s\nauth_options: %s\nemail: %s\nphone: %s\n" % (self.row_id_old, self.username_old, self.password_old, self.auth_options_old, self.email_old, self.phone_old)

	# Description:
	# Return a LIST of object Entry, filtered by "search"
	# Req:
	# self.username or self.row_id
	def getVault(self, search=None): # ???
		
		if (self.row_id == None):
			self.fetch()

		if (search != '' and search != None):
			search = search + "%"
			params = (self.row_id, search)
			q = ' AND url LIKE ?'
		else:
			params = (self.row_id,)
			q = ''

		entries = []
		for row in CarrotDB.c.execute('SELECT * FROM vaults WHERE user_id = ?' + q, params):
			entries.append(Entry(row))
		return entries

class Entry():
	
	def __init__(self, entry=None):
		if (entry == None):
			self.reset()
		else:
			self.entry_id = entry[0]
			self.user_id = entry[1]
			self.url = entry[2]
			self.username = entry[3]
			self.password = entry[4]
			self.details = entry[5]
			self.copy_to_old()

	# DO NOT USE THIS! This is a private function
	def reset(self):
		self.entry_id = None
		self.user_id = None
		self.url = None
		self.username = None
		self.password = None
		self.details = None

		# old values - DO NOT MODIFY THEM!
		self.entry_id_old = None
		self.user_id_old = None
		self.url_old = None
		self.username_old = None
		self.password_old = None
		self.details_old = None

	# DO NOT USE THIS! This is a private function!
	def copy_to_old(self):
		self.entry_id_old = self.entry_id
		self.user_id_old = self.user_id
		self.url_old = self.url
		self.username_old = self.username
		self.password_old = self.password
		self.details_old = self.details

	# Description:
	# Use entry_id or (user_id, url) to fetch an entry
	# Req:
	# self.entry_id or (self.user_id, self.url)
	def fetch(self):
		
		if (self.entry_id != None):
			query = "SELECT * FROM vaults WHERE entry_id=?"
			params = (self.entry_id,)
		elif (self.user_id != None and self.url != None):
			query = "SELECT * FROM vaults WHERE user_id=? AND url=?"
			params = (self.user_id, self.url)
		else:
			print "entry_id or (user_id, url) required for fetch()"
			return None

		CarrotDB.c.execute(query,params)
		row = CarrotDB.c.fetchone()
		if (row == None):
			print "entry " + str(params) + " is not found"
			return None
		else:
			self.entry_id = row[0]
			self.user_id = row[1]
			self.url = row[2]
			self.username = row[3]
			self.password = row[4]
			self.details = row[5]
			# update old values too
			self.copy_to_old()
			print row
		return True


	# Description:
	# Insert a new entry into database for user. After success, entry_id is assigned
	# Req:
	# self.user_id, self.url, self.username, self.password
	def insert(self):
		
		if (self.user_id == None or self.url == None or self.url == "" or self.username == None or self.username == "" or self.password == None or self.password == ""):
			print "user_id, url, username, password required for insert()"
			return None

		# check foreign key
		CarrotDB.c.execute('SELECT COUNT(*) FROM users WHERE row_id=?', (self.user_id,))
		(num_rows,) = CarrotDB.c.fetchone()
		if (num_rows == 0):
			print "user \"%d\" is not found" % self.user_id
			return None

		# check uniqueness
		CarrotDB.c.execute('SELECT COUNT(*) FROM vaults WHERE user_id=? AND url=?', (self.user_id, self.url))
		(num_rows2,) = CarrotDB.c.fetchone()
		if (num_rows2 > 0):
			print "entry (%d, %s) already exists" % (self.user_id, self.url)
			return None

		# insert
		CarrotDB.c.execute('INSERT INTO vaults (user_id, url, username, password) VALUES (?, ?, ?, ?)', (self.user_id, self.url, self.username, self.password))
		CarrotDB.conn.commit()
		self.entry_id = CarrotDB.c.lastrowid
		self.copy_to_old()
		print "entry (%s, %s, %s) added to user %d, entry_id %d assigned" % (self.url, self.username, self.password, self.user_id, self.entry_id)

	# Description:
	# Update entry info in database, using:
	# self.user_id -> ignore
	# self.url -> cannot be empty; must be unique with user_id
	# self.username -> cannot be empty
	# self.password -> cannot be empty
	# self.details
	# Req:
	# self.entry_id, self.user_id
	def update(self):
		
		if (self.entry_id == None):
			print "entry_id required for update()"
			return None
		elif (self.user_id == None):
			print "user_id required for update()"
			return None
		elif (self.url == "" or self.url == None or self.username == "" or self.username == None or self.password == "" or self.password == None):
			print "url, username, password required for update()"
			return None

		# check ownership 1
		if (self.user_id != self.user_id_old):
			self.user_id = self.user_id_old
			print "you cannot change the owner of a vault entry"
			return None

		# check ownership 2
		CarrotDB.c.execute('SELECT user_id FROM vaults WHERE entry_id=?', (self.entry_id,))
		(result,) = CarrotDB.c.fetchone()
		if (result != self.user_id):
			print "user_id doesn't match entry_id"
			return None

		# Do not need below because I need this func to change
		# an existing password (i.e. the url will be the same).

		# check url uniqueness if changed
		# if (self.url != self.url_old):
		# 	CarrotDB.c.execute('SELECT COUNT(*) FROM vaults WHERE user_id=? AND url=?', (self.user_id, self.url))
		# 	(num_rows,) = CarrotDB.c.fetchone()
		# 	if (num_rows > 0):
		# 		print "entry (%d, %s) already exists" % (self.user_id, self.url)
		# 		return None

		# update
		CarrotDB.c.execute('UPDATE vaults SET url=?, username=?, password=?, details=? WHERE entry_id=?',
			(self.url, self.username, self.password, self.details, self.entry_id))
		CarrotDB.conn.commit()
		if (CarrotDB.c.rowcount == 0):
			print "Failed to update entry with entry_id %d: no rows affected" % self.entry_id
		else:
			self.copy_to_old()

	# Description:
	# Delete entry from database
	# Req:
	# self.entry_id
	# Node:
	# If entry is in a list, for example, fetched from user.getVault(), remove this entry from that list!
	def delete(self):
		
		if (self.entry_id == None):
			print "entry_id required for delete()"
			return None

		CarrotDB.c.execute('DELETE FROM vaults WHERE entry_id=?', (self.entry_id,))
		CarrotDB.conn.commit()
		if (CarrotDB.c.rowcount == 0):
			print "Failed to delete entry with entry_id %d: no rows affected" % self.entry_id
		else:
			self.reset()

	def display(self): # display entry info
		print "Current Value\nentry_id: %s\nuser_id: %s\nurl: %s\nusername: %s\npassword: %s\ndetails: %s\n" % (self.entry_id, self.user_id, self.url, self.username, self.password, self.details)
		print "Old Value\nentry_id: %s\nuser_id: %s\nurl: %s\nusername: %s\npassword: %s\ndetails: %s\n" % (self.entry_id_old, self.user_id_old, self.url_old, self.username_old, self.password_old, self.details_old)


# testing
# connect()

# user = User()
# user.username = "xdk"
# user.fetch()

# disconnect()