import CarrotDB
import vault_encrypt
from Headless_Browser import Auto_PW_Change

def setup():
	# Prompt User for login credentials

	# Initialize user in DB

	# Prompt User to enter new passwords to vault

	return None

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

	# decrypt stored password with user credentials
	vault_pass = vault_encrypt.decrypt(entry.password, password)

	CarrotDB.disconnect()

	return vault_pass

def store_new_pass(username, url, details="N/A", password):
	CarrotDB.connect()

	user = CarrotDB.User()
	user.username = username
	user.fetch()

	ntry = CarrotDB.Entry()
	entry.user_id = user.row_id
	entry.url = url
	entry.username = username
	entry.details = details

	new_pass = vault_encrypt.pwd_gen()

	encrypt_pass = vault.encrypt(new_pass, password)

	entry.password = encrypt_pass

	entry.insert()

	CarrotDB.disconnect()