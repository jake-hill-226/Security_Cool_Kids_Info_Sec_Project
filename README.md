# Security_Cool_Kids_Info_Sec_Project
### CSE 4471 Security application project and home of the Security Cool Kids

#### CarrotKey

CarrotKey is a python based password vault that persists on the user's local disk.
In this application, users can access their account passwords for various sites from
a local database where they are stored encrypted using AES CTR mode. The passwords
are only decrypted when the user has authenticated themselves. Users also have the ability
to authenticate via 2-factor-authentication via text message or email.

 Users are also presented with the option to securely input their passwords into a login prompt using our keyboard
emulation function which simiulates the user alt+tab into the previouse window and type the corresponding password.
To make matters more simple for our users we currently have in beta an auto-password-changer engine which currently
works for their Google and Facebook accounts. 


#### Installation and Requirements

##### Requirements
- Python=2.7
- pip>=9.0.1
- Chrome webdriver (optional if you don't want to participate in the auto-pass-changer beta)
	- please vist https://sites.google.com/a/chromium.org/chromedriver/downloads
	  and download the appropriate webdriver for your OS.
	  Then add the webdriver download into you environment PATH variable using the
	  respective method of you OS.

##### Installation
- In a terminal navigate to the root project directory
- In your terminal enter
	$ pip -r requirements.txt
- Accept all packages to be installed


#### Running The Application

##### CarrotKey GUI (WIP)

##### From the command-line
- from your terminal navigate to the project src folder
- enter the command
	$ python login_gui.py

##### From a double-click
- from your terminal navigate to the project src folder
- enter the command chmod u=x login_gui.py
- Now open you file explorer and find the login_gui.py file
  and double-click on the script
- Note you may also create a shortcut to this file if you would like

#### GitHub URL
https://github.com/jake-hill-226/Security_Cool_Kids_Info_Sec_Project

## Contributors
- Anastasia Bourlas
- Jake Hill
- Phaedra Paul
- Dikai Xiong
- Fan Chen
