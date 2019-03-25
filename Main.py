# -*- coding: utf-8 -*-
from GuaranteeGraph import *
from LabelPropagation import *

if __name__ == "__main__":
    LPA = LabelPropagation()
    g = GuaranteeGraph('clients.txt', 'guarantees.txt')
    g.nodes = LPA(g.nodes, g.graph)
    print(g)
