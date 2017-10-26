#!usr/bin/python

from Crypto.Cipher import AES
import random

chars = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
len = 4

def encrypt(pwd){
    obj = AES.new(pwd, AES.MODE_CBC, 'This is an IV456')
    message = pwd
    ciphertext = obj.encrypt(message)
    return ciphertext
}

def decrypt(cipheredpwd, pwd){
    obj2 = AES.new(pwd, AES.MODE_CBC, 'This is an IV456')
    return(obj2.decrypt(cipheredpwd))
}
#Generate arbitrary password
def pwd_gen(){
    pwd = ''
    for x in range(0,len):
        for x in range(0,len):
            pwd += random.choice(chars)
        pwd += '-'
    encrypt(pwd)

}
