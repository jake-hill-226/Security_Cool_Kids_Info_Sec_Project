from twilio.rest import Client
import smtplib
import  random
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

selection = 'default'
branch = True
code = str(random.randrange(100000,999999))
while True:
    selection = str(raw_input("Enter either \'phone\' or \'mail\' for your authentication: "))
    if (selection == 'phone' or selection == 'mail'):
        if (selection == 'mail'):
            branch = False
        break
    else:
        print  ("Error, Please enter again! ")


if branch:
    # twilio SMS Authentication
    account_sid = "ACaaa09e40e7f439226b94d26f61ea98ed"
    # Your Auth Token from twilio.com/console
    auth_token  = "28ee5bf3dad72ebe57c058e454b2e357"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+16148860860",
        from_="+17402174583 ",
        body="From Corporal Carrot Password Manager(Phone) \nThis is your security verification code: " + code)

    print(message.sid)
else:
    # gmail smtp authentication
    msg = MIMEMultipart()
    msg['From'] = 'wrnmmpjobsearch@gmail.com'
    msg['To'] = 'chen.4207@osu.edu'
    msg['Subject'] = 'Security Verification'
    message = 'From Corporal Carrot Password Manager(Web)\nThis is your verification code: ' + code
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login('wrnmmpjobsearch@gmail.com', '19950103Cf')

    mailserver.sendmail('wrnmmpjobsearch@gmail.com','chen.4207@osu.edu',msg.as_string())

    mailserver.quit()