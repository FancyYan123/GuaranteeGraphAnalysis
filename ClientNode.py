# -*- coding: utf-8 -*-

import math
from enum import Enum

ClientType = Enum('ClientType', ('Enterprise', 'individual'))


class ClientNode:
    """
    this class is to represent the node of gurantee graph
    """

    def __init__(self, id: str, client_type: ClientType = 'Enterprise', level: int = 0):
        """
        :param type: client type
        :param level: bank's credit level for this client
        """
        self.ID = id
        self.type = client_type
        self.level = level
        self.positive_label = (0.5, 0.5)

    def calculate_label(self, due_sum, overdue_sum):
        """
        
        TODO: finish this method to after determined how to calculate the label.
        :param due_sum:
        :param overdue_sum:
        :return:
        """
        positive = math.fabs(due_sum)
        negetive = math.fabs(overdue_sum)
        self.positive_label = positive / (positive + negetive)
        return self.positive_label
