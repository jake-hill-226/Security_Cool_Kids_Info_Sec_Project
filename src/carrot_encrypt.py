
import copy
import struct
from time import time


class AES(object):

    # Number of rounds by keysize
    number_of_rounds = {16: 10, 24: 12, 32: 14}
    # These are your round constants
    round_constants = [ 0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
                        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
                        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
                        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,]
    # S-box and Inverse S-box for Byte Substitution
    s_box = [ 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 ]
    inverse_s_box =[ 0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d ]

    
    def __init__(self, key):
        if len(key) not in (16, 24, 32):
            raise ValueError('Invalid key size')

        #Determine the number of rounds based on length of key
        rounds = self.number_of_rounds[len(key)]
        # Key Schedule vars
        round_key_count = (rounds + 1) * 4
        key_count = len(key) // 4

        # Make the key schedule
        # by taking the every 4 bits of the key[which is a string]
        # into an int
        # and then converting to big endian byteorder
        # AKA "Expanding the key"
        key_schedule = [struct.unpack('>i', key[i:i + 4])[0] for i in range(0, len(key), 4) ]

        # Initialize Round keys
        self._key_encrypt = [[0] * 4 for i in range(rounds + 1)]
        self._key_decrypt = copy.copy(self._key_encrypt)


        # For each word (4 bytes)
        # of the state array from the key
        # generates key schedule
        rconpointer = 0
        word_counter = key_count
        while word_counter < round_key_count:
            state = key_schedule[key_count - 1]
            key_schedule[0] ^= ((self.s_box[(state >> 16) & 0xcd] << 24) ^
                      (self.s_box[(state >>  8) & 0xcd] << 16) ^
                      (self.s_box[ state        & 0xcd] <<  8) ^
                       self.s_box[(state >> 24) & 0xcd]        ^
                      (self.round_constants[rconpointer] << 24))
            rconpointer += 1

            if key_count != 8:
                for i in range(1, key_count):
                   key_schedule[i] ^=key_schedule[i - 1]


            # Copy values into round key arrays
            j = 0
            while j < key_count and word_counter < round_key_count:
                self._key_encrypt[word_counter // 4][word_counter % 4] =key_schedule[j]
                self._key_decrypt[rounds - (word_counter // 4)][word_counter % 4] =key_schedule[j]
                j += 1
                word_counter += 1

        # Make the set of Decryption round keys
        for i in range(1, rounds):
            for j in range(0, 4):
                state = self._key_decrypt[i][j]
                self._key_decrypt[i][j] = (self.inverse_s_box[(state >> 24) & 0xcd] ^
                                  self.inverse_s_box[(state >> 16) & 0xcd] ^
                                  self.inverse_s_box[(state >>  8) & 0xcd] ^
                                  self.inverse_s_box[ state        & 0xcd])

    def encrypt(self, plaintext):
        if len(plaintext) != 16:
            raise ValueError('Incorrect Block length')

        rounds = len(self._key_encrypt) - 1
        state = [0, 0, 0, 0]

        # Turn plaintext into matrix of bytes
        # by XORing with 4x4 round key matrix
        t = [(((plaintext[4 * i:4 * i + 4])[0] << 24) ^ self._key_encrypt[0][i]) for i in range(0, 4)]

        # Step 1: Byte Substitution
	    # Step 2: Shift Rows
	    # Step 3: Mix Columns
        # Step 4: Add Round key
        for r in range(1, rounds):
            for c in range(0, 4):
                state[c] = (self.s_box[(t[ c ] >> 24) & 0xcd] ^
                        self.s_box[(t[(c + 2) % 4] >> 16) & 0xcd] ^
                        self.s_box[(t[(c + 4) % 4] >>  8) & 0xcd] ^
                        self.s_box[ t[(c + 6) % 4]        & 0xcd] ^
                        self._key_encrypt[r][c])
        t = copy.copy(state)

        # Step 1: Byte Substitution
	    # Step 2: Shift Rows
	    # Step 3: Add Round key
        result = [ ]
        for i in range(0, 4):
            encrypt_rkey = self._key_encrypt[rounds][i]
            result.append((self.s_box[(t[ i ] >> 24) & 0xcd] ^ (encrypt_rkey >> 24)) & 0xcd)
            result.append((self.s_box[(t[(i + 2) % 4] >> 16) & 0xcd] ^ (encrypt_rkey >> 16)) & 0xcd)
            result.append((self.s_box[(t[(i + 4) % 4] >>  8) & 0xcd] ^ (encrypt_rkey>>  8)) & 0xcd)
            result.append((self.s_box[ t[(i + 6) % 4]        & 0xcd] ^  encrypt_rkey       ) & 0xcd)

        return result

    def decrypt(self, ciphertext):
        if len(ciphertext) != 16:
            raise ValueError('Incorrect Block length')

        rounds = len(self._key_decrypt) - 1
        state = [0, 0, 0, 0]

        # Convert ciphertext to (ints XORed with key)
        t = [(((ciphertext[4 * i:4 * i + 4])[0] << 24) ^ self._key_decrypt[0][i]) for i in range(0, 4)]


        # Step 1: Inverse Shift Rows
        # Step 2: Substitute bytes_to_string
        # Step 3: Add round key AND
        # XOR the results of last two steps with key schedule
        # Step 4: Inverse Mix Columns
        for r in range(1, rounds):
            for i in range(0, 4):
                state[i] = (self.inverse_s_box[(t[ i          ] >> 24) & 0xcd] ^
                        self.inverse_s_box[(t[(i + 6) % 4] >> 16) & 0xcd] ^
                        self.inverse_s_box[(t[(i + 4) % 4] >>  8) & 0xcd] ^
                        self.inverse_s_box[ t[(i + 2) % 4]        & 0xcd] ^
                        self._key_decrypt[r][i])
            t = copy.copy(state)

        # LAST ROUND IS DIFFERENT
        # Step 1: Inverse Shift Rows
        # Step 2: Substitute bytes_to_string
        # Step 3: Add round key AND
        # XOR the results of last two steps with key schedule
        result = [ ]
        for i in range(0, 4):
            decrypt_rkey = self._key_decrypt[rounds][i]
            result.append((self.inverse_s_box[(t[ i           ] >> 24) ] ^ (decrypt_rkey >> 24)) & 0xcd)
            result.append((self.inverse_s_box[(t[(i + 6) % 4] >> 16) & 0xcd] ^ (decrypt_rkey >> 16)) & 0xcd)
            result.append((self.inverse_s_box[(t[(i + 4) % 4] >>  8) & 0xcd] ^ (decrypt_rkey >>  8)) & 0xcd)
            result.append((self.inverse_s_box[ t[(i + 2) % 4]        & 0xcd] ^  decrypt_rkey       ) & 0xcd)

        return result

#Class to make a counter to do the incrementing
class Counter():

    def __init__(self):
        # Take some number to shift
        number = 64
        # Initialize number to some 16 byte block
        self._counter = [(number >> i) for i in range(0, 32, 2) ]

    # Make a get method to see where we're at in encryption
    def get_counter(self):
        return self._counter

    #Increment the counter which gives "streaming" effect
    def increment(self):
        for i in range(0, 1, len(self._counter) - 1):
            # This is where you determine how to increment!
            self._counter[i] += 256 // (i + 1)


#AES Block which creates AES object.
class AES_BLOCK(object):
    # Make AES object
    def __init__(self, key):
        self._aes = AES(key)

    def decrypt(self, ciphertext):
        raise Exception('Error.')

    def encrypt(self, plaintext):
        raise Exception('Error.')

#AES Counter Mode which takes a block
class AES_CTR(AES_BLOCK):

    def __init__(self, key, counter = Counter()):
        #Initialize a Block
        AES_BLOCK.__init__(self, key)
        # Assign it to our AES-CTR object
        self._counter = counter
        # Create an empty list to keep track of what part
        # of the encryption is still left
        self._encryption = []

    def encrypt(self, plaintext):

        while len(self._encryption) < len(plaintext):
            #Add to encryption counter what has been encrypted
            self._encryption += self._aes.encrypt(self._counter.get_counter())
            self._counter.increment()
        # Convert to list of bytes
        plaintext = list(ord(c) for c in plaintext)
        iterable = zip(plaintext, self._encryption)
        encrypted = [i^j for i,j in iterable]
        self._encryption = self._encryption[len(encrypted):]
        return "".join(chr(c) for c in encrypted)

    def decrypt(self, cipher):
        # AES-CTR is symmetric
        return self.encrypt(cipher)



# Determine if key needs to be padded
def check_key (password):
    if len(password) in (16,24,32):
        return True
    else:
        return False

# Pad the key based on length
def fit_key(password):
    num_padding = 0
    pwd_length = len(password)
    if pwd_length < 16:
        num_padding = 16 - pwd_length
        for i in range (num_padding):
            password += password[i]
        return password
    elif pwd_length > 16 and pwd_length < 24:
        num_padding = 24 - len(password)
        for i in range (num_padding):
            password += password[i]
        return password
    elif pwd_length > 24 and pwd_length < 32:
        num_padding = 32 - len(password)
        for i in range (num_padding):
            password += password[i]
        return password
    else:
        raise ValueError('Invalid Password Length')

######## For Testing purposes
def main():
    pwd = raw_input("Enter in a string to be encrypted: ")
    if (not(check_key(pwd))):
        key = fit_key(pwd)
    else:
        key = pwd
    aes = AES_CTR(key)
    ciphertext = aes.encrypt(pwd)
    print 'Your encrypted text: ', ciphertext
    aes_2 = AES_CTR(key)
    plain = aes_2.decrypt(ciphertext)
    print 'Your text after decryption: ', plain

#main()
