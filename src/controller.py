import CarrotDB
import carrot_encrypt
import vault_encrypt
from Headless_Browser import Auto_PW_Change
from pyautogui import press, typewrite, hotkey
import re
import binascii

def setup():
	# Prompt User for login credentials

	# Create User

	# Initialize user in DB

	# Prompt User to enter new passwords to vault

	return None

def create_new_user(username, password, auth_options, email=None, phone=None):
	CarrotDB.connect()

	# grab user credentials
	user = CarrotDB.User()
	user.username = username
	user.password = vault_encrypt.hash_user_pwd(password)
	user.auth_options = auth_options
	if email:
		user.email = email
	if phone:
		user.phone = phone

	user.insert()

def update_user_prefs(username, new_username=None, password=None, auth_options=None, email=None, phone=None):
	CarrotDB.conntect()

	# grab user credentials
	user = CarrotDB.User()
	user.username = username
	user.fetch()

	if password:
		user.password = vault_encrypt.hash_usr_pwd(password)
	if auth_options:
		user.auth_options = auth_options
	if email and re.search('^.*@.*\....$', email):
		user.email = email
	else:
		print "Error: invalid email format. Attribute not updated in database"
	if phone and re.search('^\d\d\d-\d\d\d-\d\d\d\d$', phone):
		user.phone = phone
	else:
		print "Error: invalid phone number format. Attribute not updated in database"
	CarrotDB.disconnect()

"""
# Used to obtain plaintext password from database

# username: The user name of the currently logged on
			user
# url: The url for the account associated with the
	   desired password
# password: The authenticated user's password
# return val: Plaintext password matching the username,
			  url pair
"""
def retrieve_pass(username, url, password):
	CarrotDB.connect()
	
	# grab user credentials
	user = CarrotDB.User()
	user.username = username
	user.fetch()

	# grab entry credentials
	entry = CarrotDB.Entry()
	entry.user_id = user.row_id
	entry.url = url
	entry.fetch()

	#
	#if (not(carrot_encrypt.check_key(pwd))):
		#key = carrot_encrypt.fit_key(pwd)
	#else:
	       # key = pwd
	#Create AES stream object
 	#aes = carrot_encrypt.AESModeOfOperationCTR(key)
    	#plaintext = aes.decrypt(pwd)
	
	# decrypt stored password with user credentials
	if entry.password:
		# byte_pass = binascii.unhexlify(entry.password)
		byte_pass = binascii.unhexlify(entry.password)
		print byte_pass
		# byte_pass = bin(int(entry.password, 16))[2:]

		vault_pass = vault_encrypt.decrypt(byte_pass, password)

	CarrotDB.disconnect()

	return vault_pass


"""
# Used to generate and insert a new password 
  into the database
# username: The user name of the currently logged on
			user
# url: The url for the account associated with the
	   new password
# password: The authenticated user's password
# return val: None(error occured) or True(success)
# result: Either a new url, password pair is inserted
		  inserted into the database or an error occured.
"""
def store_new_pass(username, url, password, details="N/A"):
	CarrotDB.connect()

	result = True

	user = CarrotDB.User()
	user.username = username
	user.fetch()

	print "user fetched"
	if not user.fetch():
		result = None
	else:
		entry = CarrotDB.Entry()

		entry.user_id = user.row_id
		entry.url = url
		entry.username = username
		entry.details = details


		if entry.fetch():
			result = None
		else:
			new_pass = vault_encrypt.pwd_gen()

		# 	key = None
		# 	if (not(carrot_encrypt.check_key(password))):
		# 	        key = carrot_encrypt.fit_key(password)
		# 	else:
		# 	       key = password
		# 	#Create AES stream object
 	# 		aes = carrot_encrypt.AESModeOfOperationCTR(key)
		# 	encrypt_pass = aes.encrypt(new_pass).decode()
			encrypt_pass = binascii.hexlify(vault_encrypt.encrypt(new_pass, password))

			entry.password = encrypt_pass

			entry.insert()

	CarrotDB.disconnect()
	return result

"""
# Update an existing account password in database
# username: The user name of the currently logged on
			user
# url: The url for the account associated with the
	   password
# password: The authenticated user's password
# new_pass: The new password to be used for given account
# return val: None(error occured) or True(success)
# result: Either a new url, password pair is inserted
		  inserted into the database or an error occured.
"""
def update_pass(username, url, password, new_pass=None):
	CarrotDB.connect()
	
	result = True

	# grab user credentials
	user = CarrotDB.User()
	user.username = username
	user.fetch()

	if not user.fetch():
		result = None
	else:
		# grab entry credentials
		entry = CarrotDB.Entry()
		entry.user_id = user.row_id
		entry.url = url
		entry.fetch()
		if not entry.fetch():
			result = None
		else:
			if(new_pass == None):
				new_pass = vault_encrypt.pwd_gen()

			#if (not(carrot_encrypt.check_key(pwd))):
			        #key = carrot_encrypt.fit_key(pwd)
			#else:
			       # key = pwd
			#Create AES stream object
 			#aes = carrot_encrypt.AESModeOfOperationCTR(key)
    			#ciphertext = aes.encrypt(pwd)
			new_pass = binascii.hexlify(vault_encrypt.encrypt(new_pass, password))

			entry.password = new_pass

			entry.update()

	CarrotDB.disconnect()
	return result

"""
# Search for a password via its url
# username: The authenticated user
# search_string: A string to be pattern matched with
				 against entries in the database
# retrun val: A list containing all passwords matched to
			  to the search string.
"""
def search_vault(username, search_string=None):
	CarrotDB.connect()

	# grab user credentials
	user = CarrotDB.User()
	user.username = username
	user.fetch()

	results = user.getVault(search=search_string)

	CarrotDB.disconnect()

	return results

"""
# A helper method to similate the key stroke (alt+tab) 
"""
def sim_Alt_Tab():
	hotkey('alt','tab')

"""
# A helper method to circumvent copy/paste of passwords 
"""
def sim_typing(message):
	typewrite(message)
