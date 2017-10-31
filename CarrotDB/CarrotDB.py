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
def close():
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
		else:
			self.row_id = row[0]
			self.password = row[2]
			self.auth_options = row[3]
			self.email = row[4]
			self.phone = row[5]
			# update old values too
			self.copy_to_old()
			print row

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
			print "Failed to update user with row_id %d" % self.row_id
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
			print "Failed to delete user with row_id %d" % self.row_id
		else:
			self.reset()

	def display(self): # display user info
		print "username: %s\npassword: %s\nauth_options: %s\nemail: %s\nphone: %s\n" % (self.username, self.password, self.auth_options, self.email, self.phone)

	def getVault(self): # ???
		pass


class Entry():
	pass


# testing
# connect()

# user = User()
# user.username = "xdk"
# user.fetch()

# close()