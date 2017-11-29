# Console based features demo

import controller
import carrot_encrypt
import vault_encrypt
#import twofactor
from Headless_Browser import Auto_PW_Change as auto_pass

choice = ""
result = ""

def print_buff():
	for i in range(60):
		print "\n"

while choice != "q":
	print """Welcome to the Carrot Key Console Interface
	Please make a selection
	1. Add user
	2. Create new pass
	3. Print passes for user
	4. Copy password into previouse window
	5. AES Demo
	6. Headless Browser Demo

	q. Quit Carrot Key
--------------------------------------------------
	"""

	choice = raw_input("Selection: ")

	if choice == '1':
		print "**Selected: 1. Add User**"
		username = raw_input("Enter Username: ")
		password = raw_input("Enter Password: ")
		auth_options = raw_input("Enter authorization options: ")
		email = raw_input("Enter email (optional may leave blank): ")
		phone = raw_input("Enter phone (optional may leave blank): ")

		controller.create_new_user(username, password, auth_options, email, phone)
		result = "New pass added: " + username + ", " + password + ", " + auth_options +", " + email + ", " + phone
	if choice == '2':
		print "**Selected: 2. Create new pass**"
		username = raw_input("Enter Username: ")
		password = raw_input("Enter Password: ")
		url = raw_input("Enter URL of login page: ")
		details = raw_input("Enter short desciption of account (optional): ")

		controller.store_new_pass(username, url, password, details)
		result = "New pass added: " + username + ", " + password + ", " + url + ", " + details

	if choice == '3':
		print "**Selected: 3. Print passes for user**"
		username = raw_input("Enter Username: ")

		pass_list = controller.search_vault(username)
		for pwd in pass_list:
			details = ""
			if pwd.details:
				details = pwd.details
			result = "ID: " + str(pwd.entry_id) + "\nusername: " + pwd.username + "\nurl: " + pwd.url + "\ndetails: " + details + "\npassword: " + pwd.password

	if choice == '4':
		print "**Selected: 4. Copy password into previouse window**"
		# username = raw_input("Enter Username: ")

		# pass_list = controller.search_vault(username)
		# entry = pass_list[0]
		
		# password = controller.retrieve_pass(entry.username, entry.url, entry.password)
		# result = "Encrypt-Pass: " + entry.password + "\nPlain-Text-Password: " + password

		message = raw_input("Enter a message to copy: ")
		controller.sim_Alt_Tab()
		controller.sim_typing(message)

	if choice == '5':
		print "**Selected: 5. AES Demo**"
		pwd = vault_encrypt.pwd_gen()
		key = None

		result = "Generated Pass: " + pwd 
		if (not(carrot_encrypt.check_key(pwd))):
		        key = carrot_encrypt.fit_key(pwd)
		else:
		       key = pwd
		#Create AES stream object
		aes = carrot_encrypt.AESModeOfOperationCTR(key)
		ciphertext = aes.encrypt(pwd)

		std_ciphertext = vault_encrypt.encrypt(pwd, pwd)

		aes = carrot_encrypt.AESModeOfOperationCTR(key)
		plain_text = aes.decrypt(ciphertext)
		std_plaintext = vault_encrypt.decrypt(std_ciphertext, pwd)

		result += "\nEncrypted Password (Our AES - CBC): " + ciphertext
		result += "\nEncyted Password (AES - EAX mode): " + std_ciphertext
		result += "\nDecrypted Password (Our AES - CBC): " + plain_text
		result += "\nDecrypted Password (AES - EAX mode): " + std_plaintext
	if choice == '6':
		print "**Selected: 6. Headless Browser Demo**"

		account = raw_input("Facebook(1) or google(2)?: ")

		fb_login_url = "https://facebook.com"
		g_login_url = "https://accounts.google.com"
		username = "secCoolKids@gmail.com"
		fb_password = "holycowbatman123"
		g_password = "supersecret"

		login_url = None
		password = None

		if account == '1':
			login_url = fb_login_url
			password = fb_password
		else:
			login_url = g_login_url
			password = g_password

		auto_pass.auto_change_password(login_url, username, password, "robotsAreCool123")
	# if choice == '7':
	# 	print "**Selected: 7. 2-Factor-Auth Demo"
	# 	code = twofactor.init_2fa()

	# 	user_auth = raw_input("Please enter 2fa code: ")

	# 	if user_auth == code:
	# 		result = "User has been authenticated"
	# 	else:
	# 		result = "Code entered was wrong"

	print_buff()
	print result + "\n\n"

