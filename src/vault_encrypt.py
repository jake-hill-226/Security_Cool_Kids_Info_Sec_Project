#!usr/bin/python

from Crypto.Cipher import AES
from Crypto.Hash import SHA512
import random
import CarrotDB


chars = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
length = 4

def encrypt(vault_pwd, usr_pwd):
    while len(usr_pwd) < 32:
        usr_pwd = usr_pwd + usr_pwd

    obj = AES.new(usr_pwd[:32], AES.MODE_EAX)
    message = vault_pwd
    ciphertext = obj.nonce +  obj.encrypt(message)
    return ciphertext


def decrypt(cipheredpwd, usr_pwd):
    while (len(usr_pwd) < 32):
        usr_pwd = usr_pwd + usr_pwd

    obj2 = AES.new(usr_pwd[:32], AES.MODE_EAX, cipheredpwd[:16])
    return(obj2.decrypt(cipheredpwd[16:]))


#Generate arbitrary password
def pwd_gen():
    pwd = ''
    for x in range(0,length):
        for x in range(0,length):
            pwd += random.choice(chars)
        pwd += '-'
    return pwd

def auth_user(user_name, password):
    CarrotDB.connect()

    user = CarrotDB.User()
    user.username = user_name

    result = False

    if user.fetch():
        db_pass_hash = SHA512.new(data=user.password)
        test_pass_hash = SHA512.new(data=password)

        if db_pass_hash.hexdigest() == test_pass_hash.hexdigest():
            result = True

    CarrotDB.disconnect()
    return result