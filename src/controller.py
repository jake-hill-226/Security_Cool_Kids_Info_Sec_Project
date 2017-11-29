"""
##########################################################
				controller

Description: This module is an inteface to link all feature components of CarrotKey 
			 to the front end GUI. All functions contained in this module access 
			 various modules of the application in order to facilitate the middle 
			 logic between the front-end interface and the back-end logic and management.

Contributors: Jake Hill
Last modified: 11/27/17			 
##########################################################
"""


import CarrotDB
import carrot_encrypt
import vault_encrypt
from Headless_Browser import Auto_PW_Change
from pyautogui import press, typewrite, hotkey
import re


"""
# Instantiates a new user for the application

# username: (string) The username of the new user
# password: (string) The application password for the new user
# auth_options: (int) An integer value associated with the method of authentication a user wants
					  when logging into the application. (optional)
					    1. password only
					    2. password and 2 factor auth via phone
					    3. password and 2 factor auth via email
# email: The new email address used in 2 factor auth for the user (optional)
# phone: The new phone number used in 2 factor auth for the user (optional)
"""
def create_new_user(username, password, auth_options, email=None, phone=None):
	CarrotDB.conntect()

	# grab user credentials
	user = CarrotDB.User()
	user.username = username
	user.password = password
	user.auth_options = auth_options
	if email:
		user.email = email
	if phone:
		user.phone = phone

	user.insert()

"""
# Used to modify an existing user's credentials and authentication preferences within
	the database.
# username: The username of an existing user of the application
# password: The new application password for the corresponding  user (optional)
# auth_options: An integer value associated with the method of authentication a user wants
				when logging into the application. (optional)
				1. password only
				2. password and 2 factor auth via phone
				3. password and 2 factor auth via email
# email: The new email address used in 2 factor auth for the user (optional)
# phone: The new phone number used in 2 factor auth for the user (optional)
"""
def update_user_prefs(username, password=None, auth_options=None, email=None, phone=None):
	CarrotDB.conntect()

	# grab user credentials
	user = CarrotDB.User()
	user.username = username
	user.fetch()

	# Change them according to the input parameters
	if password:
		user.password = vault_encrypt.hash_usr_pwd(password)
	if auth_options:
		user.auth_options = auth_options
	if email and re.search('^.*@.*\....$', email):
		# email is matched to a regular expression reflecting the standard email
		# format in order to prevent junk entries into the database.
		# This of course does not prevent the entry of invalid email addresses however,
		# it does prevent the entry of non-email like inputs
		user.email = email
	else:
		print "Error: invalid email format. Attribute not updated in database"
	if phone and re.search('^\d\d\d-\d\d\d-\d\d\d\d$', phone):
		# phone is matched to a regular expression reflecting the standard phone number
		# format in order to prevent junk entries into the database
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
		vault_pass = vault_encrypt.decrypt(entry.password, password)

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

		print "before conditional"

		if not entry.fetch():
			result = None
			print "entry exists"
		else:
			new_pass = vault_encrypt.pwd_gen()
			print "entry does not exist"

			#
			#if (not(carrot_encrypt.check_key(pwd))):
			        #key = carrot_encrypt.fit_key(pwd)
			#else:
			       # key = pwd
			#Create AES stream object
 			#aes = carrot_encrypt.AESModeOfOperationCTR(key)
    			#ciphertext = aes.encrypt(pwd)
			encrypt_pass = vault_encrypt.encrypt(new_pass, password)

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
			new_pass = vault_encrypt.encrypt(new_pass, password)

			entry.password = new_pass

			entry.update()

	CarrotDB.disconnect()
	return resul
t
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
# Simulates that typing of the provided message
# 
# message: The string to be typed using the keyboard emulator  
"""
def sim_typing(message):
	typewrite(message)
