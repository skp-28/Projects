# importing all neccessary libraries
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
import time
import collections
import math

# definig encryption class
class Encryptor:

    #  initialisation of keys
    def __init__(self,key):
        self.key=key
        self.enc1=""

    # function to pad the message for block size
    def pad(self,s):
        return s+b'\0' *(AES.block_size -len(s)%AES.block_size)

    # function to return xor of provided values
    def byte_aes(self,ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

    # function to calculate the entropy of the encrypted data
    def entropy(self,data):
        e = 0
        counter = collections.Counter(data)
        l = len(data)
        for count in counter.values():
            p_x = count / l
            e += - p_x * math.log2(p_x)
        print('entropy of encrypted data is')
        print(e)

    # function to calculate the mean square error between decrypted and original data
    def mes(self,data):
        n=len(self.enc1)
        summation=0
        MSE=1
        for i in range (0,n):
            difference = self.enc1[i] - data[i]
            squared_difference = difference**2
            summation = summation + squared_difference
        MSE = summation/n
        print('MSE between decrypted and original data')
        print(MSE)       
   
   # declaring the aes encryption function 
    def encrypt1(self,message,key,key_size=256):
        self.plaintext=message
        message=self.pad(message)
        iv=Random.new().read(AES.block_size)
        cipher=AES.new(key,AES.MODE_CBC,iv)
        return iv+cipher.encrypt(message)

    # function to encrypt files
    def encrypt_file(self,file_name):
        
        with open(file_name,'rb')as fo:
            self.plaintext=fo.read()
        beg=time.time()
        enc=self.encrypt1(self.plaintext,self.key)
        end=time.time()
        self.enc1= self.byte_aes(self.key,self.plaintext)
        print("total time for encryption:",end-beg)
        with open(file_name,'wb') as fo:
            fo.write(enc)
        self.entropy(enc)

    # declaring aes decrypt function
    def decrypt1(self,cipherText, key):
        iv=cipherText[:AES.block_size]
        cipher=AES.new(key,AES.MODE_CBC,iv)
        self.plaintext=cipher.decrypt(cipherText[AES.block_size:])
        return self.plaintext.rstrip(b'\0')
    
    # function to decrypt the file
    def decrypt_file(self,file_name):
        with open(file_name,'rb')as fo:
            cipherText=fo.read()
        beg=time.time()
        dec=self.decrypt1(cipherText,self.key)
        end=time.time()
        print("total time for decryption:",end-beg)
        with open(file_name,'wb')as fo:
            fo.write(dec)
        self.mes(dec)

# giving a predefined key and calling the encryptor class
key=b'\0'*32
enc=Encryptor(key)

# switching over choices encryption,decryption and exitting the process
while True:
    
    choice= int(input('1. press 1 to encrpt_file \n 2. to decrypt_file\n 3.to exit:'))
    if choice==1:
        enc.encrypt_file(str(input('enter name of file to encrypt:')))
        
    elif choice==2:
        enc.decrypt_file(str(input("enter the name of file to decrypt:")))
               
    elif choice==3:
        break
    else:
        print('please select a valid option')

print('successful')

