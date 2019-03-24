# -*- coding: utf-8 -*-

"""
TODO: accomplish these methods according to expert evaluation
"""
from enum import Enum

loan_state = Enum('load_state', ('due', 'over_due', 'during_duration'))


class CalcWeight(object):
    def calc_weight(self, guarantee_sum: int, duration: int, state: loan_state):
        pass


class GeneralGuarantee(CalcWeight):
    def calc_weight(self, guarantee_sum: int, duration: int, state: loan_state):
        pass


class JointLiabilityGuaranteeCalcWeight(CalcWeight):
    def calc_weight(self, guarantee_sum: int, duration: int, state: loan_state):
        pass


class PledgeCalcWeight(CalcWeight):
    def calc_weight(self, guarantee_sum: int, duration: int, state: loan_state):
        pass


class MortgageCalcWeight(CalcWeight):
    def calc_weight(self, guarantee_sum: int, duration: int, state: loan_state):
        pass


class LienCalcWeight(CalcWeight):
    def calc_weight(self, guarantee_sum: int, duration: int, state: loan_state):
        pass


class EarnestCalcWeight(CalcWeight):
    def calc_weight(self, guarantee_sum: int, duration: int, state: loan_state):
        pass
