import bz2
import pickle
import _pickle as cPickle
import os
from SAP_Operador.modules.spellchecker.structures.ternarySearchTree import Trie, Node

WORLIST_FILE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..',
    'data',
    'wordDatasetPtBR.pbz2'
)

class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == 'Trie':
            return Trie
        if name == 'Node':
            return Node
        return super().find_class(module, name)

class PtBR:

    def __init__(self):
        self.trie = self.decompress_pickle(WORLIST_FILE_PATH)

    def compressed_pickle(self, filePath, data):
        with bz2.BZ2File(filePath, 'w') as f: 
            pickle.dump(data, f)

    def decompress_pickle(self, filePath):
        data = bz2.BZ2File(filePath, 'rb')
        data = CustomUnpickler(data).load()
        return data

    def hasWord(self, word):
        return word in self.trie


""" with open('../palavrasV3.txt', 'r') as f:
    lines = f.readlines()
    trie = None
    for l in lines:
        word = l.replace('\n', '')
        if not trie:
            trie = Trie(word)
            continue
        trie.append(word)
    compressed_pickle(WORLIST_FILE_PATH, trie) """
