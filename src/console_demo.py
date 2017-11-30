"""
###############################################
		Console based features demo

Description: This simple demo illustrates the features we were able to
			 implement but not fully integrate into the CarrotKey GUI

Contributors: Jake Hill 
			  Anastasia Bourlas
			  Phaedra Paul
			  Dikai Xiong
			  Fan Chen

Last Modified: 11/22/17
###############################################
"""

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
	4. Copy password into previous window
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
		result = "New user added: " + username + ", " + password + ", " + auth_options +", " + email + ", " + phone
	if choice == '2':
		print "**Selected: 2. Create new pass**"
		username = raw_input("Enter Username: ")
		password = raw_input("Enter Password: ")
		url = raw_input("Enter URL of login page: ")
		details = raw_input("Enter short description of account (optional): ")

		controller.store_new_pass(username, url, password, details)
		result = "New pass added: " + username + ", " + password + ", " + url + ", " + details

	if choice == '3':
		print "**Selected: 3. Print passes for user**"
		username = raw_input("Enter Username: ")
		password = raw_input("Enter Password: ")

		pass_list = controller.search_vault(username)

		for passw in pass_list:
			passw.password = controller.retrieve_pass(username, passw.url, password)
			print passw.password.encode("hex")

		result = ""

		if(len(pass_list) > 0):
			for pwd in pass_list:
				details = ""
				if pwd.details:
					details = pwd.details
				result = result + "ID: " + str(pwd.entry_id) + "\nusername: " + pwd.username + "\nurl: " + pwd.url + "\ndetails: " + details + "\npassword: " + pwd.password + "\n"
		else:
			result = "No passwords stored for " + username

	if choice == '4':
		print "**Selected: 4. Copy password into previous window**"
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
		aes = carrot_encrypt.AES_CTR(key)
		ciphertext = aes.encrypt(pwd)
		std_ciphertext = vault_encrypt.encrypt(pwd, pwd)

		aes = carrot_encrypt.AES_CTR(key)
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

		print "Selection results: url " + login_url 
		auto_pass.auto_change_password(login_url, username, password, "robotsAreCool123")

	print_buff()
	print result + "\n\n"


