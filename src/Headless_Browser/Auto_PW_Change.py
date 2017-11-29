"""
#########################################################
					Auto_PW_Change
Description: A module used to change the password automatically via
			 a headless browser

Contributors: Jake Hill
Last Modified: 11/28/17

#########################################################
"""


from splinter import Browser
from selenium import webdriver
import time


"""
# Initializes an instance of a headless chrome browser starting at "url"

# url: (string) The url for which to initialize the browser session for

# return val: (Browser) A splinter browser object
"""
def init_browser(url):
	try:
		# Disable browser notifications for unimpeeded web browsing	
		disable_notifs = {"profile.default_content_setting_values.notifications" : 2}
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_experimental_option("prefs", disable_notifs)

		# Use for testing with GUI browser
		browser = Browser("chrome", options=chrome_options)
		# browser = Browser("chrome", options=chrome_options, headless=true)

		browser.visit(url)
	except:
		print "Error: Failed to initialize browser\n"

		if browser:
			browser.quit()
	return browser


"""
# Changes the password for the given user credentials on Facebook

# acct_username: (string) The user's facebook username
# acct_pasword: (string) The user's facebook password
# new_pass: (string) The new password to replace the existing one
"""
def change_facebook_password(acct_username, acct_password, new_pass):
	try:
		browser = init_browser("https://Facebook.com")
	except:
		print "Error: Failure to init browser for facebook.com\n"
		return

	# Initial login
	email_form = browser.find_by_id("email")

	pass_form = browser.find_by_id("pass")

	login_btn = browser.find_by_value("Log In")

	# Submit login form
	try:
		email_form.fill(acct_username)
		pass_form.fill(acct_password)
		login_btn.click()
	except:
		print "Error: failed to submit login form"
		browser.quit()
		return

	# Navigate to settings -> Security and Login
	browser.visit("https://www.facebook.com/settings")
	browser.visit("https://www.facebook.com/settings?tab=security")

	# Unhide change password field
	edit_pw_btn = browser.find_by_text("Change password")
	edit_pw_btn.click()

	try:
		# OldPass
		browser.find_by_id("password_old").fill(acct_password)

		#NewPass
		browser.find_by_id("password_new").fill(new_pass)
		browser.find_by_id("password_confirm").fill(new_pass)

		# Uncomment to change password
		#save_change_btn = browser.find_by_value("Save Changes").first.click()
	except:
		print "Error: Failed to submit change password form"
		browser.quit()
		return

	browser.quit()
	print "Password Successfully Changed for Facebook"

"""
# Changes the password for the given user credentials on Google

# acct_username: (string) The user's Google username
# acct_pasword: (string) The user's Google password
# new_pass: (string) The new password to replace the existing one
"""
def change_google_password(acct_username, acct_password, new_pass):
	browser = init_browser("https://accounts.google.com")

	# Submit Username and Password for Login
	try:
		browser.find_by_id("identifierId").fill(acct_username)
		browser.find_by_tag("span").find_by_text("Next").first.click()
	except:
		print "Error: failed to submit username"
	
	try:
		time.sleep(0.5)
		browser.find_by_name("password").first.fill(acct_password)
		browser.find_by_tag("span").find_by_text("Next").first.click()
	except:
		print "Error: failed to submit password"

	# Navigate to new password page
	browser.visit("https://myaccount.google.com/security?pli=1#signin")
	browser.visit("https://myaccount.google.com/signinoptions/password")

	# Authenticate to submit new password to google
	try:
		time.sleep(0.5)
		browser.find_by_name("password").first.fill(acct_password)
		browser.find_by_tag("span").find_by_text("Next").first.click()
	except:
		print "Error: failed to submit password"

	# Submit new password to google
	try:
		time.sleep(0.5)
		browser.find_by_name("password").first.fill(new_pass)
		browser.find_by_name("confirmation_password").first.fill(new_pass)

		# Uncomment to actually change password
		#browser.find_by_tag("span").find_by_text("Change password").first.click()
	except:
		print "Error: failed to submit new password"

	raw_input("<press enter to close session>")
	browser.quit()

"""
# Changes the password for the given user credentials on a select list
  of supported websites

# Login_url: (string) The url for the login page of a given website
# acct_username: (string) The user's website username
# acct_pasword: (string) The user's website password
# new_pass: (string) The new password to replace the existing one
"""
def auto_change_password(login_url, acct_username, acct_password, new_pass):
	url_file = open("supported_websites.txt", "r")

	supported_list = []

	for line in url_file:
		line.replace("\n", "");
		supported_list.append(line)

	url_file.close()

	if login_url not in supported_list:
		print "Sorry this website is unsupported\n"
		return

	if login_url == "https://facebook.com":
		change_facebook_password(acct_username, acct_password, new_pass)
	elif login_url == "https://accounts.google.com":
		change_google_password(acct_username, acct_password, new_pass)

		
# A section used for testing this module as a standalone script

if __name__=="__main__":

	fb_login_url = "https://facebook.com"
	g_login_url = "https://accounts.google.com"
	username = "secCoolKids@gmail.com"
	fb_password = "holycowbatman123"
	g_password = "supersecret"

	change_google_password(username, g_password, "testing")
