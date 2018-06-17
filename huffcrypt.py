#------------------------------------------------------------------------------#
# Program Author: Jake Preston                                                 #
#                                                                              #
# Program Description: combines Huffman de/compresson and xor block            #
# de/encryption.                                                               #
#------------------------------------------------------------------------------#

import sys
import crypto
import huffman

def error():
    print("Usage: huffcrypt.py [-e/d] [key] [file]")
    sys.exit(1)

if __name__ == "__main__":
    argv = sys.argv
    length = len(argv)
    if length != 4:
        error()
    elif argv[1] != "-e" and argv[1] != "-d":
        error()
    else:
        flag = argv[1]
        key = argv[2]
        h = huffman.Huffman()
        c = crypto.Crypto()
        if(flag == "-e"):
            print("compressing...")
            print("encrypting...")
        else:
            str = "Once the files are lost, the pour soul is too."
            print(str)
            str = h.compress(str)
            print(str)
            cr = c.encrypt(str,key)
            print(cr)
            print("decrypting...")
            d_str = c.decrypt(cr,key)
            print(d_str)
            d_str = h.decompress(d_str)
            print(d_str)
            print("decompressing...")
