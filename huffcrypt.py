#------------------------------------------------------------------------------#
# Program Author: Jake Preston                                                 #
#                                                                              #
# Program Description: combines Huffman de/compresson and xor block            #
# de/encryption.                                                               #
#                                                                              #
# Usage: python huffcrypt.py [-e/d] [key] [file]                               #
#------------------------------------------------------------------------------#

import os
import sys
import crypto
import huffman

def error():
    print("Usage: python huffcrypt.py [-e/d] [key] [file]")
    sys.exit(1)

def configure_key(key):
    a = [format(ord(x), 'b') for x in key]
    str = ""
    for i in range(len(a)-1):
        str = bin(int(a[i],2) + int(a[i+1], 2))  
    return str[2:]

def write_to_file(file, data):
    f = open(file,"wb+")
    f.write(data.encode("utf-8"))
    f.close()

if __name__ == "__main__":
    argv = sys.argv
    length = len(argv)
    if length != 4:
        error()
    elif argv[1] != "-e" and argv[1] != "-d":
        error()
    else:
        flag = argv[1]
        key = configure_key(argv[2])
        if os.path.exists(argv[3]):
            with open(argv[3], 'r') as file:
                try:
                    data = file.read()
                except:
                    print("error: failure reading: "+argv[3])
        else:
            print("error: path to file does not exist.")
            sys.exit(1)
        dir_path = os.path.dirname(os.path.realpath(argv[3]))
        h = huffman.Huffman()
        c = crypto.Crypto()
        if(flag == "-e"):
            print("compressing...")
            compressed_data = h.compress(data)
            #print(compressed_data)
            print("encrypting...")
            encrypted_data = c.encrypt(compressed_data, key)
            #print(encrypted_data)
            write_to_file(dir_path+"\e_file",encrypted_data)
        else:
            print("decrypting...")
            decrypted_data = c.decrypt(data, key)
            #print(decrypted_data)
            print("decompressing...")
            decompressed_data = h.decompress(decrypted_data)
