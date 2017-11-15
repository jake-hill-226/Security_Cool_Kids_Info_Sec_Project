#test bed for functions

# from Crypto.Cipher import AES

# key = b'12345678901234567890123456789012'
# cipher = AES.new(key, AES.MODE_EAX)

# nonce = cipher.nonce

# print nonce

# message = b"supersecret message!!"

# ciphertext = nonce + cipher.encrypt("supersecret message!!")


# print ciphertext

# dec_nonce = ciphertext[:16]

# print dec_nonce

# rev_cipher = AES.new(key, AES.MODE_EAX, dec_nonce)

# plaintext = rev_cipher.decrypt(ciphertext[16:])

# print plaintext

##############################################################

import vault_encrypt

password = "secret"

new_pass = vault_encrypt.pwd_gen()

print "New Pass: " + new_pass

cipher_pass = vault_encrypt.encrypt(new_pass, password)

print "Cipher Pass: " + cipher_pass

plain_pass = vault_encrypt.decrypt(cipher_pass, password)

print "Plain Pass: " + plain_pass

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