# -*- coding: utf-8 -*-

import numpy as np


class LabelPropagation:

    def __init__(self, strong_positive_th=1.1, strong_negetive_th=0, iterative_th=3):
        self.strong_positive_th = strong_positive_th
        self.strong_negetive_th = strong_negetive_th
        self.iterative_th = iterative_th

    def __call__(self, nodes: dict, graph: dict):
        # label值大于或者小于某一个阈值才被称为为label样本
        # self.label是所有强置信的标签，self.unlabel是弱置信的标签
        # self.labeled_id, self.unlabeled_id分别是上文标签对应的用户id
        self.labeled_id, self.unlabeled_id = [], []
        self.label, self.unlabel = [], []
        for Id in nodes:
            node = nodes[Id]
            if node.positive_label > self.strong_positive_th or \
                    node.positive_label < self.strong_negetive_th:
                self.labeled_id.append(Id)
                self.label.append(node.positive_label)
            else:
                self.unlabeled_id.append(Id)
                self.unlabel.append(node.positive_label)
        assert (len(self.label) >= 0 and len(self.unlabel) > 0)
        self.label, self.unlabel = np.array(self.label), np.array(self.unlabel)

        self.P_ul, self.P_uu = np.zeros((len(self.unlabel), len(self.label))), \
                               np.zeros((len(self.unlabel), len(self.unlabel)))

        # 制作id和index的字典
        labelid_index, count1, unlabelid_index, count2 = dict(), 0, dict(), 0
        for each in self.labeled_id:
            labelid_index[each] = count1
            count1 += 1
        for each in self.unlabeled_id:
            unlabelid_index[each] = count2
            count2 += 1

        # 为了便于统计，需要将所有边反向
        graph = self.__transpose_graph(graph)
        # 统计概率转移矩阵P_ul, P_uu
        for each in self.unlabeled_id:
            row = unlabelid_index[each]
            all_edges, all_weight = graph[each], 0
            for edge in all_edges:
                all_weight += edge[1]
            for edge in all_edges:
                if edge[0] in labelid_index:
                    col = labelid_index[edge[0]]
                    self.P_ul[row][col] = edge[1] / all_weight
                else:
                    col = unlabelid_index[edge[0]]
                    self.P_uu[row][col] = edge[1] / all_weight

        self.__evaluate()
        return self.__renew(nodes)

    def __evaluate(self):
        count_iterate = 0
        while True:
            count_iterate += 1
            new_unlabel = np.dot(self.P_ul, self.label) + np.dot(self.P_uu, self.unlabel)
            if np.sum(np.power(new_unlabel - self.unlabel, 2)) < 0.1 or \
                    count_iterate > self.iterative_th:
                break
            self.unlabel = self.unlabel * 0.8 + new_unlabel * 0.2

    def __renew(self, nodes: dict) -> dict:
        for i in range(len(self.unlabel)):
            Id = self.unlabeled_id[i]
            positive_label = self.unlabel[i]
            nodes[Id].positive_label = positive_label
        return nodes

    def __transpose_graph(self, graph: dict):
        transposed_graph = dict()
        for start_node in graph:
            edges = graph[start_node]
            for each in edges:
                if each[0] in transposed_graph:
                    transposed_graph[each[0]].append([start_node, each[1]])
                else:
                    transposed_graph[each[0]] = [[start_node, each[1]]]
        return transposed_graph
