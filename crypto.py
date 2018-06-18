#------------------------------------------------------------------------------#
# Crypto class                                                                 #
#   simple xor block cipher                                                    #
#------------------------------------------------------------------------------#

class Crypto:

    # converts byte-string to array of byte blocks
    # bytes are xor-ed with key
    def encrypt(self, str, key):
        #print(str)
        blocks = self.str_to_byte_blocks(str)
        #print(blocks)
        chars = "".join(chr(byte ^ int(key,2)) for byte in blocks)
        #print(chars)
        return chars

    # each character is xor-ed with the key
    def decrypt(self, str, key):
        blocks = [bin(int(key,2) ^ ord(char))[2:].zfill(8) for char in str]
        #print(blocks)
        str = self.byte_blocks_to_str(blocks)
        #print(str)
        return str

    def str_to_byte_blocks(self, str):
        return [int(str[i:i+8],2) for i in range(0, len(str), 8)]

    def byte_blocks_to_str(self, bb):
        return "".join(str(b) for b in bb)
