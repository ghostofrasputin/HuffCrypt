#------------------------------------------------------------------------------#
# Program Author: Jake Preston                                                 #
#                                                                              #
# Program Description: combines Huffman de/compresson and xor block            #
# de/encryption.                                                               #
#                                                                              #
#------------------------------------------------------------------------------#

import os
import sys
import huffman
from tkinter import *
from tkinter.filedialog import askopenfilename

class HuffCrypt:
    def __init__(self):
        
        self.key = ""
        self.data = None
        self.h = huffman.Huffman()
        
        self.root = Tk()
        self.root.title("HuffCrypt")
        self.root.geometry("250x250")
        self.root.resizable(0, 0)
        
        # File Select Button
        rf_button = Button(self.root, text="Select File")
        rf_button.configure(command=self.load_file)
        rf_button.place(x=0, y=0, width=122)
        
        # Enter Password Label
        ep_label = Label(self.root, text="Enter Password:")
        ep_label.place(x=125, y=0)
        
        # Password Text Box
        self.password_box = Entry(self.root, show="\u2022", bd=3)
        self.password_box.bind('<Return>', self.get_password)
        self.password_box.place(x=125, y=25, width=120)
        
        # Compression / Encyption Button
        ce_button = Button(self.root, text="Encrypt/Compress")
        ce_button.bind("<Button-1>", self.compress_encrypt)
        ce_button.place(x=0, y=25, width=122)
        
        # Decompression / Decryption Button
        dd_button = Button(self.root, text="Decrypt/Decompress")
        dd_button.bind("<Button-1>", self.decrypt_decompress)
        dd_button.place(x=0, y=50, width=122)
        
        # Console Text Box
        self.tb = Text(self.root, bg="black",fg="#00ff37", font=("Helvetica", 8))
        self.tb.place(x=0, y=75, width=250, height=175)
        
    def run(self):
        self.root.mainloop()
    
    def get_password(self, event):
        self.key = self.configure_key(self.password_box.get())
        self.password_box.delete(0, 'end')
    
    def println(self, text):
        self.tb.insert("1.0",text+"\n")
        
    def load_file(self):
        self.fname = askopenfilename()
        ext = os.path.splitext(self.fname)[1]
        self.mode = "r" if ext != ".bin" else "rb"
        with open(self.fname, self.mode) as file:
            try:
                self.data = file.read()
                self.dir_path = os.path.dirname(os.path.realpath(self.fname))
            except:
                print("Error: failure reading: "+self.fname)
                sys.exit(1)
        
        self.tb.insert("1.0","Read in file: "+self.fname+"\n")
    
    def compress_encrypt(self, event):
        if self.mode != "r":
            self.println("This is a binary file,")
            return
        if self.key == "":
            self.println("No Key Given.")
            return    
        self.println("Compressing...")
        header, compressed_data = self.h.compress(self.data)
        self.println("Encrypting...")
        self.encrypt(self.key, self.dir_path+"\e_file.bin", header, compressed_data)
        self.println("Done.")
    
    def decrypt_decompress(self, event):
        if self.mode != "rb":
            self.println("This isn't a binary file.")
            return
        if self.key == "":
            self.println("No Key Given.")
            return      
        self.println("Decrypting...")
        decrypted_data = self.decrypt(self.key, list(self.data))
        self.println("Decompressing...")
        self.write_to_file(self.dir_path+"\d_file", self.h.decompress(decrypted_data))
        self.println("Done.")
    
    def configure_key(self, key):
        key = ['{0:08b}'.format(ord(x), 'b') for x in key]
        s = '{0:08b}'.format(sum(int(x, 2) for x in key))[0:8]
        # debug
        #print(s)  
        return int(s,2)
    
    def encrypt(self, key, file, head, data):
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
    
    def decrypt(self, key, data):
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
            
    def write_to_file(self, file, data):
        f = open(file,"w+")
        f.write(data)
        f.close()        
        
app = HuffCrypt()
app.run()        

