#------------------------------------------------------------------------------#
# Huffman class                                                                #
#   huffman compression algorithm                                              #
#------------------------------------------------------------------------------#

import heapq

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return "(char: "+self.char+" freq: "+str(self.freq)+")"

class Huffman:

    def __init__(self):
        self.root = None

    def encode(self, root, str, hcode):
        if root == None:
            return
        if root.left == None and root.right == None:
            hcode[root.char] = str
        self.encode(root.left, str + '0', hcode)
        self.encode(root.right, str + '1', hcode)

    def decode(self, root, index, e_str, d_str):
        if root == None:
            return index
        if root.left == None and root.right == None:
            print(root.char, end="")
            d_str += root.char
            return index
        index+=1
        if e_str[index] == '0':
            index = self.decode(root.left, index, e_str, d_str)
        else:
            index = self.decode(root.right, index, e_str, d_str)
        return index

    def compress(self, txt):
        freq = {}
        for char in txt:
            if not char in freq:
                freq[char] = 0
            freq[char] += 1

        pq = []
        for key,value in freq.items():
            heapq.heappush(pq, Node(key,value))

        while len(pq) != 1:
            left = heapq.heappop(pq)
            right = heapq.heappop(pq)
            heapq.heappush(pq, Node('\0', left.freq+right.freq, left, right))

        self.root = pq[0]
        hcode = {}
        self.encode(self.root, "", hcode)
        #print("huffman codes:")
        #for key,value in hcode.items():
            #print(key+" "+value)

        #print("original string: "+txt)
        e_str = ""
        for i in range(len(txt)):
            e_str += hcode[txt[i]]
        return e_str

    def decompress(self, txt):
        index = -1
        d_str = ""
        while index < len(txt)-2:
            index = self.decode(self.root, index, txt, d_str)
        return d_str
