# importing all the necessary libaries
from Crypto.Cipher import DES3
from hashlib import md5
import time
import collections
import math
encr=""

#  function to xor 2 given byte strings
def byte_des(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

# function to calculate the entropy of the data
def entropy(data):
    e = 0
    counter = collections.Counter(data)
    l = len(data)
    for count in counter.values():
        p_x = count / l
        e += - p_x * math.log2(p_x)
    print(e)

# function to calculate the mean square error between decrypted and original data
def mse(m2,m1):
    n=len(m2)
    summation=0
    MSE=1
    for i in range (0,n):
        difference = m2[i] - m1[i]
        squared_difference = difference**2
        summation = summation + squared_difference
    MSE = summation/n
    print('MSE between decrypted and original data:',MSE)
      
# switching over encryption,decryption and exit options
while True:
    print("choose the following operation to be performed:\n\t1-Encrypt\n\t2-Decrypt\n\t3-Close")
    operation=input("your choice:")
    if operation == "3":
        print("success")
        break
    file_path=input("file path:")

    # getting key input from the user and hashing it and adjusting key parity and declaration of 3des
    key=input("TDES key:")
    key_hash= md5(key.encode('ascii')).digest()
    tdes_key=DES3.adjust_key_parity(key_hash)
    cipher = DES3.new(tdes_key,DES3.MODE_EAX,nonce=b'0')
    new_file_byte=''

    # opening file to carry out operations
    with open(file_path,"rb") as input_file:
        file_bytes = input_file.read()
        
        # encryption operation
        if operation=="1":
            encr= byte_des(tdes_key,file_bytes)
            beg=time.time()
            new_file_byte = cipher.encrypt(file_bytes)
            encl=new_file_byte
            end=time.time()
            with open(file_path,'wb') as input_file:
                input_file.write(encl)
            print("total time for encryption:",end-beg)
            print('entropy of encrypted data is')
            entropy(new_file_byte)
            encr=file_bytes
        
        # decryption operation
        elif operation=='2':
            beg=time.time()
            new_file_byte = cipher.decrypt(file_bytes)
            end=time.time()
            print("total time for decryption:",end-beg)
            mse(encr,new_file_byte)
        else:
            print("enter valid option")
    # saving the carried out operation to a file
    with open(file_path,'wb') as output_file:
        output_file.write(new_file_byte)