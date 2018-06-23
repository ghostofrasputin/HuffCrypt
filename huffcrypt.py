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
import huffman

def error():
    print("Usage: python huffcrypt.py [-e/d] [key] [file]")
    sys.exit(1)

# start here
def configure_key(key):
    key = ['{0:08b}'.format(ord(x), 'b') for x in key]
    s = '{0:08b}'.format(sum(int(x, 2) for x in key))[0:8]
    # debug
    #print(s)  
    return int(s,2)

def encrypt(key, file, head, data):
    f = open(file,"wb")
    byte_array = bytearray()
    # add partition after header
    head += "  "
    #print(head)
    # convert header into bit string
    head = ''.join('{0:08b}'.format(ord(c), 'b') for c in head)
    # encrypt header huffman data first
    for i in range(0, len(head), 8):
        byte_array.append(int(head[i:i + 8], 2) ^ key)
    # encrypt file data
    for i in range(0, len(data), 8):
        byte_array.append(int(data[i:i + 8], 2) ^ key)
    #print(byte_array[0])  
    f.write(byte_array)
    f.close()

def decrypt(key, data):
    str = ""
    flag = False
    start = 0
    # decrypt head into characters
    for i in range(0,len(data)):
        str += chr(data[i] ^ key)
        if i > 0:
            if chr(data[i-1] ^ key) == " " and chr(data[i] ^ key) == " ":
                flag = True
                start = i+1
                break
    # decrypt data into bit strings
    for i in range(start, len(data)):
        bit_string = '{0:08b}'.format(data[i] ^ key,'b')
        str += bit_string                   
    return str  
        
def write_to_file(file, data):
    f = open(file,"w+")
    f.write(data)
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
            mode = "r" if flag == "-e" else "rb"
            with open(argv[3], mode) as file:
                try:
                    data = file.read()
                except:
                    print("Error: failure reading: "+argv[3])
                    sys.exit(1)
        else:
            print("Error: path to file does not exist.")
            sys.exit(1)
        dir_path = os.path.dirname(os.path.realpath(argv[3]))
        h = huffman.Huffman()
        if(flag == "-e"):
            print("Compressing...")
            header, compressed_data = h.compress(data)
            print("Encrypting...")
            encrypt(key, dir_path+"\e_file", header, compressed_data)
            print("Done.")
        else:
            print("Decrypting...")
            decrypted_data = decrypt(key, list(data))
            print("Decompressing...")
            write_to_file(dir_path+"\d_file", h.decompress(decrypted_data))
            print("Done.")


