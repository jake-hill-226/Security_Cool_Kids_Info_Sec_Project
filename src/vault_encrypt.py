#!usr/bin/python
# Library version of encryption modules
# Used as a backup
# This also provides an auto generation features that carrot_encrypt 
# does not contain
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
import random
import CarrotDB
import smtplib


chars = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
length = 4

# Encrypt module
# @vault_pwd: Master password to open vault
# @usr_pwd: Password within the vault to encrypt
# Returns: encrypted string
def encrypt(vault_pwd, usr_pwd):
    while len(usr_pwd) < 32:
        usr_pwd = usr_pwd + usr_pwd
    obj = AES.new(usr_pwd[:32], AES.MODE_EAX)
    message = vault_pwd
    ciphertext = obj.nonce +  obj.encrypt(message)
    return ciphertext

# Decrypt module
# @cipheredpwd: Encrypted string
# @usr_pwd: Password within the vault to encrypt
# Returns: decrypted string
def decrypt(cipheredpwd, usr_pwd):
    while (len(usr_pwd) < 32):
        usr_pwd = usr_pwd + usr_pwd

    obj2 = AES.new(usr_pwd[:32], AES.MODE_EAX, bytes(cipheredpwd[:16]))
    return(obj2.decrypt(cipheredpwd[16:]))

# Generate arbitrary password
# @vault_pwd: Master password to open vault
# @usr_pwd: Password within the vault to encrypt
# Returns: string of arbitrary characters
def pwd_gen():
    pwd = ''
    for x in range(0,length):
        for x in range(0,length):
            pwd += random.choice(chars)
        pwd += '-'
    return pwd
# Authoentication module
# @user_name:String
# @password: String
# Returns: boolean of successful authentication
def auth_user(user_name, password):
    CarrotDB.connect()

    user = CarrotDB.User()
    user.username = user_name

    result = False

    if user.fetch():
        db_pass_hash = user.password
        test_pass_hash = SHA512.new(data=password)

        if db_pass_hash == test_pass_hash.hexdigest():
            result = True

    CarrotDB.disconnect()
    return result
# Hash module
# @password: string
# Returns: sha512 hash for @psasword
def hash_user_pwd(password):
    return SHA512.new(data=password).hexdigest()

