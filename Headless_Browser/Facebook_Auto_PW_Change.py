from splinter import Browser
from selenium import webdriver

def change_facebook_pass(acct_username, acct_password, new_pass):
	# Disable browser notifications for unimpeeded web browsing
	disable_notifs = {"profile.default_content_setting_values.notifications" : 2}
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_experimental_option("prefs", disable_notifs)

	browser = Browser("chrome", options=chrome_options)

	site = raw_input("Enter the site you would like to navigate to: https://")

	if site == "":
		site = "https://www.google.com"
	else:
		site = "https://" + site

	browser.visit(site)


	# Initial login
	email_form = browser.find_by_id("email")

	pass_form = browser.find_by_id("pass")

	login_btn = browser.find_by_value("Log In")

	email = raw_input("Enter FB Email: ")
	password = raw_input("Enter FB Password: ")

	# Submit login form
	email_form.fill(email)
	pass_form.fill(password)
	login_btn.click()

	# Navigate to settings -> Security and Login
	browser.visit("https://www.facebook.com/settings")
	browser.visit("https://www.facebook.com/settings?tab=security")

	# Unhide change password field
	edit_pw_btn = browser.find_by_text("Change password")
	edit_pw_btn.click()

	# OldPass
	browser.find_by_id("password_old").fill("changeme123")

	#NewPass
	new_pass = "holycowbatman123"
	browser.find_by_id("password_new").fill(new_pass)
	browser.find_by_id("password_confirm").fill(new_pass)

	save_change_btn = browser.find_by_value("Save Changes").first.click()

	browser.quit()
	print "Password Successfully Changed for Facebook"

login_url = "https://facebook.com"
username = "secCoolKids@gmail.com"
password = "holycowbatman123"


def auto_change_password(login_url, acct_username, acct_password, new_pass):
	url_file = open("supported_websites.txt", "r")

	supported_list = []

	for line in url_file:
		line.replace("\n", "");
		supported_list.append(line)

	url_file.close()

	if login_url in supported_list:
		print "We found it!\n"
	else:
		print "Sorry this website is unsupported\n"

auto_change_password(login_url, username, password, "robotsAreCool123")