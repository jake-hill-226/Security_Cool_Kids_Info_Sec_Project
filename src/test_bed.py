#test bed for functions

# from Crypto.Cipher import AES

# key = b'12345678901234567890123456789012'
# cipher = AES.new(key, AES.MODE_EAX)

# nonce = cipher.nonce

# print nonce

# message = b"didyousaywaffles"

# ciphertext = nonce + cipher.encrypt(message)


# print ciphertext

# dec_nonce = ciphertext[:16]

# print dec_nonce

# rev_cipher = AES.new(key, AES.MODE_EAX, dec_nonce)

# plaintext = rev_cipher.decrypt(ciphertext[16:])

# print plaintext

##############################################################

# import vault_encrypt
# import binascii

# password = "secret"

# new_pass = vault_encrypt.pwd_gen()

# print "New Pass: " + new_pass

# cipher_pass = vault_encrypt.encrypt(new_pass, password)

# print "Cipher Pass: " + cipher_pass
# print "Cipher Pass Hex: " + binascii.unhexlify(binascii.hexlify(cipher_pass))

# plain_pass = vault_encrypt.decrypt(cipher_pass, password)

# print "Plain Pass: " + plain_pass

##############################################################

# import controller

# controller.sim_Alt_Tab()
# controller.sim_typing("this is a test")

##############################################################

# import controller

# username = "jake"
# password = "temp"

# pass_list = controller.search_vault(username)

# for p in pass_list:
# 	p.display()

# import binascii

# hexi = (b"hello world").encode("hex")
# print hexi

# message = binascii.unhexlify(hexi)
# print message


import CarrotDB as db

db.connect()

usr = db.User()
usr.username = "john"

usr.fetch()

passwords = usr.getVault()

for psw in passwords:
	psw.delete()

db.disconnect()

import carrot_encrypt
import base64

password = "test"
message = "Hello world"
key = ""

if (not(carrot_encrypt.check_key(password))):
	key = carrot_encrypt.fit_key(password)

else:
	key = password
#Create AES stream object
aes = carrot_encrypt.AES_CTR(key)
vault_pass = aes.encrypt(message)
print vault_pass
print type(vault_pass)

b64_pass = base64.standard_b64encode(vault_pass)
print "Base64 vault_pass: " + b64_pass
print "Base64 vault_pass decoded: " + base64.standard_b64decode(b64_pass)

hex_pass = b64_pass.encode("hex")

print "Hex b64_pass: " +  hex_pass

hex_pass = hex_pass.decode("hex")
print "Hex b64_pass decoded: " +  hex_pass

b64_pass = base64.standard_b64decode(hex_pass)
print "b64_pass decoded from hex_pass decoded to base64: " +  b64_pass

aes2 = carrot_encrypt.AES_CTR(key)
vault_pass = aes2.decrypt(vault_pass)

print vault_pass