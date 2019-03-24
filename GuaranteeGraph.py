# -*- coding: utf-8 -*-
from ClientNode import *
from StategiesCalcWeight import *


class GuaranteeGraph(object):
    def __init__(self, client_filepath: str, guarantee_filepath: str):
        clients = self.__construct_client_nodes(client_filepath)
        # get the graph structure in a dict(key: id, value: [[nodeID, weight], ...]
        # get all the nodes in a dict(key: id, value: Node)
        self.nodes, self.graph = self.__construct_guarantee_edges(clients, guarantee_filepath)

    def __construct_client_nodes(self, client_filepath: str) -> dict:
        allnodes = dict()
        clientfile = open(client_filepath, 'r')
        for line in clientfile:
            line = line.split(',')
            client_type = ClientType.Enterprise if int(line[1]) == 1 else ClientType.Individual
            allnodes[line[0]] = ClientNode(line[0], client_type, int(line[2]))
        clientfile.close()
        return allnodes

    def __construct_guarantee_edges(self, clients: dict, guarantee_filepath: str):
        graph, client_loan = dict(), dict()
        for each in clients:
            client_loan[each] = [0, 0]
        guaranteefile = open(guarantee_filepath, 'r')
        guaranteefile.readline()
        for line in guaranteefile:
            line = line.split(',')
            loan_type, guarantee_id, client_id, duration, sum, ratio, state = \
                int(line[1]), line[2], line[3], int(line[4]), int(line[5]), float(line[6]), int(line[7])
            state = {1: loan_state.due, 2: loan_state.overdue, 3: loan_state.during_duration}.get(state, loan_state.due)

            # calculate and renew the edge weight
            weight_to_add = self.__calc_edge_weight(loan_type, sum, duration, state)
            if guarantee_id not in graph:
                graph[guarantee_id] = [[client_id, weight_to_add]]
            else:
                add_new_edge = True
                for i in range(len(graph[guarantee_id])):
                    if graph[guarantee_id][i][0] == client_id:
                        graph[guarantee_id][i][1] += weight_to_add
                        add_new_edge = False
                if add_new_edge:
                    graph[guarantee_id].append([client_id, weight_to_add])

            # calculate the due and overdue loan:
            if state is loan_state.due:
                client_loan[client_id][0] += sum
            elif state is loan_state.overdue:
                client_loan[client_id][1] += sum

        for each in clients:
            clients[each].calculate_label(client_loan[each][0], client_loan[each][1])
        return clients, graph

    def __calc_edge_weight(self, loan_type: int, guarantee_sum: int, duration: int, state: loan_state):
        if loan_type == 1:
            return GeneralGuarantee.calc_weight(guarantee_sum, duration, state)
        elif loan_type == 2:
            return JointLiabilityGuaranteeCalcWeight.calc_weight(guarantee_sum, duration, loan_state)
        elif loan_type == 3:
            return PledgeCalcWeight.calc_weight(guarantee_sum, duration, loan_type)
        elif loan_type == 4:
            return MortgageCalcWeight.calc_weight(guarantee_sum, duration, loan_type)
        elif loan_type == 5:
            return LienCalcWeight.calc_weight(guarantee_sum, duration, loan_type)
        elif loan_type == 6:
            return EarnestCalcWeight.calc_weight(guarantee_sum, duration, loan_type)
        else:
            raise Exception("The guarantee type is not considered.")


if __name__ == "__main__":
    g = GuaranteeGraph('clients.txt', 'guarantees.txt')
    print('Graph constructed. ')
