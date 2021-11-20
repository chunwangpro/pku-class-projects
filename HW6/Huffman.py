from collections import Counter
import struct


class HuffmanTree:
    class Node:
        def __init__(self, name=None, val=None):
            self._name = name
            self._val = val
            self._left = None
            self._right = None
            self._code = ''

    def __init__(self, origintext):
        # calculate frequency
        with open(origintext) as f:
            self.origintext = "" + f.read()  # .replace('\n', '').replace('\r', '')#.replace(' ', '')
        self.frequency = Counter(self.origintext)
        # init nodes
        self.nodes = [self.Node(name=part[0], val=part[1]) for part in self.frequency.items()]
        # build huffman tree
        while len(self.nodes) != 1:
            self.nodes.sort(key=lambda node: node._val, reverse=True)
            parent = self.Node(name=None, val=(self.nodes[-1]._val + self.nodes[-2]._val))
            parent._left = self.nodes.pop()
            parent._right = self.nodes.pop()
            self.nodes.append(parent)
        # root
        self.root = self.nodes[0]
        self.root._code = '0'
        # code & decode dictionary
        self.codes, self.decodes = {}, {}
        # bit remain
        self.remain = 0

    def give_code(self, node):
        if node._name is not None:
            self.codes.update({node._name: node._code})
        if node._left:
            node._left._code = f'{node._code}0'
            self.give_code(node._left)
        if node._right:
            node._right._code = f'{node._code}1'
            self.give_code(node._right)

    def plain_to_cipher(self):
        self.give_code(self.root)
        content = ""
        for s in self.origintext:
            content += self.codes[s]
        length = len(content)
        with open("ciphertext.txt", "wb") as f:
            for i in range(0, length, 8):
                if i + 8 < length:
                    f.write(struct.pack('B', int(content[i: i + 8], 2)))
                else:  # padding
                    self.remain = length - i
                    f.write(struct.pack('B', int(content[i:], 2)))

    def cipher_to_plain(self, file="ciphertext.txt"):
        text = []
        with open(file, "rb") as f:
            data = f.read(1)
            while data:
                text.append(bin(struct.unpack('B', data)[0])[2:])
                data = f.read(1)
        for i in range(len(text) - 1):
            text[i] = f"{'0'*(8 - len(text[i]))}{text[i]}"
        text[-1] = f"{'0'*(self.remain - len(text[-1]))}{text[-1]}"
        text = [bit for byte in text for bit in byte]
        text.reverse()
        current, decode = "", ""
        self.decodes = {v: k for k, v in self.codes.items()}
        while text:
            current += text.pop()
            if current in self.decodes.keys():
                decode += self.decodes[current]
                current = ""
        with open("plaintext.txt", "w") as f:
            f.write(decode)


if __name__ == '__main__':
    tree = HuffmanTree("origintext.txt")
    tree.plain_to_cipher()
    tree.cipher_to_plain()
    print(f"character frequency：\n{tree.frequency}")
    print(f"code dictionary：\n{tree.codes}")
    print(f"decode dictionary：\n{tree.decodes}")
