#!usr/bin/python

from Crypto.Cipher import AES
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
