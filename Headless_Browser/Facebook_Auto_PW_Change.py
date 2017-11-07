from splinter import Browser
from selenium import webdriver

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



raw_input("<To end session press enter>")
browser.quit()

#browser.find_by_css("._54nh")